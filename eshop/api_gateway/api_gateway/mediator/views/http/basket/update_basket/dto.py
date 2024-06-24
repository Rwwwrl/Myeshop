from typing import List, NewType, final

from framework.common.dto import DTO

ProductId = NewType('ProductId', int)


@final
class UpdateBasketRequestItemData(DTO):
    product_id: ProductId
    quantity: int


@final
class UpdateBasketRequestData(DTO):
    buyer_id: int
    basket_items: List[UpdateBasketRequestItemData]
