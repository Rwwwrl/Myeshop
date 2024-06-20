from typing import List

from fastapi import status

from mock import Mock, patch

import pytest

import pytest_lazyfixture

from api_gateway.mediator.views.http.basket.api_router import api_router
from api_gateway.mediator.views.http.basket.update_basket import update_basket
from api_gateway.mediator.views.http.basket.update_basket.dto import (
    UpdateBasketRequestData,
    UpdateBasketRequestItemData,
)

from basket_cqrs_contract.command import UpdateCustomerBasketCommand
from basket_cqrs_contract.command.command import BasketItemDTO

from catalog_cqrs_contract.query.query import CatalogItemsByIdsQuery
from catalog_cqrs_contract.query.query_response import CatalogBrandDTO, CatalogItemDTO, CatalogTypeDTO

from framework.for_pytests.test_case import TestCase
from framework.for_pytests.test_class import TestClass


class UpdateBasketTestCase(TestCase):
    request_data: UpdateBasketRequestData
    mock__catalog_item_by_ids_query__fetch__return_value: List[CatalogItemDTO]
    update_customerer_basket_command_init_call_args: dict
    expected_response_status_code: int


@pytest.fixture(scope='session')
def test_case_success() -> UpdateBasketTestCase:
    request_data = UpdateBasketRequestData(
        buyer_id=1,
        basket_items=[
            UpdateBasketRequestItemData(
                product_id=1,
                quantity=1,
            ),
            UpdateBasketRequestItemData(
                product_id=2,
                quantity=2,
            ),
        ],
    )

    mock__catalog_item_by_ids_query__fetch__return_value = [
        CatalogItemDTO(
            id=1,
            name='name1',
            description='description1',
            price=100,
            picture_filename='picture_filename1',
            picture_url='picture_url1',
            catalog_type=CatalogTypeDTO(
                id=1,
                type='type1',
            ),
            catalog_brand=CatalogBrandDTO(
                id=1,
                brand='brand1',
            ),
            available_stock=10,
            restock_threshold=5,
            maxstock_threshold=15,
            on_reorder=False,
        ),
        CatalogItemDTO(
            id=2,
            name='name2',
            description='description2',
            price=200,
            picture_filename='picture_filename2',
            picture_url='picture_url2',
            catalog_type=CatalogTypeDTO(
                id=1,
                type='type1',
            ),
            catalog_brand=CatalogBrandDTO(
                id=1,
                brand='brand1',
            ),
            available_stock=10,
            restock_threshold=5,
            maxstock_threshold=15,
            on_reorder=False,
        ),
    ]

    update_customerer_basket_command_init_call_args = {
        'buyer_id':
            1,
        'basket_items':
            [
                BasketItemDTO(
                    product_id=1,
                    product_name='name1',
                    unit_price=100,
                    quantity=1,
                    picture_url='picture_url1',
                ),
                BasketItemDTO(
                    product_id=2,
                    product_name='name2',
                    unit_price=200,
                    quantity=2,
                    picture_url='picture_url2',
                ),
            ],
    }

    return UpdateBasketTestCase(
        request_data=request_data,
        mock__catalog_item_by_ids_query__fetch__return_value=mock__catalog_item_by_ids_query__fetch__return_value,
        update_customerer_basket_command_init_call_args=update_customerer_basket_command_init_call_args,
        expected_response_status_code=status.HTTP_200_OK,
    )


@pytest.fixture(scope='session')
def test_case_400_basket_must_have_at_least_one_basket_item() -> UpdateBasketTestCase:
    return UpdateBasketTestCase()


@pytest.fixture(scope='session')
def test_case_400_basket_refer_to_non_existing_products() -> UpdateBasketTestCase:
    return UpdateBasketTestCase()


@pytest.fixture(scope='session')
def test_case_500_failed_to_update_basket_due_to_UpdateCustomerBasketCommand_failed() -> UpdateBasketTestCase:
    return UpdateBasketTestCase()


@pytest.fixture(
    scope='session',
    params=[
        pytest_lazyfixture.lazy_fixture(test_case_success.__name__),
    ],
)
def test_case(request) -> UpdateBasketTestCase:
    return request.param


class TestUrlToView(TestClass[update_basket]):
    def test(self):
        expected_url = '/api_gateway/basket/basket/'
        fact_url = api_router.url_path_for('update_basket')
        assert fact_url == expected_url


class TestUpdateBasket(TestClass[update_basket]):

    URL_TO_VIEW = '/api_gateway/basket/basket/'

    @patch.object(UpdateCustomerBasketCommand, 'execute')
    @patch.object(UpdateCustomerBasketCommand, '__init__')
    @patch.object(CatalogItemsByIdsQuery, 'fetch')
    def test(
        self,
        mock__catalog_item_by_ids_query__fetch: Mock,
        mock__update_customer_basket_command__init: Mock,
        mock__update_customer_basket_command__execute: Mock,
        test_case: UpdateBasketTestCase,
    ):
        mock__update_customer_basket_command__init.return_value = None
        mock__catalog_item_by_ids_query__fetch.return_value = (
            test_case.mock__catalog_item_by_ids_query__fetch__return_value
        )

        response = update_basket(request_data=test_case.request_data, user_id=1)
        assert response.status_code == test_case.expected_response_status_code

        mock__update_customer_basket_command__init.assert_called_once_with(
            **test_case.update_customerer_basket_command_init_call_args,
        )
