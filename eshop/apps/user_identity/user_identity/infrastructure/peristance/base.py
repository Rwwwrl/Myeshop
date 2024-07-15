from sqlalchemy import MetaData
from sqlalchemy.orm import DeclarativeBase

from user_identity.app_config import UserIdentityAppConfig


class Base(DeclarativeBase):

    metadata = MetaData(schema=UserIdentityAppConfig.name)
