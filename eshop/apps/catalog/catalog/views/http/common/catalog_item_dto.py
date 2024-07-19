from pydantic.types import PositiveFloat, PositiveInt

from catalog import hints
from catalog.infrastructure.persistance.postgres import CatalogItemORM

from framework.common.dto import DTO


class CatalogItemDTO(DTO):
    id: hints.CatalogItemId
    name: str
    description: str
    price: PositiveFloat
    picture_filename: str
    picture_url: str
    available_stock: PositiveInt
    restock_threshold: PositiveInt
    maxstock_threshold: PositiveInt
    on_reorder: bool

    @classmethod
    def from_orm(cls, orm: CatalogItemORM) -> 'CatalogItemDTO':
        return CatalogItemDTO(
            id=orm.id,
            name=orm.name,
            description=orm.description,
            price=orm.price,
            picture_filename=orm.picture_filename,
            picture_url=orm.picture_url,
            catalog_type_id=orm.catalog_type_id,
            catalog_brand_id=orm.catalog_brand_id,
            available_stock=orm.available_stock,
            restock_threshold=orm.restock_threshold,
            maxstock_threshold=orm.maxstock_threshold,
            on_reorder=orm.on_reorder,
        )
