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
    """
    FastAPI 라우터 설정 파일, HTTP 요청이 들어오면 이 요청을 처리하고 API 키 인증을 호출
    """
    # 1. API Key 추출
    api_key = request.headers.get("x-api-key")

    # 2. API Key가 없거나 인증 실패하면 401 에러 반환
    if not api_key or not await is_valid_api_key(api_key):
        return JSONResponse(status_code=401, content={"error": "Unauthorized"})

    # 3. 요청 경로 기반으로 서비스 URL 찾기
    full_path = f"/{path}"
    target_base_url = ROUTES.get(full_path)
    if not target_base_url:
        return JSONResponse(status_code=404, content={"error": "라우터를 찾을 수 없음"})

    forward_url = f"{target_base_url}{full_path}"

    # 4. 실제 요청을 대상 서비스로 전달
    async with httpx.AsyncClient() as client:
        response = await client.request(
            method=request.method,
            url=forward_url,
            headers=request.headers.raw,
            content=await request.body()
        )
        return JSONResponse(status_code=response.status_code, content=response.json())
