from pydantic import Field

from catalog_cqrs_contract import hints

from framework.common.dto import DTO


class CatalogTypeDTO(DTO):
    id: hints.CatalogTypeId
    type: str


class CatalogBrandDTO(DTO):
    id: hints.CatalogBrandId
    brand: str


class CatalogItemDTO(DTO):
    id: hints.CatalogItemId
    name: str
    description: str
    price: float
    picture_filename: str
    picture_url: str
    catalog_type: CatalogTypeDTO
    catalog_brand: CatalogBrandDTO
    available_stock: int
    restock_threshold: int
    maxstock_threshold: int
    on_reorder: bool
    discount: int = Field(ge=0, le=100)
