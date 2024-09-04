from typing import List, final

from basket.domain.models.customer_basket import (
    CustomerBasket,
    CustomerBasketRepository,
)
from basket.domain.models.customer_basket.customer_basket_repository import (
    NotFoundError,
)

from basket_cqrs_contract.customer_basket_dto import BasketItemDTO, CustomerBasketDTO
from basket_cqrs_contract.query import CustomerBasketQuery, CustomerDoesNotHaveBasketError

from framework.cqrs.query.handler import IQueryHandler
from framework.sqlalchemy.session import Session

__all__ = ('CustomerBasketQueryHandler', )


@final
@CustomerBasketQuery.handler
class CustomerBasketQueryHandler(IQueryHandler):
    @staticmethod
    def _orm_to_dto(customer_basket_orm: CustomerBasket) -> CustomerBasketDTO:
        basket_items: List[BasketItemDTO] = []
        for basket_item in customer_basket_orm.data.basket_items:
            basket_items.append(
                BasketItemDTO(
                    id=basket_item.id,
                    product_id=basket_item.product_id,
                    product_name=basket_item.product_name,
                    unit_price=basket_item.unit_price,
                    quantity=basket_item.quantity,
                    picture_url=basket_item.picture_url,
                ),
            )

        return CustomerBasketDTO(
            buyer_id=customer_basket_orm.buyer_id,
            basket_items=basket_items,
        )

    def handle(self, query: CustomerBasketQuery) -> CustomerBasketDTO:
        with Session() as session:
            customer_basket_repository = CustomerBasketRepository(session=session)
            try:
                with session.begin():
                    customer_basket_orm = customer_basket_repository.get_by_buyer_id(buyer_id=query.customer_id)
            except NotFoundError:
                raise CustomerDoesNotHaveBasketError(f'customer_id = {query.customer_id}')

            return self._orm_to_dto(customer_basket_orm)
