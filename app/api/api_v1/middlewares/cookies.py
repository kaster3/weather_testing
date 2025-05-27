import logging

from fastapi import Request, Response

from app.core import settings
from app.core.use_cases.user import CreateUserCookieInteractor
from app.ioc.init_container import init_async_container

log = logging.getLogger(__name__)


container = init_async_container(settings=settings)


async def set_anon_user_id_cookie(request: Request, call_next) -> Response:
    async with container() as request_container:
        interactor = await request_container.get(CreateUserCookieInteractor)
        user_id = await interactor.set_user_cookie_if_needed(request)

    request.state.user_id = user_id

    response = await call_next(request)

    if not request.cookies.get(settings.cookie.key):
        response.set_cookie(
            key=settings.cookie.key,
            value=user_id,
            httponly=settings.cookie.httponly,
            max_age=settings.cookie.max_age,
            secure=settings.cookie.secure,
            samesite=settings.cookie.same_site,
        )
        log.info("The cookie: '%s' is set", user_id)

    return response
