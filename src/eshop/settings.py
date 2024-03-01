from contextlib import asynccontextmanager
from typing import List, Type

import dotenv

from eshop.apps.test_app.app_config import TestAppConfig
from eshop.framework.fastapi.app_config import AppConfig

from fastapi import FastAPI

import pydantic_settings

dotenv.load_dotenv('.env')

INSTALLED_APPS: List[Type[AppConfig]] = [
    TestAppConfig,
]


def import_models() -> None:
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


class BaseSettings(pydantic_settings.BaseSettings):

    model_config = pydantic_settings.SettingsConfigDict(env_file='.env')


class DatabaseSettings(BaseSettings, frozen=True):

    db_name: str
    db_host: str
    db_user_login: str
    db_user_password: str


class Settings(BaseSettings, frozen=True):

    db: DatabaseSettings = DatabaseSettings()


SETTINGS = Settings()
