from contextlib import asynccontextmanager
from datetime import timedelta
from pathlib import Path
from typing import List, Type

import decouple

from fastapi import FastAPI
from fastapi.security import OAuth2PasswordBearer

import pydantic

from sqlalchemy import URL
from sqlalchemy.engine import create_engine

from test_app.app_config import TestAppConfig

from framework.fastapi.app_config import IAppConfig

from user_identity.app_config import UserIdentityAppConfig

INSTALLED_APPS: List[Type[IAppConfig]] = [
    TestAppConfig,
    UserIdentityAppConfig,
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


def include_routes() -> None:
    for app_config in INSTALLED_APPS:
        MAIN_APP.include_router(app_config.get_api_router())


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


class BaseSettings(pydantic.BaseModel, frozen=True):
    pass


class DatabaseSettings(BaseSettings):

    name: str = decouple.config('DB_NAME')
    host: str = decouple.config('DB_HOST')
    login: str = decouple.config('DB_USER_LOGIN')
    password: str = decouple.config('DB_USER_PASSWORD')


class UserIdentityServiceSettings(BaseSettings):

    secret: str = decouple.config('USER_IDENTITY_SERVICE_SECRET')
    token_life_time_duration: timedelta = timedelta(minutes=5)


class Settings(BaseSettings):

    db: DatabaseSettings = DatabaseSettings()
    user_identity_service_settings: UserIdentityServiceSettings = UserIdentityServiceSettings()


SETTINGS = Settings()

DB_URL = URL.create(
    drivername='postgresql',
    database=SETTINGS.db.name,
    host=SETTINGS.db.host,
    username=SETTINGS.db.login,
    password=SETTINGS.db.password,
)

SQLALCHEMY_ENGINE = create_engine(url=DB_URL)

OAUTH2_SCHEME = OAuth2PasswordBearer(tokenUrl='user_identity/token/')
