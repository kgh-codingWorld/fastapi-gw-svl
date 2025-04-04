from fastapi import FastAPI
from gateway.core.router import gateway_router
from gateway.core.middleware import verify_api_key_middleware
from gateway.core.lifespan import lifespan

app = FastAPI(lifespan=lifespan) # DB 연결
app.middleware("http")(verify_api_key_middleware) # API Key 유효성 검사
app.include_router(gateway_router) # 유효한 요청일 시 라우터 처리