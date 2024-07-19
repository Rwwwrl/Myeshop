from pydantic.types import PositiveFloat, PositiveInt

from catalog import hints

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
