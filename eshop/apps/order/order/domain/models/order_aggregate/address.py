from typing import final

from order.framework.ddd import ValueObject


@final
class Address(ValueObject):
    street: str
    city: str
    state: str
    country: str
    zip_code: str
