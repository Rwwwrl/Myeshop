from sqlalchemy.orm import Session

from eshop.settings import SQLALCHEMY_ENGINE


def session_factory() -> Session:
    return Session(SQLALCHEMY_ENGINE)
