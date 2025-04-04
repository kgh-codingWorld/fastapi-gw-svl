import httpx
import redis.asyncio as redis

redis_client = redis.Redis(host="redis", port=6379, decode_responses=True)

async def is_valid_api_key(api_key: str) -> bool:
    cached = await redis_client.get(api_key)
    if cached:
        print("Redis 캐시에서 인증됨")
        return True

    print("Redis에 없음. 인증 서버로 요청")

    try:
        print("try 진입")
        async with httpx.AsyncClient() as client:  
            print("http에 요청") 
            res = await client.get(
                "http://auth_server:8000/verify",
                headers={"x-api-key": api_key},
                timeout=3.0
            )
            print(f"@@@@@@{res}")
            if res.status_code == 200:
                await redis_client.set(api_key, "valid", ex=3600)  # TTL 1시간
                print("인증 서버 통해 인증됨. Redis에 저장")
                return True
    except httpx.RequestError as e:
        print("Auth request failed:", e)
        return False
