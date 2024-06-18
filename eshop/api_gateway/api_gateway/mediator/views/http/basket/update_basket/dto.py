from typing import List, NewType, final

from framework.common.dto import DTO

ProductId = NewType('ProductId', int)


@final
class UpdateBasketRequestItemData(DTO):
    product_id: int
    quantity: int


@final
class UpdateBasketRequestData(DTO):
    buyer_id: int
    basket_items: List[UpdateBasketRequestItemData]
