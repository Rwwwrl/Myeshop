from datetime import datetime
from typing import List, Union

import basket_cqrs_contract.hints
from basket_cqrs_contract.customer_basket_dto import BasketItemDTO, CustomerBasketDTO
from basket_cqrs_contract.event import UserCheckoutAcceptedEvent
from basket_cqrs_contract.query import CustomerBasketQuery

import catalog_cqrs_contract.hints
from catalog_cqrs_contract.event import (
    CatalogItemHasBeenDeletedEvent,
    CatalogItemPriceChangedEvent,
)

from framework.for_pytests.for_testing_cqrs_contract_usage import (
    ITestEventContract,
    ITestQueryContract,
    assert_attribute,
)

import user_identity_cqrs_contract.hints
from user_identity_cqrs_contract.query import UserQuery
from user_identity_cqrs_contract.query.query_response import UserDTO


class TestUserCheckoutAcceptedEvent(ITestEventContract[UserCheckoutAcceptedEvent]):
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

        assert_attribute(CustomerBasketDTO, 'buyer_id', basket_cqrs_contract.hints.BuyerId)
        assert_attribute(CustomerBasketDTO, 'basket_items', List[BasketItemDTO])

        assert_attribute(BasketItemDTO, 'id', Union[basket_cqrs_contract.hints.BasketItemId, None])
        assert_attribute(BasketItemDTO, 'product_id', basket_cqrs_contract.hints.ProductId)
        assert_attribute(BasketItemDTO, 'product_name', basket_cqrs_contract.hints.ProductName)
        assert_attribute(BasketItemDTO, 'unit_price', basket_cqrs_contract.hints.Price)
        assert_attribute(BasketItemDTO, 'quantity', basket_cqrs_contract.hints.Quantity)
        assert_attribute(BasketItemDTO, 'picture_url', basket_cqrs_contract.hints.PictureUrl)


class TestCatalogItemPriceChangedEvent(ITestEventContract[CatalogItemPriceChangedEvent]):
    def test_event_contract(self) -> None:
        assert_attribute(CatalogItemPriceChangedEvent, 'catalog_item_id', catalog_cqrs_contract.hints.CatalogItemId)
        assert_attribute(CatalogItemPriceChangedEvent, 'new_price', float)


class TestCatalogItemHasBeenDeletedEvent(ITestEventContract[CatalogItemHasBeenDeletedEvent]):
    def test_event_contract(self) -> None:
        assert_attribute(CatalogItemHasBeenDeletedEvent, 'catalog_item_id', catalog_cqrs_contract.hints.CatalogItemId)


class TestUserQuery(ITestQueryContract[UserQuery]):
    def test_query_contract(self) -> None:
        assert_attribute(UserQuery, 'user_id', user_identity_cqrs_contract.hints.UserId)

    def test_query_response_contract(self) -> None:
        response_type = UserQuery.__response_type__()

        assert response_type == UserDTO

        assert_attribute(UserDTO, 'name', user_identity_cqrs_contract.hints.UserName)


class TestCustomerBasketQuery(ITestQueryContract[CustomerBasketQuery]):
    def test_query_contract(self) -> None:
        assert_attribute(CustomerBasketQuery, 'customer_id', basket_cqrs_contract.hints.CustomerId)

    def test_query_response_contract(self) -> None:
        response_type = CustomerBasketQuery.__response_type__()

        assert response_type == CustomerBasketDTO

        # на данный момент мы не используем никакие поля, потому проверяем только response_type
