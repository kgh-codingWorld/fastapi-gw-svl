from contextlib import asynccontextmanager
from fastapi import FastAPI
import asyncio
import redis.asyncio as redis
from auth_server.routes import router

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("lifespan 진입 - Redis 연결 시도 중...")
    for i in range(10):
        try:
            app.state.redis = redis.Redis(host="redis", port=6379, decode_responses=True)
            await app.state.redis.ping()
            print("Redis 연결 성공")
            break
        except Exception as e:
            print(f"Redis 연결 실패 {i+1}/10회 - {e}")
            await asyncio.sleep(1)
    else:
        raise RuntimeError("Redis 연결 실패")

    yield

    print("앱 종료 - Redis 연결 종료 중...")
    await app.state.redis.close()
    print("Redis 연결 종료 완료")

app = FastAPI(lifespan=lifespan)
app.include_router(router)