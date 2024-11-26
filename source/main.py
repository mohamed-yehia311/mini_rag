from fastapi import FastAPI
from routes import base, data


app = FastAPI()
app.include_router(base.baseRouter)
app.include_router(data.dataRouter)