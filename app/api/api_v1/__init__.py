from fastapi import APIRouter

from app.core import settings

from .weather import router as weather_router

router = APIRouter(
    prefix=settings.api.v1.prefix,
)

for rout in (weather_router,):
    router.include_router(
        router=rout,
    )
