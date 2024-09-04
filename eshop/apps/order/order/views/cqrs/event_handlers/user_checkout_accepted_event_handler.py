from typing import final

from basket_cqrs_contract.customer_basket_dto import BasketItemDTO
from basket_cqrs_contract.event import UserCheckoutAcceptedEvent

from framework.cqrs.event import IEventHandler

from order_cqrs_contract.command.create_order_command import CreateOrderCommand, OrderItemDTO

__all__ = ('UserCheckoutAcceptedEventHandler', )


@final
@UserCheckoutAcceptedEvent.handler
class UserCheckoutAcceptedEventHandler(IEventHandler):
    @staticmethod
    def _basket_item_dto_to_order_item_dto(basket_item_dto: BasketItemDTO) -> OrderItemDTO:
        return OrderItemDTO(
            product_id=basket_item_dto.product_id,
            product_name=basket_item_dto.product_name,
            unit_price=basket_item_dto.unit_price,
            units=basket_item_dto.quantity,
            picture_url=basket_item_dto.picture_url,
        )

    def handle(self, event: UserCheckoutAcceptedEvent) -> None:
        create_order_command = CreateOrderCommand(
            order_items=[
                self._basket_item_dto_to_order_item_dto(basket_item) for basket_item in event.basket.basket_items
            ],
            buyer_id=event.user_id,
            buyer_name=event.username,
            city=event.city,
            street=event.street,
            state=event.state,
            country=event.country,
            zip_code=event.zip_code,
            card_number=event.card_number,
            card_holder_name=event.card_holder_name,
            card_expiration=event.card_expiration,
            card_security_number=event.card_security_number,
            card_type_id=event.card_type_id,
        )

        # TODO: надо подпумать, вероятно можно заменить на sync_execute
        create_order_command.execute()
