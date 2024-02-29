from fastapi import APIRouter

from framework.fastapi.app_config import AppConfig


class TestAppConfig(AppConfig):

    name = 'test_app'

    @classmethod
    def get_api_router(cls) -> APIRouter:
        from .api_router import api_router

        return api_router

    @classmethod
    def import_models(cls) -> None:
        pass

    @classmethod
    def import_views(cls) -> None:
        exec('from .views import *')
