from datetime import datetime
from enum import Enum
from typing import final

from pydantic.types import PositiveInt

from framework.common.date_utils import utc_now

from order import hints
from order.framework.ddd import AggregateRoot

from .address import Address

__all__ = ('Order', )


@final
class OrderStatusEnum(Enum):
    SUBMITTED = 1
    AwaitingValidation = 2
    StockConfirmed = 3
    Paid = 4
    Shipped = 5
    Cancelled = 6


@final
class Order(AggregateRoot):
    def __init__(
        self,
        id: hints.OrderId,
        address: Address,
        buyer_id: PositiveInt,
        buyer_username: str,
    ):
        self.id = id
        self.address = address
        self._buyer_id = buyer_id
        self._buyer_username = buyer_username
        self._order_date: datetime = utc_now()
        self._order_status: OrderStatusEnum = OrderStatusEnum.SUBMITTED
