from contextlib import asynccontextmanager
from typing import List, Type

import dotenv

from eshop.apps.test_app.app_config import TestAppConfig
from eshop.framework.fastapi.app_config import AppConfig

from fastapi import FastAPI

import pydantic_settings

from sqlalchemy import URL
from sqlalchemy.engine import create_engine
from sqlalchemy.orm import DeclarativeBase as SqlalchemyDeclarativeBase

dotenv.load_dotenv('.env')

INSTALLED_APPS: List[Type[AppConfig]] = [
    TestAppConfig,
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


class BaseSettings(pydantic_settings.BaseSettings, frozen=True):

    model_config = pydantic_settings.SettingsConfigDict(env_file='.env')


class DatabaseSettings(BaseSettings):

    db_name: str
    db_host: str
    db_user_login: str
    db_user_password: str


class Settings(BaseSettings):

    db: DatabaseSettings = DatabaseSettings()


SETTINGS = Settings()

DB_URL = URL.create(
    drivername='postgresql',
    database=SETTINGS.db.db_name,
    host=SETTINGS.db.db_host,
    username=SETTINGS.db.db_user_login,
    password=SETTINGS.db.db_user_password,
)


class SQLALCHEMY_BASE(SqlalchemyDeclarativeBase):
    pass


SQLALCHEMY_ENGINE = create_engine(url=DB_URL)
