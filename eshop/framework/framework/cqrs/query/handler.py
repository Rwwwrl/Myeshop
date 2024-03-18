import abc
from typing import Type

from .query import Query, QueryResponse


class IQueryHandler(abc.ABC):
    @abc.abstractmethod
    def handle(self, query: Query) -> QueryResponse:
        raise NotImplementedError


def query_handler(query_cls: Type[Query]):
    from .registry import query_registry

    def inner(query_handler_cls: Type[IQueryHandler]):
        query_registry.register_query(query_cls=query_cls, query_handler_cls=query_handler_cls)
        return query_handler_cls

    return inner
