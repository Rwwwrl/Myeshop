from __future__ import annotations

import abc
from typing import TYPE_CHECKING

from ..request import IRequestHandler

if TYPE_CHECKING:
    from .query import IQuery, QueryResponseType

__all__ = ('IQueryHandler', )


class IQueryHandler(IRequestHandler, abc.ABC):
    @abc.abstractmethod
    def handle(self, query: IQuery) -> QueryResponseType:
        raise NotImplementedError
