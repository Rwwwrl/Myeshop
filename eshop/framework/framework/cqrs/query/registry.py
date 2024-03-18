from typing import Dict, Type

from .handler import IQueryHandler
from .query import IQuery

QueryRegistryData = Dict[Type[IQuery], Type[IQueryHandler]]


class QueryAlreadyRegisteredException(Exception):
    pass


class ThatQueryIsNotRegistered(Exception):
    pass


class QueryRegistry:
    def __init__(self):
        self._data: QueryRegistryData = {}

    def register_query(self, query_cls: Type[IQuery], query_handler_cls: Type[IQueryHandler]) -> None:
        if self._data.get(query_cls, None) is not None:
            raise QueryAlreadyRegisteredException

        self._data[query_cls] = query_handler_cls

    def get_query_handler_cls(self, query_cls: Type[IQuery]) -> Type[IQueryHandler]:
        try:
            return self._data[query_cls]
        except KeyError:
            raise ThatQueryIsNotRegistered


query_registry = QueryRegistry()
