from fastapi import FastAPI, APIRouter, Depends, UploadFile, status
from fastapi.responses import JSONResponse
from helpers.config import get_setting, Settings
from controlers import Datacontroler, ProjectControler
import os
import aiofiles
from models import ResponseSignal
import logging

logger = logging.getLogger('uvicorn.error')


dataRouter = APIRouter(
    prefix="/api/v1/data",
    tags=["api_v1", "data"],
)

@dataRouter.post("/upload/{project_id}")
async def upload_data(project_id:str, file: UploadFile,
                       setting: Settings = Depends(get_setting)):

    is_valide, signal = Datacontroler().validate_uploaded_file(file)

    if not is_valide :
        return JSONResponse(
            status_code = status.HTTP_400_BAD_REQUEST,
            content={
                "signal": signal
            }
        )
    
    project_dir_path = ProjectControler().get_project_path(project_id)
    file_path, file_id = ProjectControler().generate_unique_file_path(
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
            "file_id": file_id
        }
    )
