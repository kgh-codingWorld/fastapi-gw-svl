from fastapi import APIRouter, Request, HTTPException

router = APIRouter()

@router.get("/verify")
async def verify(request: Request):
    api_key = request.headers.get("x-api-key")
    if not api_key:
        raise HTTPException(status_code=400, detail="Missing API Key")

    redis = request.app.state.redis
    cached = await redis.get(api_key)
    if cached == "valid":
        return {"valid": True}
    raise HTTPException(status_code=401, detail="Invalid API Key")