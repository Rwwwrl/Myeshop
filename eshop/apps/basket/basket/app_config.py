from typing import Optional, Type

from fastapi import APIRouter

from sqlalchemy.orm import DeclarativeBase

from framework.app_config import IAppConfig


class BasketAppConfig(IAppConfig):

    name = 'basket'

    @classmethod
    def get_api_router(cls) -> Optional[APIRouter]:
        return None

    @classmethod
    def get_sqlalchemy_base(cls) -> Optional[Type[DeclarativeBase]]:
        from .domain.models.base import Base

        return Base

    @classmethod
    def import_models(cls) -> None:
        from .domain import models    # noqa

    @classmethod
    def import_http_views(cls) -> None:
        pass

    @classmethod
    def import_cqrs_handlers(cls) -> None:
        from .views import cqrs    # noqa
