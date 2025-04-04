from fastapi import Request
from starlette.responses import JSONResponse
import time

async def verify_api_key_middleware(request:Request,call_next):
    api_key = request.headers.get("x-api-key")
    if not api_key:
        return JSONResponse(status_code=401,content={"error":"API Key missing"})
    
    redis = request.app.state.redis
    cached = await redis.get(api_key)

    if cached:
        print(f"Redis 캐시에서 인증된 키 사용됨")
    else:

        async with request.app.state.pool.acquire() as conn:
            row = await conn.fetchrow("SELECT * FROM api_keys WHERE key = $1", api_key)
            if not row:
                return JSONResponse(status_code=401, content={"error":"Invalid API Key"})
            await redis.set(api_key, "valid", ex=3600)
            print("🔐 DB에서 인증 후 Redis에 저장됨")
        
    return await call_next(request)