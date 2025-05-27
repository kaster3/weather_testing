import logging

import httpx
from fastapi import HTTPException, Request
from httpx import AsyncClient

from app.core import Settings
from app.core.database import City
from app.core.repositories.city import CityRepository
from app.core.repositories.user_city import UserCityRepository

log = logging.getLogger(__name__)


class BaseUserCityInteractor:
    def __init__(self, settings: Settings) -> None:
        self.settings = settings


class UserCityInteractor(BaseUserCityInteractor):
    def __init__(
        self,
        settings: Settings,
        city_repository: CityRepository,
        user_city_repository: UserCityRepository,
    ) -> None:
        super().__init__(settings)
        self.city_repository = city_repository
        self.user_city_repository = user_city_repository


class GetWeatherInteractor(BaseUserCityInteractor):
    async def __call__(self, data):
        async with httpx.AsyncClient(timeout=10) as client:
            geo_resp = await self._get_coordinates_by_name(data=data, client=client)
            geo_data = geo_resp.json()
            if not geo_data:
                raise HTTPException(status_code=404, detail="Город не найден")

            weather_resp = await self._get_weather_by_city_name(geo_data=geo_data, client=client)
            weather_data = weather_resp.json()
            weather = weather_data.get("current_weather", {})

            city_name = geo_data[0]["name"]

            return city_name, weather

    async def _get_coordinates_by_name(self, data, client: AsyncClient):
        input_city = data.city
        geo_resp = await client.get(
            self.settings.links.GEOCODER_API, params={"q": input_city, "format": "json", "limit": 1}
        )
        return geo_resp

    async def _get_weather_by_city_name(self, geo_data: dict, client: AsyncClient):
        lat = geo_data[0]["lat"]
        lon = geo_data[0]["lon"]

        weather_resp = await client.get(
            self.settings.links.WEATHER_API,
            params={"latitude": lat, "longitude": lon, "current_weather": True},
        )
        return weather_resp


class CreateUserCityInteractor(UserCityInteractor):
    async def __call__(self, request: Request, city_name: str) -> None:
        user_id = getattr(request.state, "user_id", None) or request.cookies.get(
            self.settings.cookie.key
        )
        city = await self.city_repository.get_city_by_name(name=city_name)

        if city is None:
            city = await self.city_repository.create_city(name=city_name)
            log.info("New city: '%s' is created", city.name)

        await self.user_city_repository.create_user_city(city_id=city.id, user_id=user_id)
        log.info("History successfully saved: user - %s city - %s", user_id, city.name)
        await self.city_repository.increase_search(city=city)
        log.info("Increased amount of searching by 1. %s total %d", city.name, city.search_count)


class GetLastSearchInteractor(UserCityInteractor):
    async def __call__(self, request: Request) -> City | None:
        user_id = getattr(request.state, "user_id", None) or request.cookies.get(
            self.settings.cookie.key
        )
        user_city = await self.user_city_repository.get_last_searched_city_by_user(user_id)
        if user_city is None:
            return None
        city = await self.city_repository.get_city_by_id(city_id=user_city.city_id)
        return city
