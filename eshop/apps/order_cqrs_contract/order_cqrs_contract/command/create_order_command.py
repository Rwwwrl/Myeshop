from datetime import datetime
from typing import List, final

from attrs import define

from pydantic.types import PositiveFloat, PositiveInt

from framework.common.dto import DTO
from framework.cqrs.command import SyncCommand

__all__ = ('CreateOrderCommand', )


@final
class OrderItemDTO(DTO):
    product_id: PositiveInt
    product_name: str
    unit_price: PositiveFloat
    units: PositiveInt
    picture_url: str


@final
@define(frozen=True)
class CreateOrderCommand(SyncCommand[None]):
    order_items: List[OrderItemDTO]
    user_id: PositiveInt
    username: str
    city: str
    street: str
    state: str
    country: str
    zip_code: str
    card_number: str
    card_holder_name: str
    card_expiration: datetime
    card_security_number: str
    card_type_id: PositiveInt
