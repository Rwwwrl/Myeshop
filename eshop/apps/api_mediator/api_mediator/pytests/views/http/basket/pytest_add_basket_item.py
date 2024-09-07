from typing import Any, List

from fastapi import HTTPException, status

from mock import Mock, patch

import pytest

from api_mediator.views.http.basket.add_basket_item import add_basket_item
from api_mediator.views.http.basket.add_basket_item.dto import AddBasketItemRequest

from basket_cqrs_contract.command import UpdateCustomerBasketCommand
from basket_cqrs_contract.customer_basket_dto import BasketItemDTO, CustomerBasketDTO
from basket_cqrs_contract.query import CustomerBasketQuery

import catalog_cqrs_contract.query.query_response
from catalog_cqrs_contract.query import CatalogItemsByIdsQuery

from framework.cqrs.exceptions import CQRSException
from framework.for_pytests.for_testing_http_views import ExpectedHttpResponse, ExpectedHttpResponseException
from framework.for_pytests.test_case import TestCase
from framework.for_pytests.test_class import TestClass

import user_identity_cqrs_contract.hints


class TestCaseBasketDoesNotHaveBasketItem(TestCase['TestViewAddBasketItem']):
    request_data: AddBasketItemRequest
    user_id: user_identity_cqrs_contract.hints.UserId
    mock__customer_basket_query__fetch__return_value: CustomerBasketDTO
    mock__catalog_items_by_ids_query__fetch__return_value: List[
        catalog_cqrs_contract.query.query_response.CatalogItemDTO,
    ]
    expected_executed_command: UpdateCustomerBasketCommand
    expected_http_response: ExpectedHttpResponse


class TestCaseBasketAlreadyHaveBasketItem(TestCase['TestViewAddBasketItem']):
    request_data: AddBasketItemRequest
    user_id: user_identity_cqrs_contract.hints.UserId
    mock__customer_basket_query__fetch__return_value: CustomerBasketDTO
    expected_executed_command: UpdateCustomerBasketCommand
    expected_http_response: ExpectedHttpResponse


class TestCaseUpdateCustomerBasketCommandExecuteCqrsException(TestCase['TestViewAddBasketItem']):
    request_data: AddBasketItemRequest
    user_id: user_identity_cqrs_contract.hints.UserId
    mock__customer_basket_query__fetch__return_value: CustomerBasketDTO
    expected_executed_command: UpdateCustomerBasketCommand
    expected_http_response_exception: ExpectedHttpResponseException


@pytest.fixture(scope='session')
def test_case_basket_does_not_have_basket_item() -> TestCaseBasketDoesNotHaveBasketItem:
    request_data = AddBasketItemRequest(
        catalog_item_id=3,
        quantity=3,
    )

    user_id = 1

    mock__customer_basket_query__fetch__return_value = CustomerBasketDTO(
        buyer_id=1,
        basket_items=[
            BasketItemDTO(
                id=1,
                product_id=1,
                product_name='product_name1',
                unit_price=10,
                quantity=5,
                discount=10,
                picture_url='picture_url1',
            ),
            BasketItemDTO(
                id=2,
                product_id=2,
                product_name='product_name2',
                unit_price=20,
                quantity=1,
                discount=15,
                picture_url='picture_url2',
            ),
        ],
    )

    mock__catalog_items_by_ids_query__fetch__return_value = [
        catalog_cqrs_contract.query.query_response.CatalogItemDTO(
            id=3,
            name='product_name3',
            description='description',
            price=10,
            picture_filename='picture_filename',
            discount=20,
            picture_url='picture_url3',
            catalog_type=catalog_cqrs_contract.query.query_response.CatalogTypeDTO(
                id=1,
                type='type',
            ),
            catalog_brand=catalog_cqrs_contract.query.query_response.CatalogBrandDTO(
                id=1,
                brand='brand',
            ),
            available_stock=10,
            maxstock_threshold=15,
            on_reorder=False,
            restock_threshold=13,
        ),
    ]

    expected_executed_command = UpdateCustomerBasketCommand(
        customer_basket=CustomerBasketDTO(
            buyer_id=1,
            basket_items=[
                BasketItemDTO(
                    id=1,
                    product_id=1,
                    product_name='product_name1',
                    unit_price=10,
                    quantity=5,
                    discount=10,
                    picture_url='picture_url1',
                ),
                BasketItemDTO(
                    id=2,
                    product_id=2,
                    product_name='product_name2',
                    unit_price=20,
                    quantity=1,
                    discount=15,
                    picture_url='picture_url2',
                ),
                BasketItemDTO(
                    id=None,
                    product_id=3,
                    product_name='product_name3',
                    unit_price=10,
                    quantity=3,
                    discount=20,
                    picture_url='picture_url3',
                ),
            ],
        ),
    )

    return TestCaseBasketDoesNotHaveBasketItem(
        request_data=request_data,
        user_id=user_id,
        mock__customer_basket_query__fetch__return_value=mock__customer_basket_query__fetch__return_value,
        mock__catalog_items_by_ids_query__fetch__return_value=mock__catalog_items_by_ids_query__fetch__return_value,
        expected_executed_command=expected_executed_command,
        expected_http_response=ExpectedHttpResponse(
            status_code=status.HTTP_200_OK,
            body=b'',
        ),
    )


@pytest.fixture(scope='session')
def test_case_basket_already_have_basket_item() -> TestCaseBasketAlreadyHaveBasketItem:
    request_data = AddBasketItemRequest(
        catalog_item_id=1,
        quantity=3,
    )

    user_id = 1

    mock__customer_basket_query__fetch__return_value = CustomerBasketDTO(
        buyer_id=1,
        basket_items=[
            BasketItemDTO(
                id=1,
                product_id=1,
                product_name='product_name1',
                unit_price=10,
                quantity=5,
                discount=10,
                picture_url='picture_url1',
            ),
            BasketItemDTO(
                id=2,
                product_id=2,
                product_name='product_name2',
                unit_price=20,
                quantity=1,
                discount=15,
                picture_url='picture_url2',
            ),
        ],
    )

    expected_executed_command = UpdateCustomerBasketCommand(
        customer_basket=CustomerBasketDTO(
            buyer_id=1,
            basket_items=[
                BasketItemDTO(
                    id=1,
                    product_id=1,
                    product_name='product_name1',
                    unit_price=10,
                    quantity=8,
                    discount=10,
                    picture_url='picture_url1',
                ),
                BasketItemDTO(
                    id=2,
                    product_id=2,
                    product_name='product_name2',
                    unit_price=20,
                    quantity=1,
                    discount=15,
                    picture_url='picture_url2',
                ),
            ],
        ),
    )

    return TestCaseBasketAlreadyHaveBasketItem(
        request_data=request_data,
        user_id=user_id,
        mock__customer_basket_query__fetch__return_value=mock__customer_basket_query__fetch__return_value,
        expected_executed_command=expected_executed_command,
        expected_http_response=ExpectedHttpResponse(
            status_code=status.HTTP_200_OK,
            body=b'',
        ),
    )


@pytest.fixture(scope='session')
def test_case_update_customer_basket_command_execute_cqrs_exception() -> TestCaseBasketAlreadyHaveBasketItem:
    request_data = AddBasketItemRequest(
        catalog_item_id=1,
        quantity=3,
    )

    user_id = 1

    mock__customer_basket_query__fetch__return_value = CustomerBasketDTO(
        buyer_id=1,
        basket_items=[
            BasketItemDTO(
                id=1,
                product_id=1,
                product_name='product_name1',
                unit_price=10,
                quantity=5,
                discount=10,
                picture_url='picture_url1',
            ),
            BasketItemDTO(
                id=2,
                product_id=2,
                product_name='product_name2',
                unit_price=20,
                quantity=1,
                discount=15,
                picture_url='picture_url2',
            ),
        ],
    )

    expected_executed_command = UpdateCustomerBasketCommand(
        customer_basket=CustomerBasketDTO(
            buyer_id=1,
            basket_items=[
                BasketItemDTO(
                    id=1,
                    product_id=1,
                    product_name='product_name1',
                    unit_price=10,
                    quantity=8,
                    discount=10,
                    picture_url='picture_url1',
                ),
                BasketItemDTO(
                    id=2,
                    product_id=2,
                    product_name='product_name2',
                    unit_price=20,
                    quantity=1,
                    discount=15,
                    picture_url='picture_url2',
                ),
            ],
        ),
    )

    return TestCaseUpdateCustomerBasketCommandExecuteCqrsException(
        request_data=request_data,
        user_id=user_id,
        mock__customer_basket_query__fetch__return_value=mock__customer_basket_query__fetch__return_value,
        expected_executed_command=expected_executed_command,
        expected_http_response_exception=ExpectedHttpResponseException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f'failed to update basket due to {UpdateCustomerBasketCommand.__name__} failed',
        ),
    )


class TestViewAddBasketItem(TestClass[add_basket_item]):
    @staticmethod
    def _assert(fact: Any, expected: Any) -> None:
        assert fact == expected

    @patch.object(UpdateCustomerBasketCommand, UpdateCustomerBasketCommand.execute.__name__, autospec=True)
    @patch.object(CatalogItemsByIdsQuery, CatalogItemsByIdsQuery.fetch.__name__)
    @patch.object(CustomerBasketQuery, CustomerBasketQuery.fetch.__name__)
    def test_case_basket_does_not_have_basket_item(
        self,
        mock__customer_basket_query__fetch: Mock,
        mock__catalog_items_by_ids_query__fetch: Mock,
        mock__update_customer_basket_command__execute: Mock,
        test_case_basket_does_not_have_basket_item: TestCaseBasketDoesNotHaveBasketItem,
    ):
        test_case = test_case_basket_does_not_have_basket_item

        mock__customer_basket_query__fetch.return_value = test_case.mock__customer_basket_query__fetch__return_value

        mock__catalog_items_by_ids_query__fetch.return_value = (
            test_case.mock__catalog_items_by_ids_query__fetch__return_value
        )

        mock__update_customer_basket_command__execute.return_value = None

        response = add_basket_item(request_data=test_case.request_data, user_id=test_case.user_id)
        assert response.status_code == test_case.expected_http_response.status_code
        assert response.body == test_case.expected_http_response.body

        fact_called_command: UpdateCustomerBasketCommand = (
            mock__update_customer_basket_command__execute.call_args[0][0]
        )
        fact_customer_basket_arg = fact_called_command.customer_basket
        expected_customer_basket_arg = test_case.expected_executed_command.customer_basket
        assert fact_customer_basket_arg.buyer_id == expected_customer_basket_arg.buyer_id
        self._assert(
            set(fact_customer_basket_arg.basket_items),
            set(expected_customer_basket_arg.basket_items),
        )
        mock__update_customer_basket_command__execute.assert_called_once()

    @patch.object(UpdateCustomerBasketCommand, UpdateCustomerBasketCommand.execute.__name__, autospec=True)
    @patch.object(CustomerBasketQuery, CustomerBasketQuery.fetch.__name__)
    def test_case_basket_already_have_basket_item(
        self,
        mock__customer_basket_query__fetch: Mock,
        mock__update_customer_basket_command__execute: Mock,
        test_case_basket_already_have_basket_item: TestCaseBasketAlreadyHaveBasketItem,
    ):
        test_case = test_case_basket_already_have_basket_item

        mock__customer_basket_query__fetch.return_value = test_case.mock__customer_basket_query__fetch__return_value

        mock__update_customer_basket_command__execute.return_value = None

        response = add_basket_item(request_data=test_case.request_data, user_id=test_case.user_id)
        assert response.status_code == test_case.expected_http_response.status_code
        assert response.body == test_case.expected_http_response.body

        fact_called_command: UpdateCustomerBasketCommand = (
            mock__update_customer_basket_command__execute.call_args[0][0]
        )
        fact_customer_basket_arg = fact_called_command.customer_basket
        expected_customer_basket_arg = test_case.expected_executed_command.customer_basket
        assert fact_customer_basket_arg.buyer_id == expected_customer_basket_arg.buyer_id
        self._assert(
            set(fact_customer_basket_arg.basket_items),
            set(expected_customer_basket_arg.basket_items),
        )
        mock__update_customer_basket_command__execute.assert_called_once()

    @patch.object(UpdateCustomerBasketCommand, UpdateCustomerBasketCommand.execute.__name__, autospec=True)
    @patch.object(CustomerBasketQuery, CustomerBasketQuery.fetch.__name__)
    def test_case_update_customer_basket_command_execute_cqrs_exception(
        self,
        mock__customer_basket_query__fetch: Mock,
        mock__update_customer_basket_command__execute: Mock,
        test_case_update_customer_basket_command_execute_cqrs_exception:
        TestCaseUpdateCustomerBasketCommandExecuteCqrsException,
    ):
        test_case = test_case_update_customer_basket_command_execute_cqrs_exception

        mock__customer_basket_query__fetch.return_value = test_case.mock__customer_basket_query__fetch__return_value

        mock__update_customer_basket_command__execute.side_effect = CQRSException

        try:
            add_basket_item(request_data=test_case.request_data, user_id=test_case.user_id)
        except HTTPException as e:
            assert e.status_code == test_case.expected_http_response_exception.status_code
            assert e.detail == test_case.expected_http_response_exception.detail

        fact_called_command: UpdateCustomerBasketCommand = (
            mock__update_customer_basket_command__execute.call_args[0][0]
        )
        fact_customer_basket_arg = fact_called_command.customer_basket
        expected_customer_basket_arg = test_case.expected_executed_command.customer_basket
        assert fact_customer_basket_arg.buyer_id == expected_customer_basket_arg.buyer_id
        self._assert(
            set(fact_customer_basket_arg.basket_items),
            set(expected_customer_basket_arg.basket_items),
        )
        mock__update_customer_basket_command__execute.assert_called_once()
