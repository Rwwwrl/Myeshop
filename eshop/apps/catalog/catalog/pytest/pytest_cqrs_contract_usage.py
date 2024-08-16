from catalog_cqrs_contract.event import (
    CatalogItemHasBeenDeletedEvent,
    CatalogItemPriceChangedEvent,
)

from framework.cqrs.context import InsideSqlachemyTransactionContext
from framework.for_pytests.for_testing_cqrs_contract_usage import ITestEventContractPublisher, assert_attribute


class TestCatalogItemPriceChangedEvent(ITestEventContractPublisher[CatalogItemPriceChangedEvent]):
    def test_event_contract(self) -> None:
        assert_attribute(CatalogItemPriceChangedEvent, 'catalog_item_id', int)
        assert_attribute(CatalogItemPriceChangedEvent, 'old_price', float)
        assert_attribute(CatalogItemPriceChangedEvent, 'new_price', float)
        assert_attribute(CatalogItemPriceChangedEvent, 'context', InsideSqlachemyTransactionContext)


class TestCatalogItemHasBeenDeleted(ITestEventContractPublisher[CatalogItemHasBeenDeletedEvent]):
    def test_event_contract(self) -> None:
        assert_attribute(CatalogItemHasBeenDeletedEvent, 'catalog_item_id', int)
        assert_attribute(CatalogItemHasBeenDeletedEvent, 'context', InsideSqlachemyTransactionContext)
