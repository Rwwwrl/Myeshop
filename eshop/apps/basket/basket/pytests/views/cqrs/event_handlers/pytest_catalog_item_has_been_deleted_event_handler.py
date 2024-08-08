from typing import List, cast

from mock import Mock, patch

import pytest

from basket.infrastructure.persistence.postgres.customer_basket import (
    CustomerBasketORM,
    PostgresCustomerBasketRepository,
)
from basket.infrastructure.persistence.postgres.customer_basket.customer_basket_orm import BasketItem, Data
from basket.views.cqrs.event_handlers import CatalogItemHasBeenDeletedEventHandler

from catalog_cqrs_contract.event import CatalogItemHasBeenDeletedEvent

from framework.cqrs.context import InsideSqlachemyTransactionContext
from framework.for_pytests.test_case import TestCase as _TestCase
from framework.for_pytests.test_class import TestClass
from framework.sqlalchemy.session import Session


class TestCase(_TestCase['TestCatalogItemHasBeenDeletedEventHandler__handle']):
    event: CatalogItemHasBeenDeletedEvent
    mock__customer_basket_repository__all__return_value: List[CustomerBasketORM]
    expected_customer_basket_repository_calls: List[CustomerBasketORM]


@pytest.fixture(scope='session')
def test_case() -> TestCase:
    event = CatalogItemHasBeenDeletedEvent(
        catalog_item_id=1,
        context=InsideSqlachemyTransactionContext(session=Session()),
    )

    mock__customer_basket_repository__all__return_value: List[CustomerBasketORM] = [
        CustomerBasketORM(
            buyer_id=1,
            data=Data(
                basket_items=[
                    BasketItem(
                        id=1,
                        product_id=1,
                        product_name='product_name1',
                        unit_price=10,
                        quantity=1,
                        picture_url='picture_url1',
                    ),
                    BasketItem(
                        id=2,
                        product_id=2,
                        product_name='product_name2',
                        unit_price=15,
                        quantity=2,
                        picture_url='picture_url2',
                    ),
                ],
            ),
        ),
        CustomerBasketORM(
            buyer_id=2,
            data=Data(
                basket_items=[
                    BasketItem(
                        id=1,
                        product_id=2,
                        product_name='product_name2',
                        unit_price=15,
                        quantity=2,
                        picture_url='picture_url2',
                    ),
                ],
            ),
        ),
        CustomerBasketORM(
            buyer_id=3,
            data=Data(
                basket_items=[
                    BasketItem(
                        id=1,
                        product_id=1,
                        product_name='product_name1',
                        unit_price=9,
                        quantity=1,
                        picture_url='picture_url1',
                    ),
                    BasketItem(
                        id=2,
                        product_id=2,
                        product_name='product_name2',
                        unit_price=15,
                        quantity=2,
                        picture_url='picture_url2',
                    ),
                ],
            ),
        ),
    ]

    expected_customer_basket_repository_calls: List[CustomerBasketORM] = [
        CustomerBasketORM(
            buyer_id=1,
            data=Data(
                basket_items=[
                    BasketItem(
                        id=2,
                        product_id=2,
                        product_name='product_name2',
                        unit_price=15,
                        quantity=2,
                        picture_url='picture_url2',
                    ),
                ],
            ),
        ),
        CustomerBasketORM(
            buyer_id=3,
            data=Data(
                basket_items=[
                    BasketItem(
                        id=2,
                        product_id=2,
                        product_name='product_name2',
                        unit_price=15,
                        quantity=2,
                        picture_url='picture_url2',
                    ),
                ],
            ),
        ),
    ]

    return TestCase(
        event=event,
        mock__customer_basket_repository__all__return_value=mock__customer_basket_repository__all__return_value,
        expected_customer_basket_repository_calls=expected_customer_basket_repository_calls,
    )


class TestCatalogItemHasBeenDeletedEventHandler__handle(TestClass[CatalogItemHasBeenDeletedEventHandler.handle]):
    @patch.object(PostgresCustomerBasketRepository, 'save')
    @patch.object(PostgresCustomerBasketRepository, 'all')
    def test_case(
        self,
        mock__customer_basket_repository__all: Mock,
        mock__customer_basket_repository__save: Mock,
        test_case: TestCase,
    ):
        mock__customer_basket_repository__all.return_value = (
            test_case.mock__customer_basket_repository__all__return_value
        )

        mock__customer_basket_repository__save.return_value = None

        CatalogItemHasBeenDeletedEventHandler().handle(event=test_case.event)

        assert mock__customer_basket_repository__save.call_count == 2
        for call, expected_call_arg in zip(
            mock__customer_basket_repository__save.call_args_list,
            test_case.expected_customer_basket_repository_calls,
        ):
            fact_call = cast(CustomerBasketORM, call.kwargs['customer_basket_orm'])
            assert fact_call.buyer_id == expected_call_arg.buyer_id
            assert fact_call.data == expected_call_arg.data
