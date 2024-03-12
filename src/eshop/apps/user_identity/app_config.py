from fastapi import APIRouter

from eshop.framework.fastapi.app_config import AppConfig


class UserIdentityAppConfig(AppConfig):

    name = 'user_identity'

    @classmethod
    def get_api_router(cls) -> APIRouter:
        from .api_router import api_router

        return api_router

    @classmethod
    def import_models(cls) -> None:
        exec('from .domain.models import *')

    @classmethod
    def import_views(cls) -> None:
        exec('from .views import *')
