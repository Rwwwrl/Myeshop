from contextlib import asynccontextmanager
from datetime import timedelta
from pathlib import Path
from typing import List, Type

from fastapi import FastAPI
from fastapi.security import OAuth2PasswordBearer

import pydantic

import pydantic_settings

from sqlalchemy import URL
from sqlalchemy.engine import create_engine

from test_app.app_config import TestAppConfig

from api_mediator.app_config import ApiMediatorAppConfig

from basket.app_config import BasketAppConfig

from catalog.app_config import CatalogAppConfig

from framework.app_config import IAppConfig

from user_identity.app_config import UserIdentityAppConfig

INSTALLED_APPS: List[Type[IAppConfig]] = [
    TestAppConfig,
    UserIdentityAppConfig,
    BasketAppConfig,
    CatalogAppConfig,
]


def init_logging() -> None:
    import yaml
    import logging
    from logging import config as logging_config

    LOGGING_CONFIG_YAML_FILENAME = 'logging_config.yaml'
    LOGGIN_CONFIG_YAML_FILE_PATH = BASE_DIR / 'settings' / LOGGING_CONFIG_YAML_FILENAME

    with open(LOGGIN_CONFIG_YAML_FILE_PATH, 'r') as file:
        config = yaml.safe_load(file.read())

    logging_config.dictConfig(config)

    logger = logging.getLogger('settings')
    logger.info('%s was used to configure logging', LOGGING_CONFIG_YAML_FILENAME)


def import_http_views() -> None:
    for app_config in INSTALLED_APPS:
        app_config.import_http_views()

    ApiMediatorAppConfig.import_http_views()


def include_routes() -> None:
    for app_config in INSTALLED_APPS:
        router = app_config.get_api_router()
        if router:
            MAIN_APP.include_router(router)

    for router in ApiMediatorAppConfig.get_api_routers():
        MAIN_APP.include_router(router)


def import_cqrs_controllers() -> None:
    for app_config in INSTALLED_APPS:
        app_config.import_cqrs_handlers()


@asynccontextmanager
async def lifespan(app: FastAPI):
    import_http_views()
    include_routes()
    import_cqrs_controllers()
    init_logging()
    yield


MAIN_APP = FastAPI(lifespan=lifespan)

BASE_DIR = Path(__file__).resolve().parent.parent


class PostgresSettings(pydantic.BaseModel):
    name: str
    host: str
    port: int
    login: str
    password: str


class UserIdentityServiceSettings(pydantic.BaseModel):

    secret: str
    token_life_time_duration: timedelta = timedelta(minutes=5)


class Settings(pydantic_settings.BaseSettings):
    model_config = pydantic_settings.SettingsConfigDict(
        case_sensitive=False,
        env_nested_delimiter='__',
    )

    postgres: PostgresSettings
    user_identity_service: UserIdentityServiceSettings


SETTINGS = Settings()

DB_URL = URL.create(
    drivername='postgresql',
    database=SETTINGS.postgres.name,
    host=SETTINGS.postgres.host,
    port=SETTINGS.postgres.port,
    username=SETTINGS.postgres.login,
    password=SETTINGS.postgres.password,
)

SQLALCHEMY_ENGINE = create_engine(url=DB_URL)

OAUTH2_SCHEME = OAuth2PasswordBearer(tokenUrl='user_identity/token/')
