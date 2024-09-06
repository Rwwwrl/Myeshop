from typing import List, Union

from basket_cqrs_contract.command import UpdateCustomerBasketCommand
from basket_cqrs_contract.customer_basket_dto import BasketItemDTO, CustomerBasketDTO
from basket_cqrs_contract.query import CustomerBasketQuery

from catalog_cqrs_contract.query import CatalogItemsByIdsQuery
from catalog_cqrs_contract.query.query_response import CatalogItemDTO

from framework.for_pytests.for_testing_cqrs_contract_usage import (
    ITestQueryContract,
    ITestSyncCommandContract,
    assert_attribute,
)


class TestCatalogItemByIdsQuery(ITestQueryContract[CatalogItemsByIdsQuery]):
    def test_query_contract(self):
        assert_attribute(CatalogItemsByIdsQuery, 'ids', List[int])

    def test_query_response_contract(self):
        response_type = CatalogItemsByIdsQuery.__response_type__()

        assert response_type == List[CatalogItemDTO]
        assert_attribute(CatalogItemDTO, 'id', int)
        assert_attribute(CatalogItemDTO, 'name', str)
        assert_attribute(CatalogItemDTO, 'price', float)
        assert_attribute(CatalogItemDTO, 'discount', int)
        assert_attribute(CatalogItemDTO, 'picture_url', str)


class TestUpdateCustomerBasketCommand(ITestSyncCommandContract[UpdateCustomerBasketCommand]):
    def test_command_contract(self) -> None:
        assert_attribute(UpdateCustomerBasketCommand, 'customer_basket', CustomerBasketDTO)

        assert_attribute(CustomerBasketDTO, 'basket_items', List[BasketItemDTO])

        assert_attribute(BasketItemDTO, 'id', Union[int, None])
        assert_attribute(BasketItemDTO, 'product_id', int)
        assert_attribute(BasketItemDTO, 'product_name', str)
        assert_attribute(BasketItemDTO, 'quantity', int)
        assert_attribute(BasketItemDTO, 'discount', int)
        assert_attribute(BasketItemDTO, 'picture_url', str)

    def test_command_response_contract(self) -> None:
        # мы не используем ответ от команды
        pass


class TestCustomerBasketQuery(ITestQueryContract[CustomerBasketQuery]):
    def test_query_contract(self) -> None:
        assert_attribute(CustomerBasketQuery, 'customer_id', int)

    def test_query_response_contract(self) -> None:
        response_type = CustomerBasketQuery.__response_type__()

        assert response_type == CustomerBasketDTO
        assert_attribute(CustomerBasketDTO, 'basket_items', List[BasketItemDTO])

        assert_attribute(BasketItemDTO, 'id', Union[int, None])
        assert_attribute(BasketItemDTO, 'product_id', int)
        assert_attribute(BasketItemDTO, 'product_name', str)
        assert_attribute(BasketItemDTO, 'unit_price', float)
        assert_attribute(BasketItemDTO, 'quantity', int)
        assert_attribute(BasketItemDTO, 'picture_url', str)
