from datetime import datetime

from pydantic.types import PositiveInt

from framework.cqrs.event import Event

from .customer_basket_dto import CustomerBasketDTO

__all__ = ('UserCheckoutAcceptedEvent', )


class UserCheckoutAcceptedEvent(Event):

    user_id: PositiveInt
    username: str
    order_number: PositiveInt
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
    basket: CustomerBasketDTO
