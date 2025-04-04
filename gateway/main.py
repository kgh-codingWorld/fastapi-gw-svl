from fastapi import FastAPI
from gateway.core.router import gateway_router

app = FastAPI()
app.include_router(gateway_router)