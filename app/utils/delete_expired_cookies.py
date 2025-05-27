import asyncio
import logging

from app.api.api_v1.middlewares.cookies import container
from app.core import Settings
from app.core.use_cases.user import DeleteExpiredCookies

log = logging.getLogger(__name__)


async def delete_expired_cookies() -> None:
    async with container() as requested_container:
        interactor = await requested_container.get(DeleteExpiredCookies)
        settings = await requested_container.get(Settings)

        while True:
            await asyncio.sleep(settings.cookie.max_age)
            try:
                await interactor()
                log.info("Expired cookies deleted.")
            except Exception as e:
                logging.exception("Error while deleting expired cookies: %s", e)
