from typing import Optional

from pydantic import Field

from framework.common.dto import DTO


class AddBasketItemRequest(DTO):
    catalog_item_id: int
    # TODO: должен быть PositiveInt
    quantity: Optional[int] = Field(default=1)
