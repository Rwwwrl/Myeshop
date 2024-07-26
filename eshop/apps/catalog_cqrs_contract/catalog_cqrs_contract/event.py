from typing import final

from pydantic.types import PositiveFloat

from catalog_cqrs_contract import hints

from framework.cqrs.event import Event


@final
class CatalogItemPriceChangedEvent(Event):
    catalog_item_id: hints.CatalogItemId
    old_price: PositiveFloat
    new_price: PositiveFloat


@final
class CatalogItemHasBeenDeletedEvent(Event):
    catalog_item_id: hints.CatalogItemId
