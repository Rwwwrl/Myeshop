from __future__ import annotations

import abc
from logging import getLogger
from typing import List, TYPE_CHECKING, cast

from . import registry
from .command import ICommandHandler
from .exceptions import UnexpectedError
from .query import IQueryHandler

if TYPE_CHECKING:
    from .query import IQuery, QueryResponseType
    from .command import ISyncCommand, CommandResponseType, IAsyncCommand
    from .event import IEvent


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

    @abc.abstractmethod
    def publish(self, event: IEvent) -> None:
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

    def publish(self, event: IEvent) -> None:
        self._logger.debug('start processing event %s', event)

        exceptions: List[UnexpectedError] = []

        for handler_cls in registry.get_registry().get_event_handlers_cls(event=type(event)):
            try:
                handler_cls().handle(event=event)
            except Exception as e:
                self._logger.debug('event handler %s ended with an error during handle event %s', handler_cls, event)
                exceptions.append(UnexpectedError(original_exception=e))
                continue
            else:
                self._logger.debug('event handler %s successfully handle event %s', handler_cls, event)

        if exceptions:
            self._logger.debug('event %s processing produced errors %s', event, exceptions)
            raise ExceptionGroup(f'event {event} processing produced errors', exceptions)


class CQRSBusSingletoneFactory:

    _instance: CQRSBus = None

    @classmethod
    def create(cls) -> CQRSBus:
        if cls._instance is not None:
            return cls._instance

        cls._instance = CQRSBus()
        return cls._instance
