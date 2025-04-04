from fastapi import FastAPI
from services.hello2_service.routes import router

app = FastAPI()
app.include_router(router)