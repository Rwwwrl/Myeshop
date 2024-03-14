from __future__ import annotations

import abc
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .query import Query, QueryResponse


class ICQRSBus(abc.ABC):
    @abc.abstractmethod
    def fetch(self, query: Query) -> QueryResponse:
        raise NotImplementedError


class CQRSBus(ICQRSBus):
    def fetch(self, query: Query) -> QueryResponse:
        from .query.registry import query_registry

        handler_cls = query_registry.get_query_handler_cls(query_cls=query.__class__)
        handler = handler_cls()
        return handler.handle(query=query)


class CQRSBusSingletoneFactory:

    _instance: CQRSBus = None

    @classmethod
    def create(cls) -> CQRSBus:
        if cls._instance is not None:
            return cls._instance

        cls._instance = CQRSBus()
        return cls._instance
