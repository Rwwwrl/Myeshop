from typing import Type

from fastapi import APIRouter

from sqlalchemy.orm import DeclarativeBase

from framework.fastapi.app_config import IAppConfig


class BasketAppConfig(IAppConfig):

    name = 'basket'

    @classmethod
    def get_api_router(cls) -> APIRouter:
        raise NotImplementedError

    @classmethod
    def get_sqlalchemy_base(cls) -> Type[DeclarativeBase]:
        raise NotImplementedError

    @classmethod
    def import_models(cls) -> None:
        raise NotImplementedError

    @classmethod
    def import_http_views(cls) -> None:
        raise NotImplementedError

    @classmethod
    def import_cqrs_handlers(cls) -> None:
        raise NotImplementedError
