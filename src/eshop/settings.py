from contextlib import asynccontextmanager
from datetime import timedelta
from typing import List, Type

import decouple

import dotenv

from fastapi import FastAPI

import pydantic

from sqlalchemy import URL
from sqlalchemy.engine import create_engine
from sqlalchemy.orm import DeclarativeBase as SqlalchemyDeclarativeBase

from eshop.apps.test_app.app_config import TestAppConfig
from eshop.apps.user_identity.app_config import UserIdentityAppConfig
from eshop.framework.fastapi.app_config import AppConfig

dotenv.load_dotenv('.env')

INSTALLED_APPS: List[Type[AppConfig]] = [
    TestAppConfig,
    UserIdentityAppConfig,
]


def import_all_models_in_project() -> None:
    for app_config in INSTALLED_APPS:
        app_config.import_models()


def import_views() -> None:
    for app_config in INSTALLED_APPS:
        app_config.import_views()


def include_routes() -> None:
    for app_config in INSTALLED_APPS:
        MAIN_APP.include_router(app_config.get_api_router())


@asynccontextmanager
async def lifespan(app: FastAPI):
    import_views()
    include_routes()
    yield


MAIN_APP = FastAPI(lifespan=lifespan)


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


class SQLALCHEMY_BASE(SqlalchemyDeclarativeBase):
    pass


SQLALCHEMY_ENGINE = create_engine(url=DB_URL)
