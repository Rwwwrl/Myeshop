from typing import final

from pydantic import Field
from pydantic.types import PositiveFloat

from catalog_cqrs_contract import hints

from framework.cqrs.context import InsideSqlachemyTransactionContext
from framework.cqrs.event import Event


@final
class CatalogItemPriceChangedEvent(Event):
    catalog_item_id: hints.CatalogItemId
    old_price: PositiveFloat
    new_price: PositiveFloat

    context: InsideSqlachemyTransactionContext = Field(exclude=False)


@final
class CatalogItemHasBeenDeletedEvent(Event):
    catalog_item_id: hints.CatalogItemId

    context: InsideSqlachemyTransactionContext = Field(exclude=False)
