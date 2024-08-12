from __future__ import annotations

import abc
from typing import (
    Optional,
    TYPE_CHECKING,
    TypeVar,
    final,
)

from attrs import define

from ..request import BaseSyncRequest, ISyncRequest

if TYPE_CHECKING:
    from ..cqrs_bus import ICQRSBus

CommandResponseType = TypeVar('CommandResponseType')

__all__ = (
    'ISyncCommand',
    'SyncCommand',
)


@define
class ISyncCommand(ISyncRequest[CommandResponseType], abc.ABC):
    @abc.abstractmethod
    def execute(self, bus: Optional[ICQRSBus] = None) -> CommandResponseType:
        raise NotImplementedError


@define
class SyncCommand(ISyncCommand[CommandResponseType], BaseSyncRequest):
    @final
    def execute(self, bus: Optional[ICQRSBus] = None) -> CommandResponseType:
        from eshop.dependency_container import dependency_container

        if not bus:
            bus = dependency_container.cqrs_bus_factory()

        return bus.sync_execute(command=self)
