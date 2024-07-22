from catalog import hints

from framework.common.dto import DTO


class CatalogBrandDTO(DTO):

    id: hints.CatalogBrandId
    brand: str
