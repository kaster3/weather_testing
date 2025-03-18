from dishka import AsyncContainer, make_async_container

from app.core import Settings


def init_async_container(settings: Settings) -> AsyncContainer:
    container = make_async_container(
        context={
            Settings: settings,
        }
    )
    return container
