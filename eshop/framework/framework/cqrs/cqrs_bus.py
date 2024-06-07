from __future__ import annotations

import abc
from logging import getLogger
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .query import Query, QueryResponseType


class HandlerRaisedAnError(Exception):
    def __init__(self, *args, original_exception: Exception, **kwargs):
        self._original_exception_cls_name = original_exception.__class__.__name__
        self._original_exception_message = str(original_exception)


class ICQRSBus(abc.ABC):
    @abc.abstractmethod
    def fetch(self, query: Query) -> QueryResponseType:
        raise NotImplementedError


class CQRSBus(ICQRSBus):

    _logger = getLogger('CQRSBus')

    def fetch(self, query: Query) -> QueryResponseType:
        from .query.registry import query_registry

        self._logger.debug('start processing query %s', query)

        handler_cls = query_registry.get_query_handler_cls(query_cls=query.__class__)
        handler = handler_cls()
        try:
            result = handler.handle(query=query)
        except Exception as e:
            self._logger.debug('query %s was completed with an error', query)
            raise HandlerRaisedAnError(original_exception=e)
        else:
            self._logger.debug('query %s was succesfully completed', query)
            return result


class CQRSBusSingletoneFactory:

    _instance: CQRSBus = None

    @classmethod
    def create(cls) -> CQRSBus:
        if cls._instance is not None:
            return cls._instance

        cls._instance = CQRSBus()
        return cls._instance
