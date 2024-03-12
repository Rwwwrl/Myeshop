from sqlalchemy import Integer, VARCHAR
from sqlalchemy.orm import Mapped, mapped_column

from eshop import settings
from eshop.apps.user_identity import hints
from eshop.apps.user_identity.app_config import UserIdentityAppConfig


class User(settings.SQLALCHEMY_BASE):

    __tablename__ = f'{UserIdentityAppConfig.name}__user'

    id: Mapped[hints.UserId] = mapped_column(Integer, primary_key=True)
    name: Mapped[hints.UserName] = mapped_column(VARCHAR(40), unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column()
