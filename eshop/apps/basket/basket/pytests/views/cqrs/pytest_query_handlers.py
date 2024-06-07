from mock import Mock, patch

import pytest

from basket.domain.models.basketitem import BasketItem as BasketItemORM
from basket.domain.models.customer_basket import (
    CustomerBasket as CustomerBasketORM,
    CustomerBasketRepository,
)
from basket.views.cqrs.query_handlers import CustomerBasketQueryHandler

from basket_cqrs_contract.query import CustomerBasketQuery
from basket_cqrs_contract.query.query_response import BasketItemDTO, CustomerBasketDTO

from framework.for_pytests.test_class import TestClass
from framework.for_pytests.use_case import UseCase


class UseCaseBasketByIdQueryHandler__handle(UseCase):
    query: CustomerBasketQuery
    mock_customer_basket_repository_get_by_id_return_value: CustomerBasketORM
    expected_result: CustomerBasketDTO


@pytest.fixture(scope='session')
def use_case_basket_by_id_query_handler__handle() -> UseCaseBasketByIdQueryHandler__handle:
    query = CustomerBasketQuery(customer_id=1)
    mock_repository_get_by_id_return_value = CustomerBasketORM(
        buyer_id=10,
        basket_items=[
            BasketItemORM(
                id=1,
                basket_buyer_id=10,
                product_id=2,
                product_name='product_name1',
                unit_price=10,
                quantity=3,
                picture_url='picture_url1',
            ),
            BasketItemORM(
                id=2,
                basket_buyer_id=10,
                product_id=3,
                product_name='product_name2',
                unit_price=15,
                quantity=2,
                picture_url='picture_url2',
            ),
        ],
    )

    expected_result = CustomerBasketDTO(
        buyer_id=10,
        basket_items=[
            BasketItemDTO(
                id=1,
                product_id=2,
                product_name='product_name1',
                unit_price=10,
                quantity=3,
                picture_url='picture_url1',
            ),
            BasketItemDTO(
                id=2,
                product_id=3,
                product_name='product_name2',
                unit_price=15,
                quantity=2,
                picture_url='picture_url2',
            ),
        ],
    )

    return UseCaseBasketByIdQueryHandler__handle(
        query=query,
        mock_customer_basket_repository_get_by_id_return_value=mock_repository_get_by_id_return_value,
        expected_result=expected_result,
    )


class TestBasketByIdQueryHandler__handle(TestClass[CustomerBasketQueryHandler.handle]):
    @patch.object(CustomerBasketRepository, 'get_by_buyer_id')
    def test(
        self,
        mock__customer_basket_repository__get_by_id: Mock,
        use_case_basket_by_id_query_handler__handle: UseCaseBasketByIdQueryHandler__handle,
    ):
        use_case = use_case_basket_by_id_query_handler__handle

        mock__customer_basket_repository__get_by_id.return_value = (
            use_case.mock_customer_basket_repository_get_by_id_return_value
        )

        result = CustomerBasketQueryHandler().handle(query=use_case.query)
        assert use_case.expected_result == result
