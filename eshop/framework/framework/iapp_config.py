import abc
from typing import ClassVar, Optional, Type

from fastapi import APIRouter

from sqlalchemy.orm import DeclarativeBase


class IAppConfig:

    name: ClassVar[str]

    @property
    @abc.abstractmethod
    def name(self) -> str:
        raise NotImplementedError

    @abc.abstractclassmethod
    def get_api_router(cls) -> Optional[APIRouter]:
        raise NotImplementedError

    @classmethod
    def get_sqlalchemy_base(cls) -> Optional[Type[DeclarativeBase]]:
        raise NotImplementedError

    @abc.abstractclassmethod
    def import_models(cls) -> None:
        raise NotImplementedError

    @abc.abstractclassmethod
    def import_http_views(cls) -> None:
        raise NotImplementedError

    @abc.abstractclassmethod
    def import_cqrs_handlers(cls) -> None:
        raise NotImplementedError
