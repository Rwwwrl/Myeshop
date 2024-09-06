from catalog_cqrs_contract.event import (
    CatalogItemHasBeenDeletedEvent,
    CatalogItemPriceOrDiscountWasChangedEvent,
)

from framework.cqrs.context import InsideSqlachemyTransactionContext
from framework.for_pytests.for_testing_cqrs_contract_usage import ITestEventContractPublisher, assert_attribute


class TestCatalogItemPriceOrDiscountWasChangedEvent(
    ITestEventContractPublisher[CatalogItemPriceOrDiscountWasChangedEvent],
):
    def test_event_contract(self) -> None:
        assert_attribute(CatalogItemPriceOrDiscountWasChangedEvent, 'catalog_item_id', int)
        assert_attribute(CatalogItemPriceOrDiscountWasChangedEvent, 'new_price', float)
        assert_attribute(CatalogItemPriceOrDiscountWasChangedEvent, 'new_discount', int)
        assert_attribute(CatalogItemPriceOrDiscountWasChangedEvent, 'context', InsideSqlachemyTransactionContext)


class TestCatalogItemHasBeenDeleted(ITestEventContractPublisher[CatalogItemHasBeenDeletedEvent]):
    def test_event_contract(self) -> None:
        assert_attribute(CatalogItemHasBeenDeletedEvent, 'catalog_item_id', int)
        assert_attribute(CatalogItemHasBeenDeletedEvent, 'context', InsideSqlachemyTransactionContext)
