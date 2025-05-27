from pathlib import Path
from typing import Literal

from pydantic import BaseModel, PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_PATH = Path(__file__).resolve().parents[2]
TEMPLATE_ENV_PATH = BASE_PATH / ".template.env"
ENV_PATH = BASE_PATH / ".env"


class ApiV1Prefix(BaseModel):
    prefix: str = "/v1"
    endpoint: str = "/endpoint"


class ApiPrefix(BaseModel):
    prefix: str = "/api"
    v1: ApiV1Prefix = ApiV1Prefix()


class LoggingConfig(BaseModel):
    log_level: Literal[
        "DEBUG",
        "INFO",
        "WARNING",
        "ERROR",
        "CRITICAL",
    ] = "INFO"
    log_format: str


class DataBase(BaseModel):
    url: PostgresDsn
    echo: bool
    echo_pool: bool
    pool_size: int
    max_overflow: int


class GunicornConfig(BaseModel):
    host: str
    port: int
    workers: int
    timeout: int


class CookieConfig(BaseModel):
    key: str = "anon_user_id"
    httponly: bool = True
    max_age: int = 86400
    secure: bool = False
    same_site: Literal["lax", "strict", "none"] | None = "lax"


class Links(BaseModel):
    WEATHER_API: str = "https://api.open-meteo.com/v1/forecast"
    GEOCODER_API: str = "https://nominatim.openstreetmap.org/search"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=(TEMPLATE_ENV_PATH, ENV_PATH),
        case_sensitive=False,
        env_nested_delimiter="__",
        env_prefix="FASTAPI__",
    )
    gunicorn: GunicornConfig
    db: DataBase
    logging: LoggingConfig
    api: ApiPrefix = ApiPrefix()
    cookie: CookieConfig = CookieConfig()
    links: Links = Links()


settings = Settings()
