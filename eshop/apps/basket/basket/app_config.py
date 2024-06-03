from typing import Type

from fastapi import APIRouter

from sqlalchemy.orm import DeclarativeBase

from framework.app_config import IAppConfig


class BasketAppConfig(IAppConfig):

    name = 'basket'

    @classmethod
    def get_api_router(cls) -> APIRouter:
        raise NotImplementedError

    @classmethod
    def get_sqlalchemy_base(cls) -> Type[DeclarativeBase]:
        from .domain.models.base import Base

        return Base

    @classmethod
    def import_models(cls) -> None:
        exec('from .domain.models import *')

    @classmethod
    def import_http_views(cls) -> None:
        raise NotImplementedError

    @classmethod
    def import_cqrs_handlers(cls) -> None:
        raise NotImplementedError
