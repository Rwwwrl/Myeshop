from typing import Optional

from pydantic import Field
from pydantic.types import PositiveInt

from framework.common.dto import DTO


class AddBasketItemRequest(DTO):
    catalog_item_id: int
    quantity: Optional[PositiveInt] = Field(default=1)
