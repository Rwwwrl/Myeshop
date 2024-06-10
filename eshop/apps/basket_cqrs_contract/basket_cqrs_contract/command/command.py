from typing import List, final

from attrs import define

from basket_cqrs_contract import hints

from framework.common.dto import DTO
from framework.cqrs.command import Command

__all__ = ('UpdateCustomerBasketCommand', )


@final
class BasketItemDTO(DTO):
    product_id: hints.ProductId
    product_name: hints.ProductName
    unit_price: hints.Price
    quantity: hints.Quantity
    picture_url: hints.PictureUrl


@final
@define
class UpdateCustomerBasketCommand(Command[None]):

    buyer_id: hints.CustomerId
    basket_items: List[BasketItemDTO]
