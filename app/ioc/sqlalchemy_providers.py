from typing import AsyncGenerator

from dishka import Provider, Scope, from_context, provide
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database.db_helper import DataBaseHelper
from app.core.repositories.city import CityRepository, ICityRepository
from app.core.repositories.cookies import CookieRepository, ICookieRepository
from app.core.repositories.user_city import IUserCityRepository, UserCityRepository
from app.core.settings import Settings
from app.core.use_cases.city import CreateCityInteractor, GetCitiesByPrefix, GetCityStats
from app.core.use_cases.user import CreateUserCookieInteractor, DeleteExpiredCookies
from app.core.use_cases.user_city import (
    CreateUserCityInteractor,
    GetLastSearchInteractor,
    GetWeatherInteractor,
)


class SQLAlchemyProvider(Provider):
    scope = Scope.APP
    settings = from_context(Settings)

    @provide
    async def get_database_helper(
        self,
        settings: Settings,
    ) -> DataBaseHelper:
        return DataBaseHelper(
            url=str(settings.db.url),
            echo=settings.db.echo,
            echo_pool=settings.db.echo_pool,
            pool_size=settings.db.pool_size,
            max_overflow=settings.db.max_overflow,
        )

    @provide(scope=Scope.REQUEST)
    async def get_async_session(
        self,
        database_helper: DataBaseHelper,
    ) -> AsyncGenerator[AsyncSession, None]:
        async with database_helper.session_factory() as session:
            yield session


class UserProvider(Provider):
    scope = Scope.REQUEST

    cookie_repository = provide(ICookieRepository, provides=CookieRepository)
    create_user = provide(CreateUserCookieInteractor)
    delete_expired_cookies = provide(DeleteExpiredCookies)

    city_repository = provide(ICityRepository, provides=CityRepository)
    create_city = provide(CreateCityInteractor)
    city_stats = provide(GetCityStats)
    cities_prefix = provide(GetCitiesByPrefix)

    user_city_repository = provide(IUserCityRepository, provides=UserCityRepository)
    create_user_city = provide(CreateUserCityInteractor)
    last_searched = provide(GetLastSearchInteractor)

    weather = provide(GetWeatherInteractor)
