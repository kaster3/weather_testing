__all__ = (
    "application",
    "main",
)

from app.core import settings
from app.core.gunicorn import Application, get_app_options
from app.main import application


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
