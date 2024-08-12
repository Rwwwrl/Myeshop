from __future__ import annotations

from typing import List, TYPE_CHECKING

from sqlalchemy import INTEGER
from sqlalchemy.orm import Mapped, mapped_column, relationship

from catalog import hints
from catalog.app_config import CatalogAppConfig

if TYPE_CHECKING:
    from .catalog_item import CatalogItem

__all__ = ('CatalogBrand', )


class CatalogBrand(CatalogAppConfig.get_sqlalchemy_base()):

    __tablename__ = 'catalog_brand'

    id: Mapped[hints.CatalogTypeId] = mapped_column(INTEGER, primary_key=True)
    brand: Mapped[str] = mapped_column()

    catalog_items: Mapped[List[CatalogItem]] = relationship(back_populates='catalog_brand')
