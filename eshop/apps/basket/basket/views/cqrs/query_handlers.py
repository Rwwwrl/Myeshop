from typing import List

from basket.domain.models.customer_basket import (
    CustomerBasket as CustomerBasketORM,
    CustomerBasketRepository,
)

from basket_cqrs_contract.query import CustomerBasketQuery
from basket_cqrs_contract.query.query_response import BasketItemDTO, CustomerBasketDTO

from framework.cqrs.query.handler import IQueryHandler
from framework.sqlalchemy.session_factory import session_factory

__all__ = ('CustomerBasketQueryHandler', )


@CustomerBasketQuery.handler
class CustomerBasketQueryHandler(IQueryHandler):
    @staticmethod
    def _to_dto(customer_basket_orm: CustomerBasketORM) -> CustomerBasketDTO:
        basket_items: List[BasketItemDTO] = []
        for basket_item_orm in customer_basket_orm.basket_items:
            basket_items.append(
                BasketItemDTO(
                    id=basket_item_orm.id,
                    product_id=basket_item_orm.product_id,
                    product_name=basket_item_orm.product_name,
                    unit_price=basket_item_orm.unit_price,
                    quantity=basket_item_orm.quantity,
                    picture_url=basket_item_orm.picture_url,
                ),
            )

        return CustomerBasketDTO(
            buyer_id=customer_basket_orm.buyer_id,
            basket_items=basket_items,
        )

    def handle(self, query: CustomerBasketQuery) -> CustomerBasketDTO:
        with session_factory() as session:
            customer_basket_repository = CustomerBasketRepository(session=session)
            customer_basket_orm = customer_basket_repository.get_by_buyer_id(id=query.customer_id)
            return self._to_dto(customer_basket_orm)
