from datetime import datetime
from typing import List

from basket_cqrs_contract.customer_basket_dto import BasketItemDTO, CustomerBasketDTO
from basket_cqrs_contract.event import UserCheckoutAcceptedEvent

from framework.for_pytests.for_testing_cqrs_contract_usage import (
    ITestEventContractConsumer,
    assert_attribute,
)


class TestUserCheckoutAcceptedEvent(ITestEventContractConsumer[UserCheckoutAcceptedEvent]):
    def test_event_contract(self) -> None:
        assert_attribute(UserCheckoutAcceptedEvent, 'basket', CustomerBasketDTO)

        assert_attribute(CustomerBasketDTO, 'basket_items', List[BasketItemDTO])

        assert_attribute(BasketItemDTO, 'product_id', int)
        assert_attribute(BasketItemDTO, 'product_name', str)
        assert_attribute(BasketItemDTO, 'unit_price', float)
        assert_attribute(BasketItemDTO, 'quantity', int)
        assert_attribute(BasketItemDTO, 'picture_url', str)

        assert_attribute(UserCheckoutAcceptedEvent, 'user_id', int)
        assert_attribute(UserCheckoutAcceptedEvent, 'username', str)
        assert_attribute(UserCheckoutAcceptedEvent, 'city', str)
        assert_attribute(UserCheckoutAcceptedEvent, 'street', str)
        assert_attribute(UserCheckoutAcceptedEvent, 'state', str)
        assert_attribute(UserCheckoutAcceptedEvent, 'country', str)
        assert_attribute(UserCheckoutAcceptedEvent, 'zip_code', str)
        assert_attribute(UserCheckoutAcceptedEvent, 'card_number', str)
        assert_attribute(UserCheckoutAcceptedEvent, 'card_holder_name', str)
        assert_attribute(UserCheckoutAcceptedEvent, 'card_expiration', datetime)
        assert_attribute(UserCheckoutAcceptedEvent, 'card_security_number', str)
        assert_attribute(UserCheckoutAcceptedEvent, 'card_type_id', int)
