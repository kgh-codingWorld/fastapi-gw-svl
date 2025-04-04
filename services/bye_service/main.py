from fastapi import FastAPI
from services.bye_service.routes import router

app = FastAPI()
app.include_router(router)