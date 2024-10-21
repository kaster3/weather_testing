__all__ = (
    "application",
    "main",
)

from core import settings
from core.gunicorn import Application, get_app_options
from main import application


def main():
    Application(
        application=application,
        options=get_app_options(
            host=settings.gunicorn.host,
            port=settings.gunicorn.port,
            timeout=settings.gunicorn.timeout,
            workers=settings.gunicorn.workers,
            log_level=settings.logging.log_level,
        ),
    ).run()


if __name__ == "__main__":
    main()
