import httpx

async def is_valid_api_key(api_key: str) -> bool:
    async with httpx.AsyncClient() as client:
        try:
            res = await client.get(
                "http://auth_server:8000/verify",
                headers={"x-api-key": api_key},
                timeout=3.0
            )
            return res.status_code == 200
        except httpx.RequestError as e:
            print("Auth request failed:", e)
            return False
