import abc
from typing import Generic, Optional, TypeVar

from pydantic import BaseModel

from ..cqrs_bus import CQRSBus, ICQRSBus

QueryResponse = TypeVar('QueryResponse')


class IQuery(Generic[QueryResponse], abc.ABC):
    @abc.abstractmethod
    def fetch(self) -> QueryResponse:
        raise NotImplementedError


class Query(IQuery[QueryResponse], BaseModel, frozen=True):
    def fetch(self, bus: Optional[ICQRSBus] = None) -> QueryResponse:
        if not bus:
            bus = CQRSBus()

        return bus.fetch(query=self)
