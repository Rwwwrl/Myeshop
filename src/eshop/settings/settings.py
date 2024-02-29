from contextlib import asynccontextmanager
from typing import List, Type

from apps.test_app.app_config import TestAppConfig

from fastapi import FastAPI

from framework.fastapi.app_config import AppConfig

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
