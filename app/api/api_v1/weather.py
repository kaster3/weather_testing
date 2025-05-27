from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import APIRouter, Request, status
from pydantic import BaseModel

from app.core.use_cases.city import GetCitiesByPrefix, GetCityStats
from app.core.use_cases.user_city import (
    CreateUserCityInteractor,
    GetLastSearchInteractor,
    GetWeatherInteractor,
)

router = APIRouter(tags=["Weather"])


class WeatherRequest(BaseModel):
    city: str


class LastSearchedCityResponse(BaseModel):
    name: str | None


class CityBase(BaseModel):
    name: str


@router.get(
    "/tips",
    response_model=list[CityBase | None],
    status_code=status.HTTP_200_OK,
    description="City suggestions based on the user's input prefix",
)
@inject
async def get_tips(
    city_prefix: str,
    interactor: FromDishka[GetCitiesByPrefix],
):
    return await interactor(city_prefix=city_prefix)


@router.get(
    "/last_search",
    response_model=LastSearchedCityResponse,
    status_code=status.HTTP_200_OK,
)
@inject
async def get_last_search(
    request: Request,
    interactor: FromDishka[GetLastSearchInteractor],
):
    res = await interactor(request=request)
    if res is None:
        return LastSearchedCityResponse(name=None)
    return res


@router.get(
    "/stats",
    response_model=int,
    status_code=status.HTTP_200_OK,
    description="Number of times a specific city was searched",
)
@inject
async def get_city_stats(
    city_name: str,
    interactor: FromDishka[GetCityStats],
):
    return await interactor(city_name=city_name)


@router.post("/weather")
@inject
async def get_weather(
    request: Request,
    data: WeatherRequest,
    create_user_city_interactor: FromDishka[CreateUserCityInteractor],
    weather_interactor: FromDishka[GetWeatherInteractor],
):
    city_name, data_weather = await weather_interactor(data=data)
    await create_user_city_interactor(city_name=city_name, request=request)

    return {
        "city": city_name,
        "weather": data_weather,
    }
