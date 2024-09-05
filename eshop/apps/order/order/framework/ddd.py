from pydantic import BaseModel
from pydantic.types import PositiveInt


class ValueObject(BaseModel, frozen=True):
    pass


class Entity:
    id: PositiveInt


class AggregateRoot(Entity):
    pass
