from __future__ import annotations

import abc
from typing import TYPE_CHECKING

from ..request import IRequestHandler

if TYPE_CHECKING:
    from .command import CommandResponseType, ICommand


class ICommandHandler(IRequestHandler, abc.ABC):
    @abc.abstractmethod
    def handle(self, command: ICommand) -> CommandResponseType:
        raise NotImplementedError
