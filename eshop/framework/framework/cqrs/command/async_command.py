from __future__ import annotations

import abc
from typing import (
    Optional,
    TYPE_CHECKING,
    final,
)

from ..request import BaseAsyncRequest, IAsyncRequest

if TYPE_CHECKING:
    from ..cqrs_bus import ICQRSBus

__all__ = (
    'IAsyncCommand',
    'AsyncCommand',
)


class IAsyncCommand(IAsyncRequest, abc.ABC):
    @abc.abstractmethod
    def execute(self, bus: Optional[ICQRSBus] = None) -> None:
        raise NotImplementedError


class AsyncCommand(IAsyncCommand, BaseAsyncRequest):
    @final
    def execute(self, bus: Optional[ICQRSBus] = None) -> None:
        from eshop.dependency_container import dependency_container

        if not bus:
            bus = dependency_container.cqrs_bus_factory()

        bus.async_execute(command=self)
