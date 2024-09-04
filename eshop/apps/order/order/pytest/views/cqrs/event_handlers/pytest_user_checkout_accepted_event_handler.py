from datetime import datetime

from mock import Mock, patch

import pytest

from basket_cqrs_contract.customer_basket_dto import BasketItemDTO, CustomerBasketDTO
from basket_cqrs_contract.event import UserCheckoutAcceptedEvent

from framework.for_pytests.test_case import TestCase
from framework.for_pytests.test_class import TestClass

from order.views.cqrs.event_handlers import UserCheckoutAcceptedEventHandler

from order_cqrs_contract.command.create_order_command import CreateOrderCommand, OrderItemDTO


class TestCaseSuccess(TestCase[TestClass]):
    event: UserCheckoutAcceptedEvent
    expected_command_execute: CreateOrderCommand


@pytest.fixture(scope='session')
def test_case_success() -> TestCaseSuccess:
    event = UserCheckoutAcceptedEvent(
        user_id=1,
        username='username',
        order_number=10,
        city='city',
        street='street',
        state='state',
        country='country',
        zip_code='zip_code',
        card_number='card_number',
        card_holder_name='card_holder_name',
        card_expiration=datetime(year=1970, month=1, day=1, minute=0),
        card_security_number='card_security_number',
        card_type_id=10,
        basket=CustomerBasketDTO(
            buyer_id=1,
            basket_items=[
                BasketItemDTO(
                    id=1,
                    product_id=10,
                    product_name='product_name10',
                    picture_url='picture_url10',
                    quantity=2,
                    unit_price=5,
                ),
                BasketItemDTO(
                    id=2,
                    product_id=11,
                    product_name='product_name11',
                    picture_url='picture_url11',
                    quantity=3,
                    unit_price=6,
                ),
            ],
        ),
    )

    expected_command_execute = CreateOrderCommand(
        order_items=[
            OrderItemDTO(
                product_id=10,
                product_name='product_name10',
                unit_price=5,
                units=2,
                picture_url='picture_url10',
            ),
            OrderItemDTO(
                product_id=11,
                product_name='product_name11',
                unit_price=6,
                units=3,
                picture_url='picture_url11',
            ),
        ],
        user_id=1,
        username='username',
        city='city',
        street='street',
        state='state',
        country='country',
        zip_code='zip_code',
        card_number='card_number',
        card_holder_name='card_holder_name',
        card_expiration=datetime(year=1970, month=1, day=1, minute=0),
        card_security_number='card_security_number',
        card_type_id=10,
    )

    return TestCaseSuccess(
        event=event,
        expected_command_execute=expected_command_execute,
    )


class TestUserCheckoutAcceptedEventHandler__handle(TestClass[UserCheckoutAcceptedEventHandler.handle]):
    @patch.object(CreateOrderCommand, CreateOrderCommand.execute.__name__, autospec=True)
    def test_case_success(
        self,
        mock__create_order_command__execute: Mock,
        test_case_success: TestCaseSuccess,
    ):
        test_case = test_case_success

        UserCheckoutAcceptedEventHandler().handle(event=test_case.event)

        fact_command_execute: CreateOrderCommand = mock__create_order_command__execute.call_args_list[0].args[0]
        assert fact_command_execute == test_case.expected_command_execute
