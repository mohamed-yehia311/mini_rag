from fastapi import FastAPI
from contextlib import asynccontextmanager
from routes import base, data, chat
from motor.motor_asyncio import AsyncIOMotorClient
from helpers.config import get_settings
from stores import LLMProviderFactory
from stores.VectorDB.VectorDB_Providers_Factory import VectorDBProviderFactory
from stores.llm.template.template_parser import TemplateParser

app = FastAPI()

@app.on_event("startup")
async def startup_db_client():
    settings = get_settings()
    app.mongo_conn =  AsyncIOMotorClient(settings.MONGODB_URL)
    app.db_client = app.mongo_conn[settings.MONGODB_DATABASE]
    
    llm_provider_factory = LLMProviderFactory(settings)
    vectordb_provider_factory = VectorDBProviderFactory(settings)

    # generation client
    app.generation_client = llm_provider_factory.create(provider=settings.GENERATION_BACKEND)
    app.generation_client.set_generating_model(model_id = settings.GENERATION_MODEL_ID)

    # embedding client
    app.embedding_client = llm_provider_factory.create(provider=settings.EMBEDDING_BACKEND)
    app.embedding_client.set_embedding_model(model_id=settings.EMBEDDING_MODEL_ID,
                                             embedding_size=settings.EMBEDDING_MODEL_SIZE)
    
    # vector db client
    app.vectordb_client = vectordb_provider_factory.create(
        provider=settings.VECTOR_DB_BACKEND
    )
    app.vectordb_client.connect()

    app.template_parser = TemplateParser(
        language=settings.PRIMARY_LANG,
        default_language=settings.DEFAULT_LANG,
    )
    
@app.on_event("shutdown")
async def shutdown_db_client():
    app.mongo_conn.close()
    app.vectordb_client.disconnect()


app.include_router(base.baseRouter)
app.include_router(data.dataRouter)
app.include_router(chat.chat_router)