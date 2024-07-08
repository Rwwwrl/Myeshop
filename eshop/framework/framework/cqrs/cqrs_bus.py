from __future__ import annotations

import abc
from logging import getLogger
from typing import TYPE_CHECKING, cast

from . import registry
from .command import ICommandHandler
from .exceptions import UnexpectedError
from .query import IQueryHandler

if TYPE_CHECKING:
    from .query import IQuery, QueryResponseType
    from .command import ISyncCommand, CommandResponseType, IAsyncCommand


class ICQRSBus(abc.ABC):
    @abc.abstractmethod
    def fetch(self, query: IQuery) -> QueryResponseType:
        raise NotImplementedError

    @abc.abstractmethod
    def async_execute(self, command: IAsyncCommand) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def sync_execute(self, command: ISyncCommand) -> CommandResponseType:
        raise NotImplementedError


class CQRSBus(ICQRSBus):

    _logger = getLogger('CQRSBus')

    def fetch(self, query: IQuery) -> QueryResponseType:
        self._logger.debug('start processing query %s', query)

        handler_cls = cast(IQueryHandler, registry.get_registry().get_handler_cls(request_cls=type(query)))
        try:
            result = handler_cls().handle(query=query)
        except query.__possible_exceptions__ as e:
            self._logger.debug('query %s was completed with expected exception', query)
            raise e
        except Exception as e:
            self._logger.debug('query %s was completed with non-expected error', query)
            raise UnexpectedError(original_exception=e)
        else:
            self._logger.debug('query %s was succesfully completed', query)
            return result

    def async_execute(self, command: IAsyncCommand) -> None:
        self._logger.debug('start processing command %s', command)
        handler_cls = cast(ICommandHandler, registry.get_registry().get_handler_cls(request_cls=type(command)))
        try:
            handler_cls().handle(command=command)
        except Exception as e:
            self._logger.debug('command %s was completed with error', command)
            raise UnexpectedError(original_exception=e)
        else:
            self._logger.debug('command %s was succesfully completed', command)

    def sync_execute(self, command: ISyncCommand) -> CommandResponseType:
        self._logger.debug('start processing command %s', command)
        handler_cls = cast(ICommandHandler, registry.get_registry().get_handler_cls(request_cls=type(command)))
        try:
            result = handler_cls().handle(command=command)
        except command.__possible_exceptions__ as e:
            self._logger.debug('command %s was completed with expected exception', command)
            raise e
        except Exception as e:
            self._logger.debug('command %s was completed with non-expected error', command)
            raise UnexpectedError(original_exception=e)
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
