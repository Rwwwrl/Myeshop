from typing import Dict, Type, Union

from .command import ICommand, ICommandHandler
from .query import IQuery, IQueryHandler

Key = Union[Type[ICommand], Type[IQuery]]
Value = Union[Type[ICommandHandler], Type[IQueryHandler]]

_Registry = Dict[Key, Value]


class AlreadyRegistred(Exception):
    pass


class IsNotRegistered(Exception):
    pass


class Registry:
    def __init__(self):
        self._data: _Registry = {}

    def _ensure_key_has_not_been_registred(self, key: Key) -> None:
        if key in self._data:
            raise AlreadyRegistred

    def register(self, key: Key, value: Value) -> None:
        if issubclass(key, (ICommand, IQuery)):
            self._ensure_key_has_not_been_registred(key)

        self._data[key] = value

    def __getitem__(self, key: Key) -> Value:
        try:
            return self._data[key]
        except KeyError:
            raise IsNotRegistered(str(key))


registry = Registry()
