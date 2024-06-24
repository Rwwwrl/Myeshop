from typing import List

from framework.common.dto import DTO


class UpdateBasketItemData(DTO):

    basket_item_id: int
    new_quantity: int


class UpdateBasketItemsRequest(DTO):

    updates: List[UpdateBasketItemData]
