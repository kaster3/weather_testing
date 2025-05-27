import logging
from abc import abstractmethod
from typing import Protocol

from sqlalchemy import select

from app.core.database import UserCityHistory
from app.core.repositories.base import Repository

log = logging.getLogger(__name__)


class UserCityRepository(Protocol):
    @abstractmethod
    async def get_last_searched_city_by_user(self, user_id: str) -> UserCityHistory | None:
        raise NotImplementedError

    @abstractmethod
    async def create_user_city(self, city_id: int, user_id: str) -> UserCityHistory:
        raise NotImplementedError


class IUserCityRepository(Repository):
    async def get_last_searched_city_by_user(self, user_id: str) -> UserCityHistory | None:
        stmt = (
            select(UserCityHistory)
            .where(UserCityHistory.user_id == user_id)
            .order_by(UserCityHistory.created_at.desc())
            .limit(1)
        )
        return await self.session.scalar(stmt)

    async def create_user_city(self, city_id: int, user_id: str) -> UserCityHistory:
        user_city = UserCityHistory(city_id=city_id, user_id=user_id)
        self.session.add(user_city)
        await self.session.commit()
        return user_city
