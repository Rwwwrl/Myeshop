from __future__ import annotations

import abc
from typing import (Generic, TYPE_CHECKING, Type, TypeVar, _GenericAlias as GenericType, final)

from attrs import define

if TYPE_CHECKING:
    from .handler import IRequestHandler

RequestResponseType = TypeVar('RequestResponseType')

# TODO:
# attrs используется только потому что в pydantic есть проблема (https://github.com/pydantic/pydantic/issues/8410),
# которая не дает также красиво получать QueryResponseType из дженерика


@define
class IRequest(Generic[RequestResponseType], abc.ABC):
    @abc.abstractclassmethod
    def handler(cls, handler_cls: IRequestHandler) -> Type[IRequestHandler]:
        raise NotImplementedError

    @classmethod
    def __response_type__(cls) -> Type[RequestResponseType]:
        raise NotImplementedError


@define
class BaseRequest(IRequest[RequestResponseType]):
    @final
    @classmethod
    def __response_type__(cls) -> Type[RequestResponseType]:
        for base in cls.__orig_bases__:
            if type(base) is GenericType and base.__args__:
                return base.__args__[0]
