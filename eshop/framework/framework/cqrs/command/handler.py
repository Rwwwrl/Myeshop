from __future__ import annotations

import abc
from typing import TYPE_CHECKING, Union

from ..request import IRequestHandler

if TYPE_CHECKING:
    from .sync_command import CommandResponseType, ISyncCommand
    from .async_command import IAsyncCommand

__all__ = ('ICommandHandler', )


class ICommandHandler(IRequestHandler, abc.ABC):
    @abc.abstractmethod
    def handle(self, command: Union[ISyncCommand, IAsyncCommand]) -> Union[CommandResponseType, None]:
        raise NotImplementedError
