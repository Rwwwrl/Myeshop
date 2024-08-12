from enum import Enum

import sqlalchemy
from sqlalchemy import (
    Integer,
    VARCHAR,
)
from sqlalchemy.orm import Mapped, mapped_column

from user_identity import hints
from user_identity.app_config import UserIdentityAppConfig

__all__ = ('User', )


class UserRoleEnum(Enum):
    ADMIN = 'ADMIN'
    CUSTOMER = 'CUSTOMER'


class User(UserIdentityAppConfig.get_sqlalchemy_base()):

    __tablename__ = 'user'

    id: Mapped[hints.UserId] = mapped_column(Integer, primary_key=True)
    name: Mapped[hints.UserName] = mapped_column(VARCHAR(40), unique=True, index=True)
    role: Mapped[UserRoleEnum] = mapped_column(sqlalchemy.Enum(UserRoleEnum))
    hashed_password: Mapped[str] = mapped_column()
