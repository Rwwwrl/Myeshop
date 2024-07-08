from __future__ import annotations

import abc
from typing import TYPE_CHECKING

from ..request import IRequestHandler

if TYPE_CHECKING:
    from .event import IEvent

__all__ = ('IEventHandler', )


class IEventHandler(IRequestHandler, abc.ABC):
    @abc.abstractmethod
    def handle(self, event: IEvent) -> None:
        raise NotImplementedError
