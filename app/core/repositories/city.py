import logging
from abc import abstractmethod
from typing import Protocol

from sqlalchemy import select

from app.core.database import City
from app.core.repositories.base import Repository

log = logging.getLogger(__name__)


class CityRepository(Protocol):
    @abstractmethod
    async def get_city_by_id(self, city_id: int) -> City | None:
        raise NotImplementedError

    @abstractmethod
    async def get_city_by_name(self, name: str) -> City | None:
        raise NotImplementedError

    @abstractmethod
    async def get_cities_by_prefix(self, city_prefix: str) -> list[City | None]:
        raise NotImplementedError

    @abstractmethod
    async def create_city(self, name: str) -> City:
        raise NotImplementedError

    @abstractmethod
    async def increase_search(self, city: City) -> None:
        raise NotImplementedError


class ICityRepository(Repository):
    async def get_city_by_id(self, city_id: int) -> City | None:
        return await self.session.get(City, city_id)

    async def get_city_by_name(self, name: str) -> City | None:
        stmt = select(City).where(City.name == name)
        city = await self.session.scalar(stmt)
        return city

    async def get_cities_by_prefix(self, city_prefix: str) -> list[City | None]:
        stmt = select(City).where(City.name.ilike(f"{city_prefix}%")).order_by(City.name).limit(10)
        cities = await self.session.scalars(stmt)
        return list(cities)

    async def create_city(self, name: str) -> City:
        city = City(name=name)
        self.session.add(city)
        await self.session.commit()
        return city

    async def increase_search(self, city: City) -> None:
        city.search_count += 1
        self.session.add(city)
        await self.session.commit()
