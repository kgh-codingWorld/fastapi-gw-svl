from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from .auth import is_valid_api_key
import httpx, json
from pathlib import Path

gateway_router = APIRouter()

# 라우팅 테이블 로드
with open(Path(__file__).parent / "routes.json") as f:
    ROUTES = json.load(f)

@gateway_router.api_route("/{path:path}", methods=["GET", "POST", "PUT", "DELETE"], response_class=JSONResponse)
async def gateway(path: str, request: Request):
    api_key = request.headers.get("x-api-key")
    if not api_key or not await is_valid_api_key(api_key):
        return JSONResponse(status_code=401, content={"error": "Unauthorized"})

    full_path = f"/{path}"
    target_base_url = ROUTES.get(full_path)
    if not target_base_url:
        return JSONResponse(status_code=404, content={"error": "Route not found"})

    forward_url = f"{target_base_url}{full_path}"

    async with httpx.AsyncClient() as client:
        response = await client.request(
            method=request.method,
            url=forward_url,
            headers=request.headers.raw,
            content=await request.body()
        )
        return JSONResponse(status_code=response.status_code, content=response.json())
