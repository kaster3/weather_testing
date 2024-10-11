from fastapi import APIRouter

from core import settings
from .some_endpoint import router as endpoint


router = APIRouter(
    prefix=settings.api.v1.prefix,
)

for rout in (endpoint, ):
    router.include_router(
        router=rout,
    )
