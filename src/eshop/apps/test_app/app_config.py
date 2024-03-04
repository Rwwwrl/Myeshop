from eshop.framework.fastapi.app_config import AppConfig

from fastapi import APIRouter


class TestAppConfig(AppConfig):

    name = 'test_app'

    @classmethod
    def get_api_router(cls) -> APIRouter:
        from .api_router import api_router

        return api_router

    @classmethod
    def import_models(cls) -> None:
        exec('from .models import *')

    @classmethod
    def import_views(cls) -> None:
        exec('from .views import *')
