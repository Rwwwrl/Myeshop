from __future__ import annotations

import abc
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .command import CommandResponseType, ICommand


class ICommandHandler(abc.ABC):
    @abc.abstractmethod
    def handle(self, command: ICommand) -> CommandResponseType:
        raise NotImplementedError
