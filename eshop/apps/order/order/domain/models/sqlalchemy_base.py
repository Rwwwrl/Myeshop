from sqlalchemy import MetaData
from sqlalchemy.orm import DeclarativeBase

from order.app_config import OrderAppConfig


class Base(DeclarativeBase):

    metadata = MetaData(schema=OrderAppConfig.name)
