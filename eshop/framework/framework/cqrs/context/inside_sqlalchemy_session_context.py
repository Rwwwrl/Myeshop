from typing import Annotated, Self

from sqlalchemy.orm import Session as lib_Session

from framework.sqlalchemy.session import Session

from .icontext import IContext


class InsideSqlachemySessionContext(IContext):

    session: Annotated[lib_Session, Session]

    def __eq__(self, other: Self) -> bool:
        return True
