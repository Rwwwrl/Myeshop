import abc
from typing import ClassVar

from fastapi import APIRouter


class AppConfig:

    name: ClassVar[str]

    @property
    @abc.abstractmethod
    def name(self) -> str:
        raise NotImplementedError

    @abc.abstractclassmethod
    def get_api_router(cls) -> APIRouter:
        raise NotImplementedError

    @abc.abstractclassmethod
    def import_models(cls) -> None:
        raise NotImplementedError

    @abc.abstractclassmethod
    def import_views(cls) -> None:
        raise NotImplementedError
