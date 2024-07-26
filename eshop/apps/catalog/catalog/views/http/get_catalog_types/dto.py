from catalog import hints

from framework.common.dto import DTO


class CatalogTypeDTO(DTO):

    id: hints.CatalogTypeId
    type: str
