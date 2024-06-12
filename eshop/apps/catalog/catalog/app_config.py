from typing import Type

from fastapi import APIRouter

from sqlalchemy.orm import DeclarativeBase

from framework.app_config import IAppConfig


class CatalogAppConfig(IAppConfig):

    name = 'catalog'

    @classmethod
    def get_api_router(cls) -> APIRouter:
        pass

    @classmethod
    def get_sqlalchemy_base(cls) -> Type[DeclarativeBase]:
        pass

    @classmethod
    def import_models(cls) -> None:
        pass

    @classmethod
    def import_http_views(cls) -> None:
        pass

    @classmethod
    def import_cqrs_handlers(cls) -> None:
        pass
