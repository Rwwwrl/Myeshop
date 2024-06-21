from typing import List

import pytest

from pytest_check import check

import basket_cqrs_contract.command.command
import basket_cqrs_contract.hints
from basket_cqrs_contract.command import UpdateCustomerBasketCommand
from basket_cqrs_contract.query import CustomerBasketQuery
from basket_cqrs_contract.query.query_response import BasketItemDTO, CustomerBasketDTO

import catalog_cqrs_contract.hints
from catalog_cqrs_contract.query import CatalogItemsByIdsQuery
from catalog_cqrs_contract.query.query_response import CatalogItemDTO

from framework.for_pytests.for_testing_cqrs_contract_usage import (
    ITestCommandContract,
    ITestQueryContract,
    assert_attribute,
)


@pytest.mark.cqrs_contract_usage
class TestCatalogItemByIdsQuery(ITestQueryContract[CatalogItemsByIdsQuery]):
    def test_query_contract(self):
        with check:
            assert_attribute(CatalogItemsByIdsQuery, 'ids', List[catalog_cqrs_contract.hints.CatalogItemId])

    def test_query_response_contract(self):
        response_type = CatalogItemsByIdsQuery.__response_type__()

        with check:
            assert response_type == List[CatalogItemDTO]
            assert_attribute(CatalogItemDTO, 'id', catalog_cqrs_contract.hints.CatalogItemId)
            assert_attribute(CatalogItemDTO, 'name', str)
            assert_attribute(CatalogItemDTO, 'price', float)
            assert_attribute(CatalogItemDTO, 'picture_url', str)


class TestUpdateCustomerBasketCommand(ITestCommandContract[UpdateCustomerBasketCommand]):
    def test_command_contract(self) -> None:
        with check:
            assert_attribute(
                UpdateCustomerBasketCommand,
                'buyer_id',
                basket_cqrs_contract.hints.CustomerId,
            )
            assert_attribute(
                UpdateCustomerBasketCommand,
                'basket_items',
                List[basket_cqrs_contract.command.command.BasketItemDTO],
            )
            assert_attribute(
                basket_cqrs_contract.command.command.BasketItemDTO,
                'product_id',
                basket_cqrs_contract.hints.ProductId,
            )
            assert_attribute(
                basket_cqrs_contract.command.command.BasketItemDTO,
                'product_name',
                basket_cqrs_contract.hints.ProductName,
            )
            assert_attribute(
                basket_cqrs_contract.command.command.BasketItemDTO,
                'quantity',
                basket_cqrs_contract.hints.Quantity,
            )
            assert_attribute(
                basket_cqrs_contract.command.command.BasketItemDTO,
                'picture_url',
                basket_cqrs_contract.hints.PictureUrl,
            )

    def test_command_response_contract(self) -> None:
        # мы не используем ответ от команды
        pass

