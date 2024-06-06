from __future__ import annotations

import abc
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .query import Query, QueryResponseType


class ICQRSBus(abc.ABC):
    @abc.abstractmethod
    def fetch(self, query: Query) -> QueryResponseType:
        raise NotImplementedError


class HandlerRaisedAnError(Exception):
    def __init__(self, *args, original_exception: Exception, **kwargs):
        self._original_exception_cls_name = original_exception.__class__.__name__
        self._original_exception_message = str(original_exception)


class CQRSBus(ICQRSBus):
    def fetch(self, query: Query) -> QueryResponseType:
        from .query.registry import query_registry

        handler_cls = query_registry.get_query_handler_cls(query_cls=query.__class__)
        handler = handler_cls()
        try:
            return handler.handle(query=query)
        except Exception as e:
            raise HandlerRaisedAnError(original_exception=e)


class CQRSBusSingletoneFactory:

    _instance: CQRSBus = None

    @classmethod
    def create(cls) -> CQRSBus:
        if cls._instance is not None:
            return cls._instance

        cls._instance = CQRSBus()
        return cls._instance
