from __future__ import annotations

import abc
from typing import (
    Optional,
    TYPE_CHECKING,
    Type,
    TypeVar,
    final,
)

from attrs import define

from ..request import BaseRequest, IRequest

QueryResponseType = TypeVar('QueryResponseType')

if TYPE_CHECKING:
    from .handler import IQueryHandler
    from ..cqrs_bus import ICQRSBus


@define
class IQuery(IRequest[QueryResponseType], abc.ABC):
    @abc.abstractmethod
    def fetch(self, bus: Optional[ICQRSBus] = None) -> QueryResponseType:
        raise NotImplementedError


@define
class Query(IQuery[QueryResponseType], BaseRequest):
    @final
    def fetch(self, bus: Optional[ICQRSBus] = None) -> QueryResponseType:
        from ..cqrs_bus import CQRSBusSingletoneFactory

        if not bus:
            bus = CQRSBusSingletoneFactory.create()

        return bus.fetch(query=self)

    @final
    @classmethod
    def handler(cls, handler_cls: Type[IQueryHandler]) -> Type[IQueryHandler]:
        from ..registry import get_registry

        get_registry().register(request_cls=cls, request_handler_cls=handler_cls)

        return handler_cls
