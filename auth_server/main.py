from fastapi import FastAPI
from auth_server.routes import router
import asyncpg
import asyncio

app = FastAPI()
app.include_router(router)

@app.on_event("startup") #lifespan 
async def startup():
    for i in range(10):
        try:
            app.state.pool = await asyncpg.create_pool(
                user="postgres", password="password",
                database="auth", host="postgres"
            )
            return
        except Exception as e:
            print(f"DB 연결 실패 {i+1}/10회 - {e}")
            await asyncio.sleep(1)
    else:
        raise RuntimeError("DB 연결에 반복적으로 실패함")
