from typing import Dict, Type, final

from .command import IAsyncCommand, ISyncCommand
from .query import IQuery
from .request import IRequest, IRequestHandler


class RequestHandlerAlreadyRegistered(Exception):
    pass


class RequestHandlerHasNotRegistered(Exception):
    pass


@final
class Registry:
    def __init__(self):
        self._storage: Dict[Type[IRequest], Type[IRequestHandler]] = {}

    def _ensure_request_handlers_has_not_been_registered(self, request_cls: Type[IRequest]) -> None:
        if request_cls in self._storage:
            raise RequestHandlerAlreadyRegistered(request_cls)

    def register(self, request_cls: Type[IRequest], request_handler_cls: Type[IRequestHandler]) -> None:
        if issubclass(request_cls, (ISyncCommand, IAsyncCommand, IQuery)):
            self._ensure_request_handlers_has_not_been_registered(request_cls=request_cls)

        self._storage[request_cls] = request_handler_cls

    def get_handler_cls(self, request_cls: Type[IRequest]) -> Type[IRequestHandler]:
        try:
            return self._storage[request_cls]
        except KeyError:
            raise RequestHandlerHasNotRegistered(request_cls)


_registry = Registry()


def get_registry() -> Registry:
    return _registry
