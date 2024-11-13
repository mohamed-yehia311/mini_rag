from fastapi import FastAPI, APIRouter
import os

baseRouter = APIRouter()

@baseRouter.get("/")
async def welcome():
    app_name = os.getenv('APP_NAME')
    app_version = os.getenv('APP_VERSION')

    return {
        "app_name": app_name,
        "app_version": app_version,
        "message" : "how are u ? "
    }