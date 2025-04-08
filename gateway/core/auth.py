import httpx # 인증서버와 통신하기 위한 HTTP 클라이언트
import redis.asyncio as redis # Redis 비동기 클라이언트 사용

redis_client = redis.Redis(host="redis", port=6379, decode_responses=True)

async def is_valid_api_key(api_key: str) -> bool:
    """
    실제로 API Key를 Redis 캐시를 통해 인증하는 로직 담당
    """
    # 1. Redis에 캐시된 API Key 있는지 확인
    cached = await redis_client.get(api_key)
    if cached == "valid":
        print("Redis 캐시에서 인증됨")
        return True
    elif cached == "invalid": # 여기서 실패하면 굳이 아래 try-except문까지 갈 필요 없게 됨
        print("Redis 캐시에서 인증 거부됨")
        return False

    # 2. Redis에 없다면 인증 서버로 요청
    print("Redis에 없음. 인증 서버로 요청")

    try:
        print("try 진입")
        async with httpx.AsyncClient() as client:  
            print("http에 요청") 
            response = await client.get(
                "http://auth_server:8000/verify",
                headers={"x-api-key": api_key},
                timeout=3.0
            )
            print(f"인증서버 응답: {response.status_code}")

            # 3. 인증 서버 응답이 200이면 Redis에 저장
            if response.status_code == 200:
                await redis_client.set(api_key, "valid", ex=3600)  # TTL 1시간
                print("인증 서버 통해 인증됨. Redis에 저장 완료됨.")
                return True
            else:
                # 4. 인증 실패하면 Redis에 invalid로 짧은 시간 동안 저장(잘못된 API Key로 반복 요청 시 인증 서버 보호 목적!!)
                await redis_client.set(api_key, "invalid", ex=60)
                print("인증 실패, Redis에 임시 저장")
    except httpx.RequestError as e:
        print("인증 서버 요청 실패:", e)
        return False
