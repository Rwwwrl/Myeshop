from typing import Dict, List, Tuple, Type, Union, final

from .command import IAsyncCommand, ISyncCommand
from .event import IEvent, IEventHandler
from .query import IQuery
from .request import IRequest, IRequestHandler

NonEventRequestClasses: Tuple[IRequest] = (
    IAsyncCommand,
    ISyncCommand,
    IQuery,
)
INonEventRequest = Union[IAsyncCommand, ISyncCommand, IQuery]


class RequestHandlerAlreadyRegistered(Exception):
    pass


class RequestHandlerHasNotRegistered(Exception):
    pass


@final
class Registry:
    def __init__(self):
        self._storage: Dict[Type[IRequest], Union[Type[IRequestHandler], List[Type[IRequestHandler]]]] = {}

    def _ensure_request_handlers_has_not_been_registered(self, request_cls: Type[IRequest]) -> None:
        if request_cls in self._storage:
            raise RequestHandlerAlreadyRegistered(request_cls)

    def register(self, request_cls: Type[IRequest], request_handler_cls: Type[IRequestHandler]) -> None:
        if issubclass(request_cls, NonEventRequestClasses):
            self._ensure_request_handlers_has_not_been_registered(request_cls=request_cls)
            self._storage[request_cls] = request_handler_cls

        if issubclass(request_cls, IEvent):
            self._storage.setdefault(request_cls, []).append(request_handler_cls)

    def get_handler_cls(self, request_cls: Type[INonEventRequest]) -> Type[IRequestHandler]:
        try:
            return self._storage[request_cls]
        except KeyError:
            raise RequestHandlerHasNotRegistered(request_cls)

    def get_event_handlers_cls(self, event: Type[IEvent]) -> List[Type[IEventHandler]]:
        try:
            return self._storage[event]
        except KeyError:
            raise RequestHandlerHasNotRegistered(event)


_registry = Registry()


def get_registry() -> Registry:
    return _registry
