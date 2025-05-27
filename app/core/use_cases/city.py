import logging

from app.core.database import City
from app.core.repositories.city import CityRepository

log = logging.getLogger(__name__)


class BaseCityInteractor:
    def __init__(self, city_repository: CityRepository) -> None:
        self.city_repository = city_repository


class CreateCityInteractor(BaseCityInteractor):
    async def __call__(self, city_name: str) -> None:
        city = await self.city_repository.create_city(name=city_name)
        log.info("New city: '%s' is created", city.name)
        await self.city_repository.increase_search(city=city)
        log.info("Increased amount of searching by 1. %s total %d", city.name, city.search_count)


class GetCityStats(BaseCityInteractor):
    async def __call__(self, city_name: str) -> int:
        city = await self.city_repository.get_city_by_name(name=city_name)
        return int(city.search_count) if city else 0


class GetCitiesByPrefix(BaseCityInteractor):
    async def __call__(self, city_prefix: str) -> list[City | None]:
        cities = await self.city_repository.get_cities_by_prefix(city_prefix=city_prefix)
        return cities
