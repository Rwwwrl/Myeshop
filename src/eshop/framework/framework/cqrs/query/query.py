import abc
from typing import ClassVar, Type, TypeVar

from pydantic import BaseModel

from ..cqrs_bus import CQRSBusSingletoneFactory

QueryResponse = TypeVar('QueryResponse')


class IQuery(BaseModel, abc.ABC, frozen=True):

    _response_type: ClassVar[Type[QueryResponse]]

    @abc.abstractmethod
    def fetch(self) -> QueryResponse:
        raise NotImplementedError

    @abc.abstractclassmethod
    def get_response_type(cls) -> Type[QueryResponse]:
        raise NotImplementedError


class Query(IQuery):
    def fetch(self) -> QueryResponse:
        bus = CQRSBusSingletoneFactory.create()
        return bus.fetch(query=self)

    @classmethod
    def get_response_type(cls) -> Type[QueryResponse]:
        return cls._response_type


def query(response_type: Type[QueryResponse]):
    # TODO приходится накидывать декоратор, а не получать response_type через genericи, т.к.
    # c pydantic.BaseModel это не работает
    # https://github.com/pydantic/pydantic/issues/8410

    def inner(query_cls: Type[IQuery]) -> Type[IQuery]:
        query_cls._response_type = response_type
        return query_cls

    return inner
