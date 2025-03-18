from typing import Literal

from pydantic import BaseModel, PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class ApiV1Prefix(BaseModel):
    prefix: str = "/v1"
    endpoint: str = "/endpoint"


class ApiPrefix(BaseModel):
    prefix: str = "/api"
    v1: ApiV1Prefix = ApiV1Prefix()


class LoggingConfig(BaseModel):
    log_level: Literal[
        "debug",
        "info",
        "warning",
        "error",
        "critical",
    ] = "info"
    log_format: str


class DataBase(BaseModel):
    url: PostgresDsn
    echo: bool
    echo_pool: bool
    pool_size: int
    max_overflow: int


class RunConfig(BaseModel):
    app: str
    host: str
    port: int
    reload: bool
    workers: int


class GunicornConfig(BaseModel):
    host: str
    port: int
    workers: int
    timeout: int


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=(".template.env", ".env"),
        case_sensitive=False,
        env_nested_delimiter="__",
        env_prefix="FASTAPI__",
    )
    conf: RunConfig
    gunicorn: GunicornConfig
    db: DataBase
    logging: LoggingConfig
    api: ApiPrefix = ApiPrefix()
