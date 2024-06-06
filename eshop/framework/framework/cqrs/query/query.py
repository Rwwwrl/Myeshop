import abc
from typing import Generic, Type, TypeVar, _GenericAlias as GenericType

import attrs

from ..cqrs_bus import CQRSBusSingletoneFactory

QueryResponseType = TypeVar('QueryResponseType')

# TODO:
# attrs используется только потому что в pydantic есть проблема (https://github.com/pydantic/pydantic/issues/8410),
# которая не дает также красиво получать QueryResponseType из дженерика


@attrs.define
class IQuery(Generic[QueryResponseType], abc.ABC):

    # более красивое решение - указывать тип ответа через Generic, но
    # с pydantic моделью это пока что невозможно.

    @abc.abstractmethod
    def fetch(self) -> QueryResponseType:
        raise NotImplementedError

    @classmethod
    def __response_type__(cls) -> Type[QueryResponseType]:
        for base in cls.__orig_bases__:
            if type(base) is GenericType and base.__args__:
                return base.__args__[0]


@attrs.define
class Query(IQuery[QueryResponseType]):
    def fetch(self) -> QueryResponseType:
        bus = CQRSBusSingletoneFactory.create()
        return bus.fetch(query=self)
