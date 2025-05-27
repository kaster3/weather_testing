import logging
from abc import abstractmethod
from datetime import datetime
from typing import Callable, Protocol

from sqlalchemy import delete

from app.core.database import AnonymousUser
from app.core.repositories.base import Repository

log = logging.getLogger(__name__)


class CookieRepository(Protocol):
    @abstractmethod
    async def create_anonymous_user(self, user_id: str) -> None:
        raise NotImplementedError

    @abstractmethod
    async def delete_anonymous_users(self, older_than: datetime) -> None:
        raise NotImplementedError


class ICookieRepository(Repository):
    async def create_anonymous_user(self, user_id: str) -> None:
        user = AnonymousUser(id=user_id)
        self.session.add(user)
        await self.session.commit()
        log.info("New cookie: '%s' is created", user_id)

    async def delete_anonymous_users(self, older_than: datetime) -> Callable[[], int]:
        stmt = delete(AnonymousUser).where(AnonymousUser.created_at < older_than)
        result = await self.session.execute(stmt)
        await self.session.commit()
        return result.rowcount
