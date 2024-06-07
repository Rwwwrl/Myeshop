from __future__ import annotations

import abc
from typing import TYPE_CHECKING

from ..request import IRequestHandler

if TYPE_CHECKING:
    from .query import Query, QueryResponseType


class IQueryHandler(IRequestHandler, abc.ABC):
    @abc.abstractmethod
    def handle(self, query: Query) -> QueryResponseType:
        raise NotImplementedError
