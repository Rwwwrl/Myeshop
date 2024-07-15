from typing import cast

from mock import Mock, patch

import pytest

from typing_extensions import TypedDict

from basket.infrastructure.persistence.postgres.customer_basket import (
    CustomerBasketORM,
    PostgresCustomerBasketRepository,
)
from basket.infrastructure.persistence.postgres.customer_basket.customer_basket_orm import (
    BasketItem,
    Data,
)
from basket.views.cqrs import command_handlers
from basket.views.cqrs.command_handlers import UpdateCustomerBasketCommandHandler

from basket_cqrs_contract.command import UpdateCustomerBasketCommand
from basket_cqrs_contract.customer_basket_dto import BasketItemDTO, CustomerBasketDTO

from framework.for_pytests.sqlalchemy_session_mock import SqlalchemySessionMock
from framework.for_pytests.test_case import TestCase
from framework.for_pytests.test_class import TestClass


class ExpectedPostgresBasketRepositorySaveCallArgs(TypedDict):
    customer_basket_orm: CustomerBasketORM


class TestCaseSucess(TestCase['TestUpdateCustomerBasketCommandHandler__handle']):
    command: UpdateCustomerBasketCommand
    expected_posgres_basket_repository_save_call_args: ExpectedPostgresBasketRepositorySaveCallArgs


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
                    picture_url='picture_url1',
                ),
                BasketItemDTO(
                    id=2,
                    product_id=2,
                    product_name='product_name2',
                    unit_price=20,
                    quantity=20,
                    picture_url='picture_url2',
                ),
            ],
        ),
    )

    expected_posgres_basket_repository_save_call_args: ExpectedPostgresBasketRepositorySaveCallArgs = {
        'customer_basket_orm':
            CustomerBasketORM(
                buyer_id=1,
                data=Data(
                    basket_items=[
                        BasketItem(
                            id=1,
                            product_id=1,
                            product_name='product_name1',
                            unit_price=10,
                            quantity=10,
                            picture_url='picture_url1',
                        ),
                        BasketItem(
                            id=2,
                            product_id=2,
                            product_name='product_name2',
                            unit_price=20,
                            quantity=20,
                            picture_url='picture_url2',
                        ),
                    ],
                ),
            ),
    }

    return TestCaseSucess(
        command=command,
        expected_posgres_basket_repository_save_call_args=expected_posgres_basket_repository_save_call_args,
    )


class TestUpdateCustomerBasketCommandHandler__handle(TestClass[UpdateCustomerBasketCommandHandler]):
    @patch.object(command_handlers, 'Session', new=SqlalchemySessionMock)
    @patch.object(PostgresCustomerBasketRepository, 'save')
    def test_case_success(
        self,
        mock__postgres_customer_basket_repository__save: Mock,
        test_case_success: TestCaseSucess,
    ):
        test_case = test_case_success

        UpdateCustomerBasketCommandHandler().handle(command=test_case.command)

        call = mock__postgres_customer_basket_repository__save.call_args_list[0]
        call_kwargs__customer_basket_orm_arg = cast(
            CustomerBasketORM,
            call._get_call_arguments()[1]['customer_basket_orm'],
        )
        expected_customer_basket_orm_arg = (
            test_case.expected_posgres_basket_repository_save_call_args['customer_basket_orm']
        )
        assert call_kwargs__customer_basket_orm_arg.buyer_id == expected_customer_basket_orm_arg.buyer_id
        assert call_kwargs__customer_basket_orm_arg.data == expected_customer_basket_orm_arg.data

        sqlalchemy_session_mock.commit.assert_called_once()
