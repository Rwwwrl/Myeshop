import abc
from typing import Generic, TypeVar

from pydantic import BaseModel

from ..cqrs_bus import CQRSBusSingletoneFactory

QueryResponse = TypeVar('QueryResponse')


class IQuery(BaseModel, Generic[QueryResponse], abc.ABC, frozen=True):
    @abc.abstractmethod
    def fetch(self) -> QueryResponse:
        raise NotImplementedError


class Query(IQuery[QueryResponse]):
    def fetch(self) -> QueryResponse:
        bus = CQRSBusSingletoneFactory.create()
        return bus.fetch(query=self)
