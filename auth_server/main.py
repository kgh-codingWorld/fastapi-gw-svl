from fastapi import FastAPI
from auth_server.routes import router
import asyncpg
import asyncio
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("lifespan 진입 - DB 연결 시도 중...")
    for i in range(10):
        try:
            app.state.pool = await asyncpg.create_pool(
                user="postgres", password="password",
                database="auth", host="postgres"
            )
            print("🎉 DB 연결 성공")
            break
        except Exception as e:
            print(f"DB 연결 실패 {i+1}/10회 - {e}")
            await asyncio.sleep(1)
    else:
        raise RuntimeError("DB 연결에 반복적으로 실패함 ㅜ")

    yield  # 앱이 실행되는 동안

    print("앱 종료 - DB 커넥션 풀 정리 중...")
    await app.state.pool.close()
    print("DB 연결 종료 완료")

app = FastAPI(lifespan=lifespan)
app.include_router(router)
