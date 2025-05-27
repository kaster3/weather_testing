import logging
from datetime import UTC, datetime, timedelta
from uuid import uuid4

from fastapi import Request

from app.core import Settings
from app.core.repositories.cookies import CookieRepository

log = logging.getLogger(__name__)


class BaseUserCookieInteractor:
    def __init__(
        self,
        cookie_repository: CookieRepository,
        settings: Settings,
    ) -> None:
        self.cookie_repository = cookie_repository
        self.settings = settings


class CreateUserCookieInteractor(BaseUserCookieInteractor):
    async def set_user_cookie_if_needed(self, request: Request) -> str:
        user_id = request.cookies.get(self.settings.cookie.key)
        if user_id:
            return user_id

        new_id = str(uuid4())
        await self.cookie_repository.create_anonymous_user(user_id=new_id)

        return new_id


class DeleteExpiredCookies(BaseUserCookieInteractor):
    async def __call__(self) -> None:
        expiration_time = datetime.now(UTC) - timedelta(seconds=self.settings.cookie.max_age)
        deleted_count = await self.cookie_repository.delete_anonymous_users(
            older_than=expiration_time
        )
        log.info("Deleted %d expired anonymous users", deleted_count)
