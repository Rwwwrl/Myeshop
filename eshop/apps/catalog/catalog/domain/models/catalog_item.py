from __future__ import annotations

from typing import Annotated, TYPE_CHECKING

from sqlalchemy import (
    BOOLEAN,
    CheckConstraint,
    ForeignKey,
    INTEGER,
    TEXT,
    VARCHAR,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from typing_extensions import Doc

from catalog import hints
from catalog.app_config import CatalogAppConfig

__all__ = ('CatalogItem', )

if TYPE_CHECKING:
    from .catalog_type import CatalogType
    from .catalog_brand import CatalogBrand


class CatalogItem(CatalogAppConfig.get_sqlalchemy_base()):

    __tablename__ = 'catalog_item'

    id: Mapped[hints.CatalogItemId] = mapped_column(INTEGER, primary_key=True)
    name: Mapped[str] = mapped_column(VARCHAR(50))
    description: Mapped[str] = mapped_column(TEXT)
    price: Mapped[float] = mapped_column()
    picture_filename: Mapped[str] = mapped_column()
    picture_url: Mapped[str] = mapped_column()
    catalog_type_id: Mapped[hints.CatalogTypeId] = mapped_column(ForeignKey('catalog_type.id'))
    catalog_brand_id: Mapped[hints.CatalogBrandId] = mapped_column(ForeignKey('catalog_brand.id'))

    available_stock: Mapped[Annotated[
        int,
        Doc('quantity in stock'),
    ]] = mapped_column(INTEGER)

    restock_threshold: Mapped[Annotated[
        int,
        Doc('Available stock at which we should reorder'),
    ]] = mapped_column(INTEGER)

    maxstock_threshold: Mapped[Annotated[
        int,
        Doc(
            """
            Maximum number of units that can be in-stock at any time
             (due to physicial/logistical constraints in warehouses)
            """,
        ),
    ]] = mapped_column(INTEGER)

    on_reorder: Mapped[Annotated[bool, Doc('True if item is on reorder')]] = mapped_column(BOOLEAN)

    discount: Mapped[Annotated[
        int,
        Doc('скидкой является целое число от 0 до 100% включительно'),
    ]] = mapped_column(INTEGER, CheckConstraint('discount betweeen 0 and 100'))

    catalog_type: Mapped[CatalogType] = relationship(back_populates='catalog_items')
    catalog_brand: Mapped[CatalogBrand] = relationship(back_populates='catalog_items')
