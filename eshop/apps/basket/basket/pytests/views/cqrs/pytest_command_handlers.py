from typing import cast

from mock import MagicMock, Mock, patch

import pytest

from basket.domain.models.customer_basket import (
    CustomerBasketORM,
    PostgresCustomerBasketRepository,
)
from basket.domain.models.customer_basket.customer_basket import (
    BasketItem,
    Data,
)
from basket.views.cqrs import command_handlers
from basket.views.cqrs.command_handlers import UpdateCustomerBasketCommandHandler

from basket_cqrs_contract.command import UpdateCustomerBasketCommand
from basket_cqrs_contract.customer_basket_dto import BasketItemDTO, CustomerBasketDTO

from framework.for_pytests.test_case import TestCase
from framework.for_pytests.test_class import TestClass
from framework.sqlalchemy.session import Session


class TestCaseSucess(TestCase['TestUpdateCustomerBasketCommandHandler__handle']):
    command: UpdateCustomerBasketCommand
    expected_updated_customer_basket: CustomerBasketORM


@pytest.fixture(scope='session')
def test_case_success() -> TestCaseSucess:
    command = UpdateCustomerBasketCommand(
        customer_basket=CustomerBasketDTO(
            buyer_id=1,
            basket_items=[
                BasketItemDTO(
                    id=1,
                    product_id=1,
                    product_name='product_name1',
                    unit_price=10,
                    quantity=10,
                    discount=15,
                    picture_url='picture_url1',
                ),
                BasketItemDTO(
                    id=2,
                    product_id=2,
                    product_name='product_name2',
                    unit_price=20,
                    quantity=20,
                    discount=25,
                    picture_url='picture_url2',
                ),
            ],
        ),
    )

    expected_updated_customer_basket = CustomerBasketORM(
        buyer_id=1,
        data=Data(
            basket_items=[
                BasketItem(
                    id=1,
                    product_id=1,
                    product_name='product_name1',
                    unit_price=10,
                    quantity=10,
                    discount=15,
                    picture_url='picture_url1',
                ),
                BasketItem(
                    id=2,
                    product_id=2,
                    product_name='product_name2',
                    unit_price=20,
                    quantity=20,
                    discount=25,
                    picture_url='picture_url2',
                ),
            ],
        ),
    )

    return TestCaseSucess(
        command=command,
        expected_updated_customer_basket=expected_updated_customer_basket,
    )


class TestUpdateCustomerBasketCommandHandler__handle(TestClass[UpdateCustomerBasketCommandHandler]):
    @patch.object(command_handlers, 'Session', new=MagicMock(spec=Session))
    @patch.object(PostgresCustomerBasketRepository, PostgresCustomerBasketRepository.save.__name__)
    def test_case_success(
        self,
        mock__postgres_customer_basket_repository__save: Mock,
        test_case_success: TestCaseSucess,
    ):
        test_case = test_case_success

        UpdateCustomerBasketCommandHandler().handle(command=test_case.command)

        fact_updated_customer_basket = cast(
            CustomerBasketORM,
            mock__postgres_customer_basket_repository__save.call_args_list[0].kwargs['customer_basket_orm'],
        )
        assert fact_updated_customer_basket.buyer_id == test_case.expected_updated_customer_basket.buyer_id
        assert fact_updated_customer_basket.data == test_case.expected_updated_customer_basket.data
