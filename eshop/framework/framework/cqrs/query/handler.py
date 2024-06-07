from __future__ import annotations

import abc
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .query import Query, QueryResponseType


class IQueryHandler(abc.ABC):
    @abc.abstractmethod
    def handle(self, query: Query) -> QueryResponseType:
        raise NotImplementedError
