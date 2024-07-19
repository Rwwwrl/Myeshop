from typing import List

from sqlalchemy import (
    ForeignKey,
    INTEGER,
    TEXT,
    VARCHAR,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from catalog import hints
from catalog.app_config import CatalogAppConfig

__all__ = (
    'CatalogItemORM',
    'CatalogBrandORM',
    'CatalogTypeORM',
)


class CatalogTypeORM(CatalogAppConfig.get_sqlalchemy_base()):

    __tablename__ = 'catalog_type'

    id: Mapped[hints.CatalogTypeId] = mapped_column(INTEGER, primary_key=True)
    type: Mapped[str] = mapped_column()

    catalog_items: Mapped[List['CatalogItemORM']] = relationship(back_populates='catalog_type')


class CatalogBrandORM(CatalogAppConfig.get_sqlalchemy_base()):

    __tablename__ = 'catalog_brand'

    id: Mapped[hints.CatalogTypeId] = mapped_column(INTEGER, primary_key=True)
    brand: Mapped[str] = mapped_column()

    catalog_items: Mapped[List['CatalogItemORM']] = relationship(back_populates='catalog_brand')


class CatalogItemORM(CatalogAppConfig.get_sqlalchemy_base()):

    __tablename__ = 'catalog_item'

    id: Mapped[hints.CatalogItemId] = mapped_column(INTEGER, primary_key=True)
    name: Mapped[str] = mapped_column(VARCHAR(50))
    description: Mapped[str] = mapped_column(TEXT)
    price: Mapped[float] = mapped_column()
    picture_filename: Mapped[str] = mapped_column()
    picture_url: Mapped[str] = mapped_column()
    catalog_type_id: Mapped[hints.CatalogTypeId] = mapped_column(ForeignKey('catalog_type.id'))
    catalog_brand_id: Mapped[hints.CatalogBrandId] = mapped_column(ForeignKey('catalog_brand.id'))
    # quantity in stock
    available_stock: Mapped[int] = mapped_column()
    # Available stock at which we should reorder
    restock_threshold: Mapped[int] = mapped_column()
    # Maximum number of units that can be in-stock at any time (due to physicial/logistical constraints in warehouses)
    maxstock_threshold: Mapped[int] = mapped_column()
    # True if item is on reorder
    on_reorder: Mapped[bool] = mapped_column()

    catalog_type: Mapped[CatalogTypeORM] = relationship(back_populates='catalog_items')
    catalog_brand: Mapped[CatalogBrandORM] = relationship(back_populates='catalog_items')
