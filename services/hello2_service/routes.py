from fastapi import APIRouter

router = APIRouter()

@router.get("/hello2")
async def hello():
    return {"msg": "hello2 from hello2_service"}