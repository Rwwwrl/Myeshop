from datetime import date

from fastapi import status

from mock import Mock, patch

import pytest

from basket.app_config import BasketAppConfig
from basket.views.http.checkout import checkout
from basket.views.http.checkout.dto import BasketCheckoutRequestData

from basket_cqrs_contract.customer_basket_dto import BasketItemDTO, CustomerBasketDTO
from basket_cqrs_contract.event import UserCheckoutAcceptedEvent
from basket_cqrs_contract.query import CustomerBasketQuery

from framework.for_pytests.for_testing_http_views import ExpectedHttpResponse
from framework.for_pytests.test_case import TestCase as _TestCase
from framework.for_pytests.test_class import TestClass

from user_identity_cqrs_contract.hints import UserId
from user_identity_cqrs_contract.query import UserByIdQuery
from user_identity_cqrs_contract.query.query_response import UserDTO


class TestCase(_TestCase['TestCheckoutView']):
    request_data: BasketCheckoutRequestData
    user_id: UserId

    mock__user_query__fetch__return_value: UserDTO
    mock__customer_basket_query__fetch__return_value: CustomerBasketDTO

    expected_published_event: UserCheckoutAcceptedEvent

    expected_http_response: ExpectedHttpResponse


@pytest.fixture(scope='session')
def test_case() -> TestCase:
    request_data = BasketCheckoutRequestData(
        order_number=1,
        city='city',
        street='street',
        state='state',
        country='country',
        zip_code='zip_code',
        card_number='card_number',
        card_holder_name='card_holder_name',
        card_expiration=date(year=2000, month=1, day=2),
        card_security_number='card_security_number',
        card_type_id=1,
    )

    user_id = 1

    mock__customer_basket_query__fetch = CustomerBasketDTO(
        buyer_id=user_id,
        basket_items=[
            BasketItemDTO(
                id=1,
                product_id=1,
                product_name='product_name1',
                unit_price=10,
                quantity=20,
                picture_url='picture_url1',
            ),
            BasketItemDTO(
                id=2,
                product_id=2,
                product_name='product_name2',
                unit_price=10,
                quantity=20,
                picture_url='picture_url2',
            ),
        ],
    )

    mock__user_query__fetch = UserDTO(
        id=user_id,
        name='name',
    )

    expected_published_event = UserCheckoutAcceptedEvent(
        **request_data.model_dump(mode='python'),
        basket=mock__customer_basket_query__fetch,
        user_id=user_id,
        username=mock__user_query__fetch.name,
    )

    return TestCase(
        request_data=request_data,
        user_id=user_id,
        mock__customer_basket_query__fetch__return_value=mock__customer_basket_query__fetch,
        mock__user_query__fetch__return_value=mock__user_query__fetch,
        expected_published_event=expected_published_event,
        expected_http_response=ExpectedHttpResponse(
            status_code=status.HTTP_200_OK,
            body=b'',
        ),
    )


class TestUrlToView(TestClass[checkout]):
    def test(self):
        expected_url = '/basket/checkout/'
        fact_url = BasketAppConfig.get_api_router().url_path_for(checkout.__name__)
        assert fact_url == expected_url


class TestCheckoutView(TestClass[checkout]):
    @patch.object(UserByIdQuery, 'fetch')
    @patch.object(CustomerBasketQuery, 'fetch')
    @patch.object(UserCheckoutAcceptedEvent, 'publish', autospec=True)
    def test(
        self,
        mock__user_checkout_accepted_event__publish: Mock,
        mock__customer_basket_query__fetch: Mock,
        mock__user_query__fetch: Mock,
        test_case: TestCase,
    ):

        mock__user_query__fetch.return_value = test_case.mock__user_query__fetch__return_value
        mock__customer_basket_query__fetch.return_value = test_case.mock__customer_basket_query__fetch__return_value

        mock__user_checkout_accepted_event__publish.return_value = None

        response = checkout(request_data=test_case.request_data, user_id=test_case.user_id)
        assert response.status_code == test_case.expected_http_response.status_code
        assert response.body == test_case.expected_http_response.body

        fact_published_event: UserCheckoutAcceptedEvent = mock__user_checkout_accepted_event__publish.call_args[0][0]
        assert fact_published_event == test_case.expected_published_event
