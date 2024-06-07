from typing import List

from basket_cqrs_contract import hints

from framework.ddd.dto import DTO


class BasketItemDTO(DTO):
    id: hints.BasketItemId
    product_id: hints.ProductId
    product_name: hints.ProductName
    unit_price: hints.Price
    quantity: hints.Quantity
    picture_url: hints.PictureUrl


class CustomerBasketDTO(DTO):
    buyer_id: hints.CustomerId
    basket_items: List[BasketItemDTO]
