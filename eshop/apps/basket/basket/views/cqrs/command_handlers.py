from basket.domain.models.basket_item import BasketItem
from basket.domain.models.customer_basket import CustomerBasket, CustomerBasketRepository

from basket_cqrs_contract.command import UpdateCustomerBasketCommand

from framework.cqrs.command import ICommandHandler
from framework.sqlalchemy.session_factory import session_factory


@UpdateCustomerBasketCommand.handler
class UpdateCustomerBasketCommandHandler(ICommandHandler):
    @staticmethod
    def _deserialize_to_orm(command: UpdateCustomerBasketCommand) -> CustomerBasket:
        return CustomerBasket(
            buyer_id=command.buyer_id,
            basket_items=[
                BasketItem(
                    product_id=basket_item.product_id,
                    product_name=basket_item.product_name,
                    unit_price=basket_item.unit_price,
                    quantity=basket_item.quantity,
                    picture_url=basket_item.picture_url,
                ) for basket_item in command.basket_items
            ],
        )

    def handle(self, command: UpdateCustomerBasketCommand) -> None:
        customer_basket = self._deserialize_to_orm(command)
        with session_factory() as session:
            customer_basket_repository = CustomerBasketRepository(session=session)
            customer_basket_repository.update(customer_basket=customer_basket)
            session.commit()
