from typing import NewType

from pydantic.types import PositiveInt

OrderId = NewType('OrderId', PositiveInt)
