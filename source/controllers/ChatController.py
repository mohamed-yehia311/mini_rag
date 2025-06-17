from .BaseController import BaseController
from models.db_schemes import Project, DataChunk, RetrievedDocument
from models.enums.LLMEnum import DocumentTypeEnum
from typing import List
from stores.VectorDB.providers import QdrantDBProvider
import json

class ChatController(BaseController):
    def __init__(self, vectordb_client: QdrantDBProvider, generation_client, 
                 embedding_client, template_parser):
        super().__init__()

        self.vectordb_client = vectordb_client
        self.generation_client = generation_client
        self.embedding_client = embedding_client
        self.template_parser = template_parser
        
        
    def create_collection_name(self, project_id: str):
        return f"collection_{project_id}".strip()
    
    def reset_vectordb_collection(self, project: Project):
        collection_name = self.create_collection_name(project_id=project.project_id)
        return self.vectordb_client.delete_collection(collection_name=collection_name)
    
    def get_Vector_db_Collection_info(self, project: Project):
        collection_name = self.create_collection_name(project_id= project.project_id)
        collection_info = self.vectordb_client.get_collection_info(collection_name= collection_name)
        
        return json.loads(
            json.dumps(collection_info, default=lambda x: x.__dict__)
        )

    def index_into_vector_db(self, project: Project, 
                                   chunks: List[DataChunk], Chunks_ids:List[int], 
                                   do_reset: bool = False):
        #get_collection_name
        collection_name = self.create_collection_name(project_id=project.project_id)
        
        texts = [chunck.chunk_text for chunck in chunks]
        metadata = [chunk.chunk_metadata for chunk in chunks] 
        vectors = [ 
            self.embedding_client.generate_embedding(text= text, document_type= DocumentTypeEnum.DOCUMENT.value)
                for text in texts
            ]
        #if collection is not exist
        _ = self.vectordb_client.create_collection(
            collection_name=collection_name,
            embedding_size=self.embedding_client.embedding_size,
            do_reset=do_reset,
        )
        
        _ = self.vectordb_client.insert_many(
            collection_name=collection_name,
            texts=texts,
            metadata=metadata,
            vectors=vectors,
            record_ids=Chunks_ids,
        )
    
        return True
    
    
    def search_vector_db_collection(self, project: Project, text:str, limit: int = 20):
        
        collection_name = self.create_collection_name(project_id=project.project_id)
        
        vector = self.embedding_client.generate_embedding(text= text, document_type=DocumentTypeEnum.QUERY.value)
        
        if not vector or len(vector) == 0:
            return False
        
        results = self.vectordb_client.search_by_vector(
            collection_name=collection_name,
            vector=vector,
            limit=limit
        )
        
        if not results:
            return False
        
        return results
    

    
    def answer_rag_question(self, project: Project, query: str, limit: int = 10):
        
        answer, full_prompt, chat_history = None, None, None

        # step1: retrieve related documents
        retrieved_documents = self.search_vector_db_collection(
            project=project,
            text=query,
            limit=limit,
        )

        if not retrieved_documents or len(retrieved_documents) == 0:
            return answer, full_prompt, chat_history
        
        # step2: Construct LLM prompt
        system_prompt = self.template_parser.get("rag", "system_prompt")

        documents_prompts = "\n".join([
            self.template_parser.get("rag", "document_prompt", {
                    "doc_num": idx + 1,
                    "chunk_text": doc.text,
            })
            for idx, doc in enumerate(retrieved_documents)
        ])

        footer_prompt = self.template_parser.get("rag", "footer_prompt",{
            "query": query
        })

        # step3: Construct Generation Client Prompts
        chat_history = [
            self.generation_client.construct_prompt(
                prompt=system_prompt,
                role=self.generation_client.enums.SYSTEM.value,
            )
        ]

        full_prompt = "\n\n".join([ documents_prompts,  footer_prompt])

        # step4: Retrieve the Answer
        answer = self.generation_client.generate_text(
            prompt=full_prompt,
            chat_history=chat_history
        )

        return answer, full_prompt, chat_history
    