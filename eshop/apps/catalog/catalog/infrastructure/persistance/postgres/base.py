from sqlalchemy import MetaData
from sqlalchemy.orm import DeclarativeBase

from catalog.app_config import CatalogAppConfig


class Base(DeclarativeBase):

    metadata = MetaData(schema=CatalogAppConfig.name)
