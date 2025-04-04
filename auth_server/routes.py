from fastapi import APIRouter, Request, HTTPException

router = APIRouter()

@router.get("/verify")
async def verify(request: Request):
    api_key = request.headers.get("x-api-key")
    if not api_key:
        raise HTTPException(status_code=400, detail="Missing API Key")

    async with request.app.state.pool.acquire() as conn:
        row = await conn.fetchrow("SELECT * FROM api_keys WHERE key = $1", api_key)
        if row:
            return {"valid": True}
        raise HTTPException(status_code=401, detail="Invalid API Key")