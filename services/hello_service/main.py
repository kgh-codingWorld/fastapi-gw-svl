from fastapi import FastAPI
from services.hello_service.routes import router

app = FastAPI()
app.include_router(router)