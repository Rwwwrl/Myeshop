from typing import final

from pydantic import Field
from pydantic.types import PositiveFloat

from catalog_cqrs_contract import hints

from framework.cqrs.context import InsideSqlachemyTransactionContext
from framework.cqrs.event import Event


@final
class CatalogItemPriceOrDiscountWasChangedEvent(Event):
    """
    событие сигнализирует о том, что поменялось значение discount или price
    В случае, если поменялся, например, только price, то в поле new_discount будет старое значение discount
    (и наоборот)
    """
    catalog_item_id: hints.CatalogItemId
    new_price: PositiveFloat
    new_discount: int = Field(ge=0, le=100)

    context: InsideSqlachemyTransactionContext = Field(exclude=False)


@final
class CatalogItemHasBeenDeletedEvent(Event):
    catalog_item_id: hints.CatalogItemId

    context: InsideSqlachemyTransactionContext = Field(exclude=False)
