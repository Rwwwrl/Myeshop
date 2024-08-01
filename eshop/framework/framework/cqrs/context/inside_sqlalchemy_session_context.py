from typing import Annotated

from sqlalchemy.orm import Session as lib_Session

from framework.sqlalchemy.session import Session

from .icontext import IContext


class InsideSqlachemySessionContext(IContext):

    session: Annotated[lib_Session, Session]
