from datetime import date
from typing import final

from pydantic.types import PositiveInt

from framework.common.dto import DTO


@final
class BasketCheckoutRequestData(DTO):

    order_number: PositiveInt
    city: str
    street: str
    state: str
    country: str
    zip_code: str
    card_number: str
    card_holder_name: str
    card_expiration: date
    card_security_number: str
    card_type_id: PositiveInt
