from fastapi import APIRouter

router = APIRouter()

@router.get("/bye")
async def hello():
    return {"msg": "bye from bye_service"}