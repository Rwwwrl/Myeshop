from typing import NewType

from pydantic.types import PositiveInt

JWTToken = NewType('JWTToken', str)

UserId = NewType('UserId', PositiveInt)
UserName = NewType('UserName', str)
