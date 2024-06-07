from __future__ import annotations

import abc
from typing import (
    Generic,
    Optional,
    TYPE_CHECKING,
    Type,
    TypeVar,
    _GenericAlias as GenericType,
)

import attrs

from ..cqrs_bus import CQRSBusSingletoneFactory, ICQRSBus

if TYPE_CHECKING:
    from .handler import ICommandHandler

CommandResponseType = TypeVar('CommandResponseType')

# TODO:
# attrs используется только потому что в pydantic есть проблема (https://github.com/pydantic/pydantic/issues/8410),
# которая не дает также красиво получать QueryResponseType из дженерика


@attrs.define
class ICommand(Generic[CommandResponseType], abc.ABC):

    # более красивое решение - указывать тип ответа через Generic, но
    # с pydantic моделью это пока что невозможно.

    @abc.abstractmethod
    def execute(self, bus: Optional[ICQRSBus] = None) -> CommandResponseType:
        raise NotImplementedError

    @abc.abstractclassmethod
    def handler(cls, handler: ICommandHandler) -> ICommandHandler:
        raise NotImplementedError

    @classmethod
    def __response_type__(cls) -> Type[CommandResponseType]:
        for base in cls.__orig_bases__:
            if type(base) is GenericType and base.__args__:
                return base.__args__[0]


@attrs.define
class Command(ICommand[CommandResponseType]):
    def execute(self, bus: Optional[ICQRSBus] = None) -> CommandResponseType:
        if not bus:
            bus = CQRSBusSingletoneFactory.create()

        return bus.fetch(query=self)

    @classmethod
    def handler(cls, handler_cls: Type[ICommandHandler]) -> Type[ICommandHandler]:
        from framework.cqrs.registry import registry

        registry.register(cls, handler_cls)

        return handler_cls
