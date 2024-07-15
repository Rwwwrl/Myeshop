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
    'IEvent',
    'Event',
)


class IEvent(IAsyncRequest, abc.ABC):
    @abc.abstractmethod
    def publish(self, bus: Optional[ICQRSBus] = None) -> None:
        raise NotImplementedError


class Event(IEvent, BaseAsyncRequest):
    @final
    def publish(self, bus: Optional[ICQRSBus] = None) -> None:
        from ..cqrs_bus import CQRSBusSingletoneFactory

        if not bus:
            bus = CQRSBusSingletoneFactory.create()

        return bus.publish(query=self)
