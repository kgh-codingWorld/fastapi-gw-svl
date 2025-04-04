from contextlib import asynccontextmanager
import asyncpg
import asyncio
from fastapi import FastAPI
import redis.asyncio as redis

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("lifespan 진입 - DB/Redis 연결 시도 중...")
    for i in range(10):
        try:
            app.state.pool = await asyncpg.create_pool(
                user="postgres", password="password",
                database="auth", host="postgres"
            )
            app.state.redis = redis.Redis(host="redis", port=6379, decode_responses=True)
            await app.state.redis.ping()
            print("🎉 DB 연결 성공")
            break
        except Exception as e:
            print(f"DB 연결 실패 {i+1}/10회 - {e}")
            await asyncio.sleep(1)
    else:
        raise RuntimeError("DB 연결에 반복적으로 실패함 ㅜ")

    yield

    print("앱 종료 - DB 커넥션 풀 정리 중...")
    await app.state.pool.close()
    await app.state.redis.close()
    print("DB 연결 종료 완료")