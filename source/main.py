from fastapi import FastAPI
from contextlib import asynccontextmanager
from routes import base, data
from motor.motor_asyncio import AsyncIOMotorClient
from helpers.config import get_setting

app = FastAPI()

@app.on_event("startup")
async def startup_db_client():
    settings = get_setting()
    app.mongo_conn =  AsyncIOMotorClient(settings.MONGODB_URL)
    app.db_client = app.mongo_conn[settings.MONGODB_DATABASE]
    
@app.on_event("shutdown")
async def shutdown_db_client():
    app.mongo_conn.close()


app.include_router(base.baseRouter)
app.include_router(data.dataRouter)