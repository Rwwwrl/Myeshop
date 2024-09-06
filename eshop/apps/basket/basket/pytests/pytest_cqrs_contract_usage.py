from datetime import datetime
from typing import List, Union

from basket_cqrs_contract.customer_basket_dto import BasketItemDTO, CustomerBasketDTO
from basket_cqrs_contract.event import UserCheckoutAcceptedEvent
from basket_cqrs_contract.query import CustomerBasketQuery

from catalog_cqrs_contract.event import (
    CatalogItemHasBeenDeletedEvent,
    CatalogItemPriceOrDiscountWasChangedEvent,
)

from framework.cqrs.context import InsideSqlachemyTransactionContext
from framework.for_pytests.for_testing_cqrs_contract_usage import (
    ITestEventContractConsumer,
    ITestEventContractPublisher,
    ITestQueryContract,
    assert_attribute,
)

from user_identity_cqrs_contract.query import UserByIdQuery
from user_identity_cqrs_contract.query.query_response import UserDTO


class TestUserCheckoutAcceptedEvent(ITestEventContractPublisher[UserCheckoutAcceptedEvent]):
    def test_event_contract(self) -> None:
        assert_attribute(UserCheckoutAcceptedEvent, 'user_id', int)
        assert_attribute(UserCheckoutAcceptedEvent, 'username', str)
        assert_attribute(UserCheckoutAcceptedEvent, 'order_number', int)
        assert_attribute(UserCheckoutAcceptedEvent, 'city', str)
        assert_attribute(UserCheckoutAcceptedEvent, 'street', str)
        assert_attribute(UserCheckoutAcceptedEvent, 'state', str)
        assert_attribute(UserCheckoutAcceptedEvent, 'country', str)
        assert_attribute(UserCheckoutAcceptedEvent, 'zip_code', str)
        assert_attribute(UserCheckoutAcceptedEvent, 'card_number', str)
        assert_attribute(UserCheckoutAcceptedEvent, 'card_holder_name', str)
        assert_attribute(UserCheckoutAcceptedEvent, 'card_expiration', datetime)
        assert_attribute(UserCheckoutAcceptedEvent, 'card_security_number', str)
        assert_attribute(UserCheckoutAcceptedEvent, 'card_type_id', int)
        assert_attribute(UserCheckoutAcceptedEvent, 'basket', CustomerBasketDTO)

        assert_attribute(CustomerBasketDTO, 'buyer_id', int)
        assert_attribute(CustomerBasketDTO, 'basket_items', List[BasketItemDTO])

        assert_attribute(BasketItemDTO, 'id', Union[int, None])
        assert_attribute(BasketItemDTO, 'product_id', int)
        assert_attribute(BasketItemDTO, 'product_name', str)
        assert_attribute(BasketItemDTO, 'unit_price', float)
        assert_attribute(BasketItemDTO, 'quantity', int)
        assert_attribute(BasketItemDTO, 'picture_url', str)


class TestCatalogItemPriceOrDiscountWasChangedEvent(
    ITestEventContractConsumer[CatalogItemPriceOrDiscountWasChangedEvent],
):
    def test_event_contract(self) -> None:
        assert_attribute(CatalogItemPriceOrDiscountWasChangedEvent, 'catalog_item_id', int)
        assert_attribute(CatalogItemPriceOrDiscountWasChangedEvent, 'new_price', float)
        assert_attribute(CatalogItemPriceOrDiscountWasChangedEvent, 'new_discount', int)
        assert_attribute(CatalogItemPriceOrDiscountWasChangedEvent, 'context', InsideSqlachemyTransactionContext)


class TestCatalogItemHasBeenDeletedEvent(ITestEventContractConsumer[CatalogItemHasBeenDeletedEvent]):
    def test_event_contract(self) -> None:
        assert_attribute(CatalogItemHasBeenDeletedEvent, 'catalog_item_id', int)
        assert_attribute(CatalogItemHasBeenDeletedEvent, 'context', InsideSqlachemyTransactionContext)


class TestUserQuery(ITestQueryContract[UserByIdQuery]):
    def test_query_contract(self) -> None:
        assert_attribute(UserByIdQuery, 'id', int)

    def test_query_response_contract(self) -> None:
        response_type = UserByIdQuery.__response_type__()

        assert response_type == UserDTO

        assert_attribute(UserDTO, 'name', str)


class TestCustomerBasketQuery(ITestQueryContract[CustomerBasketQuery]):
    def test_query_contract(self) -> None:
        assert_attribute(CustomerBasketQuery, 'customer_id', int)

    def test_query_response_contract(self) -> None:
        response_type = CustomerBasketQuery.__response_type__()

        assert response_type == CustomerBasketDTO

        # на данный момент мы не используем никакие поля, потому проверяем только response_type
