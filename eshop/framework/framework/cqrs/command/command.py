from __future__ import annotations

import abc
from typing import (
    Optional,
    TYPE_CHECKING,
    Type,
    TypeVar,
    final,
)

import attrs

from ..request import BaseRequest, IRequest

if TYPE_CHECKING:
    from .handler import ICommandHandler
    from ..cqrs_bus import ICQRSBus

CommandResponseType = TypeVar('CommandResponseType')


@attrs.define
class ICommand(IRequest[CommandResponseType], abc.ABC):

    # более красивое решение - указывать тип ответа через Generic, но
    # с pydantic моделью это пока что невозможно.

    @abc.abstractmethod
    def execute(self, bus: Optional[ICQRSBus] = None) -> CommandResponseType:
        raise NotImplementedError


@attrs.define
class Command(ICommand[CommandResponseType], BaseRequest):
    @final
    def execute(self, bus: Optional[ICQRSBus] = None) -> CommandResponseType:
        from ..cqrs_bus import CQRSBusSingletoneFactory

        if not bus:
            bus = CQRSBusSingletoneFactory.create()

        return bus.fetch(query=self)

    @classmethod
    def handler(cls, handler_cls: Type[ICommandHandler]) -> Type[ICommandHandler]:
        from ..registry import get_registry

        get_registry().register(request_cls=cls, request_handler_cls=handler_cls)

        return handler_cls
