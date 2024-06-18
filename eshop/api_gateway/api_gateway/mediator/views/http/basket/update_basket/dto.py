from typing import List, final

from api_gateway import hints

from framework.common.dto import DTO


@final
class UpdateBasketRequestItemData(DTO):
    product_id: hints.ProductId
    quantity: int


@final
class UpdateBasketRequestData(DTO):
    buyer_id: hints.UserId
    basket_items: List[UpdateBasketRequestItemData]
