from .BaseDataModel import BaseDataModel
from models.db_schemes import Project
from .enums.DBEnum import DBEnum

class ProjectModel(BaseDataModel):
    def __init__(self, db_client: object):
        super().__init__(db_client)
        self.collection = self.db_client[DBEnum.COLLECTION_PROJECT_NAME.value]

    async def create_project(self, project:Project):
        result =await self.collection.insert_one(project.dict())
        project._id = result.inserted_id

        return project
    
    async def get_project_or_create (self, project_id:str):
        record = await self.collection.find_one({
            project_id : project_id
        })
        if record is None:
            project = Project(project_id = project_id)
            project = await self.create_project(project=project)
            return project
        
        return Project(**record)
    
    async def get_all_projects(self, page_size:int, page: int=1):
        total_documents = await self.collection.count_documents({})
        total_pages = total_documents // page_size
        if total_documents % total_pages > 0:
            total_pages += 1

        cursor = self.collection.find().skip((page-1) * page_size).limit(page_size)
            # find():
            # Queries all documents in the collection.
            # skip((page - 1) * page_size):
            # Skips documents from previous pages to start at the correct offset for the current page.
            # Example:
            # Page 1 (offset = 0): Skip 0 documents.
            # Page 2 (offset = 10, with page_size = 10): Skip the first 10 documents.
            # limit(page_size):
            # Limits the number of documents retrieved to the page size.
        projects = []
        async for document in cursor:
            projects.append(
                Project(**document)
            )

        return projects, total_pages
    