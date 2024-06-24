from fastapi import HTTPException, status

from mock import Mock, patch

import pytest

from api_gateway.mediator.views.http.basket.api_router import api_router
from api_gateway.mediator.views.http.basket.update_quantities import update_quantities
from api_gateway.mediator.views.http.basket.update_quantities.dto import (
    UpdateBasketItemData,
    UpdateBasketItemsRequest,
)

import basket_cqrs_contract.command.command
import basket_cqrs_contract.query.query_response
from basket_cqrs_contract.command import UpdateCustomerBasketCommand
from basket_cqrs_contract.query import CustomerBasketQuery

from framework.cqrs.exceptions import CQRSException
from framework.for_pytests.for_testing_http_views import ExpectedHttpResponse, ExpectedHttpResponseException
from framework.for_pytests.test_case import TestCase
from framework.for_pytests.test_class import TestClass

import user_identity.hints


class TestCaseSuccess(TestCase['TestViewUpdateQuantities']):
    user_id: user_identity.hints.UserId
    request_data: UpdateBasketItemsRequest
    mock__customer_basket_query__fetch__return_value: basket_cqrs_contract.query.query_response.CustomerBasketDTO
    expected_http_response: ExpectedHttpResponse
    expected_update_customer_basket_command_call_args: dict


class TestCaseNotUpdatesSent(TestCase['TestViewUpdateQuantities']):

    request_data: UpdateBasketItemsRequest
    expected_http_response_exception: ExpectedHttpResponseException


class TestCase500FailedToUpdateBasketDueToUpdateCustomerBasketCommandFailed(TestCase['TestViewUpdateQuantities']):
    user_id: user_identity.hints.UserId
    request_data: UpdateBasketItemsRequest
    expected_http_response_exception: ExpectedHttpResponseException
    mock__customer_basket_query__fetch__return_value: basket_cqrs_contract.query.query_response.CustomerBasketDTO
    expected_update_customer_basket_command_call_args: dict


@pytest.fixture(scope='session')
def test_case_success() -> TestCaseSuccess:
    user_id = 1

    request_data = UpdateBasketItemsRequest(
        updates=[
            UpdateBasketItemData(
                basket_item_id=1,
                new_quantity=10,
            ),
            UpdateBasketItemData(
                basket_item_id=2,
                new_quantity=20,
            ),
        ],
    )

    mock__customer_basket_query__fetch__return_value = basket_cqrs_contract.query.query_response.CustomerBasketDTO(
        buyer_id=1,
        basket_items=[
            basket_cqrs_contract.query.query_response.BasketItemDTO(
                id=1,
                product_id=1,
                product_name='product_name1',
                unit_price=10,
                quantity=1,
                picture_url='picture_url1',
            ),
            basket_cqrs_contract.query.query_response.BasketItemDTO(
                id=2,
                product_id=2,
                product_name='product_name2',
                unit_price=20,
                quantity=2,
                picture_url='picture_url2',
            ),
        ],
    )

    expected_update_customer_basket_command_call_args = {
        'buyer_id':
            1,
        'basket_items':
            [
                basket_cqrs_contract.command.command.BasketItemDTO(
                    product_id=1,
                    product_name='product_name1',
                    unit_price=10,
                    quantity=10,
                    picture_url='picture_url1',
                ),
                basket_cqrs_contract.command.command.BasketItemDTO(
                    product_id=2,
                    product_name='product_name2',
                    unit_price=20,
                    quantity=20,
                    picture_url='picture_url2',
                ),
            ],
    }

    return TestCaseSuccess(
        user_id=user_id,
        request_data=request_data,
        expected_http_response=ExpectedHttpResponse(
            status_code=status.HTTP_200_OK,
            body=b'',
        ),
        mock__customer_basket_query__fetch__return_value=mock__customer_basket_query__fetch__return_value,
        expected_update_customer_basket_command_call_args=expected_update_customer_basket_command_call_args,
    )


@pytest.fixture(scope='session')
def test_case_not_updates_sent() -> TestCase:
    return TestCaseNotUpdatesSent(
        request_data=UpdateBasketItemsRequest(updates=[]),
        expected_http_response_exception=ExpectedHttpResponseException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='no updates sent',
        ),
    )


@pytest.fixture(scope='session')
def test_case_500_failed_to_update_basket_due_to_UpdateCustomerBasketCommand_failed(
) -> TestCase500FailedToUpdateBasketDueToUpdateCustomerBasketCommandFailed:
    user_id = 1

    request_data = UpdateBasketItemsRequest(
        updates=[
            UpdateBasketItemData(
                basket_item_id=1,
                new_quantity=10,
            ),
            UpdateBasketItemData(
                basket_item_id=2,
                new_quantity=20,
            ),
        ],
    )

    mock__customer_basket_query__fetch__return_value = basket_cqrs_contract.query.query_response.CustomerBasketDTO(
        buyer_id=1,
        basket_items=[
            basket_cqrs_contract.query.query_response.BasketItemDTO(
                id=1,
                product_id=1,
                product_name='product_name1',
                unit_price=10,
                quantity=1,
                picture_url='picture_url1',
            ),
            basket_cqrs_contract.query.query_response.BasketItemDTO(
                id=2,
                product_id=2,
                product_name='product_name2',
                unit_price=20,
                quantity=2,
                picture_url='picture_url2',
            ),
        ],
    )

    expected_update_customer_basket_command_call_args = {
        'buyer_id':
            1,
        'basket_items':
            [
                basket_cqrs_contract.command.command.BasketItemDTO(
                    product_id=1,
                    product_name='product_name1',
                    unit_price=10,
                    quantity=10,
                    picture_url='picture_url1',
                ),
                basket_cqrs_contract.command.command.BasketItemDTO(
                    product_id=2,
                    product_name='product_name2',
                    unit_price=20,
                    quantity=20,
                    picture_url='picture_url2',
                ),
            ],
    }

    return TestCase500FailedToUpdateBasketDueToUpdateCustomerBasketCommandFailed(
        user_id=user_id,
        request_data=request_data,
        expected_http_response_exception=ExpectedHttpResponseException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f'failed to update basket due to {UpdateCustomerBasketCommand.__name__} failed',
        ),
        mock__customer_basket_query__fetch__return_value=mock__customer_basket_query__fetch__return_value,
        expected_update_customer_basket_command_call_args=expected_update_customer_basket_command_call_args,
    )


class TestUrlToView(TestClass[update_quantities]):
    def test(self):
        expected_url = '/api_gateway/basket/basket/basket_items/'
        fact_url = api_router.url_path_for(update_quantities.__name__)
        assert fact_url == expected_url


class TestViewUpdateQuantities(TestClass[update_quantities]):
    @patch.object(UpdateCustomerBasketCommand, 'execute')
    @patch.object(UpdateCustomerBasketCommand, '__init__')
    @patch.object(CustomerBasketQuery, 'fetch')
    def test_case_success(
        self,
        mock__customer_basket_query__fetch: Mock,
        mock__update_customer_basket_command__init: Mock,
        mock__update_customer_basket_command__execute: Mock,
        test_case_success: TestCaseSuccess,
    ):
        test_case = test_case_success

        mock__customer_basket_query__fetch.return_value = test_case.mock__customer_basket_query__fetch__return_value

        mock__update_customer_basket_command__init.return_value = None

        response = update_quantities(test_case.request_data, user_id=test_case.user_id)
        assert response.status_code == test_case.expected_http_response.status_code
        assert response.body == test_case.expected_http_response.body

        mock__update_customer_basket_command__init.assert_called_once_with(
            **test_case.expected_update_customer_basket_command_call_args,
        )
        mock__update_customer_basket_command__execute.assert_called_once()

    def test_case_not_updates_sent(self, test_case_not_updates_sent: TestCaseNotUpdatesSent):
        test_case = test_case_not_updates_sent

        try:
            update_quantities(request_data=test_case.request_data, user_id=1)
        except HTTPException as e:
            assert e.status_code == test_case.expected_http_response_exception.status_code
            assert e.detail == test_case.expected_http_response_exception.detail

    @patch.object(UpdateCustomerBasketCommand, 'execute')
    @patch.object(UpdateCustomerBasketCommand, '__init__')
    @patch.object(CustomerBasketQuery, 'fetch')
    def test_case_500_failed_to_update_basket_due_to_UpdateCustomerBasketCommand_failed(
        self,
        mock__customer_basket_query__fetch: Mock,
        mock__update_customer_basket_command__init: Mock,
        mock__update_customer_basket_command__execute: Mock,
        test_case_500_failed_to_update_basket_due_to_UpdateCustomerBasketCommand_failed:
        TestCase500FailedToUpdateBasketDueToUpdateCustomerBasketCommandFailed,
    ):
        test_case = test_case_500_failed_to_update_basket_due_to_UpdateCustomerBasketCommand_failed

        mock__customer_basket_query__fetch.return_value = test_case.mock__customer_basket_query__fetch__return_value

        mock__update_customer_basket_command__init.return_value = None

        mock__update_customer_basket_command__execute.side_effect = CQRSException

        try:
            update_quantities(test_case.request_data, user_id=test_case.user_id)
        except HTTPException as e:
            assert e.status_code == test_case.expected_http_response_exception.status_code
            assert e.detail == test_case.expected_http_response_exception.detail

        mock__update_customer_basket_command__init.assert_called_once_with(
            **test_case.expected_update_customer_basket_command_call_args,
        )
        mock__update_customer_basket_command__execute.assert_called_once()
