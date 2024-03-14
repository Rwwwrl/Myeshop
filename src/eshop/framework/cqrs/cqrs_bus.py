import abc
from typing import TYPE_CHECKING

from .query.registry import query_registry

if TYPE_CHECKING:
    from .query import Query, QueryResponse


class ICQRSBus(abc.ABC):
    @abc.abstractmethod
    def fetch(self, query: Query) -> QueryResponse:
        raise NotImplementedError


class CQRSBus(ICQRSBus):
    def fetch(self, query: Query) -> QueryResponse:
        handler_cls = query_registry.get_query_handler_cls(query_cls=query.__class__)
        handler = handler_cls()
        return handler.handle(query=query)
