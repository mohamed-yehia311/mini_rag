from fastapi import FastAPI, APIRouter, Depends, UploadFile, status, Request
from fastapi.responses import JSONResponse
from helpers.config import get_setting, Settings
from controllers import DataController, ProjectController, ProcessController
import os
import aiofiles
from models import ResponseSignal
import logging
from models import ProcessRequest 
from models.ProjectModel import ProjectModel
from models.ChunkModel import ChunkModel
from models.db_schemes import DataChunck

logger = logging.getLogger('uvicorn.error')


dataRouter = APIRouter(
    prefix="/api/v1/data",
    tags=["api_v1", "data"],
)

@dataRouter.post("/upload/{project_id}")
async def upload_data(request : Request, project_id:str, file: UploadFile,
                       setting: Settings = Depends(get_setting)):
    project_model = ProjectModel(
        db_client=request.app.db_client
    )

    project = await project_model.get_project_or_create(
        project_id= project_id
    )

    is_valide, signal = DataController().validate_uploaded_file(file)

    if not is_valide :
        return JSONResponse(
            status_code = status.HTTP_400_BAD_REQUEST,
            content={
                "signal": signal
            }
        )
    
    file_path, file_id = ProjectController().generate_unique_file_path(
        orig_file_name= file.filename,
        project_id= project_id
    )


    try:
        async with aiofiles.open(file_path, "wb") as f:
            while chunck := await file.read(setting.FILE_DEFAULT_CHUNK_SIZE):
                await f.write(chunck)
                
    except Exception as e:
        logger.error(f"Error While uploading file: {e}")


        return JSONResponse(
            status_code = status.HTTP_400_BAD_REQUEST,   
            content = {
                "signal": ResponseSignal.FILE_UPLOAD_FAILED.value
            }
        )

    return JSONResponse(
        content = {
            "Signal": ResponseSignal.FILE_UPLOAD_SUCCESS.value,
            "file_id": file_id,
            "project_id": str(project._id) 
        }
    )

@dataRouter.post("/process/{project_id}")
async def process(request: Request, project_id:str, ProcessRequest: ProcessRequest):
    file_id = ProcessRequest.file_id
    chunk_size = ProcessRequest.chunk_size
    overlap = ProcessRequest.chunk_size
    do_reset = ProcessRequest.do_reset


    project_model = ProjectModel(
        db_client=request.app.db_client
    )

    project = await project_model.get_project_or_create(
        project_id= project_id
    )
    procesescontroller = ProcessController(project_id=project_id)
    
    file_content = procesescontroller.get_file_content(file_id=file_id)

    file_chunks = procesescontroller.process_content(file_content=file_content, chunk_size=chunk_size, overlap_size= overlap)
    if len(file_chunks) == 0 or file_chunks == None:
        return JSONResponse(
            status_code = status.HTTP_400_BAD_REQUEST,
            content = ResponseSignal.FILE_PROCESSING_FAILD.value
        )

    file_chunks_records = [
        DataChunck(
            chunk_text=chunk.page_content,
            chunk_metadata=chunk.metadata,
            chunk_order=i+1,
            chunk_project_id=project._id,
        )for i, chunk in enumerate(file_chunks)
    ]
    chunk_model = ChunkModel(
        db_client=request.app.db_client
    )

    if do_reset == 1:
        _ = await chunk_model.delete_chunks_by_project_id(
            project_id=project.id
        )

    records = await chunk_model.insert_many_chunks(chunks=file_chunks_records)

    return JSONResponse(
        content={
            "signal": ResponseSignal.FILE_PROCESSING_SUCESS.value,
            "inserted_chunks": records
        }
    )