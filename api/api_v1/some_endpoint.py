from fastapi import APIRouter

from core import settings


router = APIRouter(
    prefix=settings.api.v1.endpoint,
    tags=["some_endpoint"],
)


@router.get("")
async def get_endpoint():
    return {"message": "Hello, this is the endpoint you requested!"}