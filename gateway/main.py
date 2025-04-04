from fastapi import FastAPI
from gateway.core.router import gateway_router
from auth_server.main import lifespan

app = FastAPI(lifespan=lifespan)
app.include_router(gateway_router)