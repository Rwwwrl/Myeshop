from fastapi import APIRouter

from eshop.framework.fastapi.app_config import IAppConfig


class TestAppConfig(IAppConfig):

    name = 'test_app'

    @classmethod
    def get_api_router(cls) -> APIRouter:
        from .api_router import api_router

        return api_router

    @classmethod
    def import_models(cls) -> None:
        exec('from .models import *')

    @classmethod
    def import_http_views(cls) -> None:
        exec('from .views import *')

    def import_cqrs_handlers(cls) -> None:
        pass
