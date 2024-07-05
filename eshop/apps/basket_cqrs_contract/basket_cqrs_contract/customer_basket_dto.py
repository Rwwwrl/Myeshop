from typing import List, Union, final

from basket_cqrs_contract import hints

from framework.common.dto import DTO


@final
class BasketItemDTO(DTO):
    id: Union[hints.BasketItemId, None]
    product_id: hints.ProductId
    product_name: hints.ProductName
    unit_price: hints.Price
    quantity: hints.Quantity
    picture_url: hints.PictureUrl


@final
class CustomerBasketDTO(DTO):
    buyer_id: hints.BuyerId
    basket_items: List[BasketItemDTO]
