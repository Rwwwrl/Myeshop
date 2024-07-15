from __future__ import annotations

import abc
from typing import (
    ClassVar,
    Generic,
    TYPE_CHECKING,
    Tuple,
    Type,
    TypeVar,
    _GenericAlias as GenericType,
    final,
)

from attrs import define

from pydantic import BaseModel

if TYPE_CHECKING:
    from .handler import IRequestHandler

    from framework.cqrs.exceptions import PossibleExpectedError

    IRequestHandlerTypeVar = TypeVar('IRequestHandlerTypeVar', bound=IRequestHandler)

__all__ = (
    'IRequest',
    'ISyncRequest',
    'IAsyncRequest',
    'BaseRequest',
    'BaseSyncRequest',
    'BaseAsyncRequest',
)

RequestResponseType = TypeVar('RequestResponseType')

# TODO:
# attrs используется только потому что в pydantic есть проблема (https://github.com/pydantic/pydantic/issues/8410),
# которая не дает также красиво получать QueryResponseType из дженерика


class IRequest(abc.ABC):
    @abc.abstractclassmethod
    def handler(cls, handler_cls: Type[IRequestHandlerTypeVar]) -> Type[IRequestHandlerTypeVar]:
        raise NotImplementedError


class ISyncRequest(IRequest, Generic[RequestResponseType], abc.ABC):
    @property
    @classmethod
    @abc.abstractmethod
    def __possible_exceptions__() -> Tuple[Type[PossibleExpectedError]]:
        raise NotImplementedError

    @classmethod
    @abc.abstractmethod
    def __response_type__(cls) -> Type[RequestResponseType]:
        raise NotImplementedError


class IAsyncRequest(IRequest):
    pass


class BaseRequest(IRequest):
    @final
    @classmethod
    def handler(cls, handler_cls: Type[IRequestHandlerTypeVar]) -> Type[IRequestHandlerTypeVar]:
        from framework.cqrs.registry import get_registry

        get_registry().register(request_cls=cls, request_handler_cls=handler_cls)

        return handler_cls


@define
class BaseSyncRequest(ISyncRequest[RequestResponseType], BaseRequest):

    __possible_exceptions__: ClassVar[Tuple[Type[PossibleExpectedError]]] = tuple()

    @final
    @classmethod
    def __response_type__(cls) -> Type[RequestResponseType]:
        for base in cls.__orig_bases__:
            if type(base) is GenericType and base.__args__:
                return base.__args__[0]


class BaseAsyncRequest(IAsyncRequest, BaseRequest, BaseModel, frozen=True):
    pass
