from typing import NewType

from pydantic.types import PositiveInt

CatalogItemId = NewType('CatalogItemId', PositiveInt)
CatalogItemName = NewType('CatalogItemName', str)

CatalogTypeId = NewType('CatalogTypeId', PositiveInt)

CatalogBrandId = NewType('CatalogBrandId', PositiveInt)
