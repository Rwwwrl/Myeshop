from typing import Dict, TYPE_CHECKING, Type

if TYPE_CHECKING:
    from .query import Query
    from .handler import IQueryHandler

QueryRegistryData = Dict[Type[Query], Type[IQueryHandler]]


class QueryAlreadyRegisteredException(Exception):
    pass


class ThatQueryIsNotRegistered(Exception):
    pass


class QueryRegistry:
    def __init__(self):
        self._data: QueryRegistryData = {}

    def register_query(self, query_cls: Type[Query], query_handler_cls: Type[IQueryHandler]) -> None:
        if self._data.get(query_cls, None) is not None:
            raise QueryAlreadyRegisteredException

        self._data[query_cls] = query_handler_cls

    def get_query_handler_cls(self, query_cls: Type[Query]) -> Type[IQueryHandler]:
        try:
            return self._data[query_cls]
        except KeyError:
            raise ThatQueryIsNotRegistered


query_registry = QueryRegistry()
