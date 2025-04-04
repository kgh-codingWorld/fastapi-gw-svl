from fastapi import APIRouter

router = APIRouter()

@router.get("/hello")
async def hello():
    return {"msg": "hello from hello_service"}