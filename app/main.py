import logging
from contextlib import asynccontextmanager

from dishka.integrations.fastapi import setup_dishka
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from app.api import router as api_router
from app.core import Settings
from app.core.gunicorn import Application, get_app_options
from app.ioc.init_container import init_async_container


@asynccontextmanager
async def lifespan(app: FastAPI):
    logging.info("Application starts successfully!")
    yield
    await app.state.dishka_container.close()
    logging.info("Application ends successfully!")


def create_fastapi_app() -> FastAPI:
    """Создаем FastAPI приложение и настраиваем его на роутеры"""
    app = FastAPI(
        default_response_class=ORJSONResponse,
        lifespan=lifespan,
    )
    app.include_router(
        router=api_router,
    )
    return app


def create_app(settings: Settings) -> FastAPI:
    """Настраиваем логи, контейнер с зависимостями и инициализируем наше приложение"""
    logging.basicConfig(
        level=logging.INFO,
        format=settings.logging.log_format,
    )
    app = create_fastapi_app()
    container = init_async_container(settings=settings)
    setup_dishka(container, app)
    return app


# Запускаем приложение с uvicorn воркерами и gunicorn менеджера
if __name__ == "__main__":
    settings = Settings()
    Application(
        application=create_app(settings=settings),
        options=get_app_options(
            host=settings.gunicorn.host,
            port=settings.gunicorn.port,
            timeout=settings.gunicorn.timeout,
            workers=settings.gunicorn.workers,
            log_level=settings.logging.log_level,
        ),
    ).run()
