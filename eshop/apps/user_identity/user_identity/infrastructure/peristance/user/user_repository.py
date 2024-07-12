from sqlalchemy import select
from sqlalchemy.orm import Session

from user_identity import hints

from .user import UserORM


class NotFoundInDB(Exception):
    pass


class UserRepository:
    def __init__(self, session: Session):
        self._session = session

    def get_by_id(self, id: hints.UserId) -> UserORM:
        stmt = select(UserORM).where(UserORM.id == id)

        user = self._session.scalar(stmt)
        if not user:
            raise NotFoundInDB

        return user

    def get_by_name(self, name: hints.UserName) -> UserORM:
        stmt = select(UserORM).where(UserORM.name == name)

        user = self._session.scalar(stmt)
        if not user:
            raise NotFoundInDB

        return user
