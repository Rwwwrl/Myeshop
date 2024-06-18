from __future__ import annotations

import abc
from logging import getLogger
from typing import TYPE_CHECKING, cast

from . import registry

if TYPE_CHECKING:
    from .query import Query, QueryResponseType, IQueryHandler
    from .command import Command, CommandResponseType, ICommandHandler


class CQRSException(Exception):
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
        self._logger.debug('start processing query %s', query)

        handler_cls = cast(IQueryHandler, registry.get_registry().get_handler_cls(request_cls=type(query)))
        try:
            result = handler_cls().handle(query=query)
        except Exception as e:
            self._logger.debug('query %s was completed with an error', query)
            raise CQRSException(original_exception=e)
        else:
            self._logger.debug('query %s was succesfully completed', query)
            return result

    def execute(self, command: Command) -> CommandResponseType:
        self._logger.debug('start processing command %s', command)
        handler_cls = cast(ICommandHandler, registry.get_registry().get_handler_cls(request_cls=type(command)))
        try:
            result = handler_cls().handle(command=command)
        except Exception as e:
            self._logger.debug('command %s was completed with an error', command)
            raise CQRSException(original_exception=e)
        else:
            self._logger.debug('command %s was succesfully completed', command)
            return result


class CQRSBusSingletoneFactory:

    _instance: CQRSBus = None

    @classmethod
    def create(cls) -> CQRSBus:
        if cls._instance is not None:
            return cls._instance

        cls._instance = CQRSBus()
        return cls._instance
