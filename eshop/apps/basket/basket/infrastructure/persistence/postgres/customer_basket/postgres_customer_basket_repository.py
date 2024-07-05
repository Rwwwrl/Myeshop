from sqlalchemy import select, update
from sqlalchemy.orm import Session

from basket import hints

from .customer_basket_orm import CustomerBasketORM

__all__ = ('PostgresCustomerBasketRepository', )


class NotFoundError(Exception):
    pass


class BasketItemIdGenerator:
    def __init__(self, customer_basket_orm: CustomerBasketORM):
        self._current_sequence_value: int = 1
        for basket_item in customer_basket_orm.data.basket_items:
            if basket_item.id is None:
                continue

            if basket_item.id > self._current_sequence_value:
                self._current_sequence_value = basket_item.id

    def next(self) -> hints.BasketItemId:
        self._current_sequence_value += 1
        return self._current_sequence_value


class PostgresCustomerBasketRepository:
    def __init__(self, session: Session):
        self._session = session

    def get_by_buyer_id(self, buyer_id: hints.BuyerId) -> CustomerBasketORM:
        # yapf: disable
        stmt = select(
            CustomerBasketORM,
        ).where(
            CustomerBasketORM.buyer_id == buyer_id,
        )
        # yapf: enable

        customer_basket_orm = self._session.scalar(stmt)
        if not customer_basket_orm:
            raise NotFoundError(f'buyer_id = {buyer_id}')

        return customer_basket_orm

    @staticmethod
    def _set_id_to_basket_items_in_transient_state(customer_basket_orm: CustomerBasketORM) -> None:
        basket_items_in_transient_state = list(filter(lambda bi: bi.id is None, customer_basket_orm.data.basket_items))
        if basket_items_in_transient_state:
            basket_item_id_generator = BasketItemIdGenerator(customer_basket_orm=customer_basket_orm)
            for basket_item in basket_items_in_transient_state:
                basket_item.id = basket_item_id_generator.next()

    def save(self, customer_basket_orm: CustomerBasketORM) -> None:
        self._set_id_to_basket_items_in_transient_state(customer_basket_orm=customer_basket_orm)

        # yapf: disable
        stmt = update(
            CustomerBasketORM,
        ).values(
            data=customer_basket_orm.data,
        ).where(
            CustomerBasketORM.buyer_id == customer_basket_orm.buyer_id,
        )
        # yapf: enable
        self._session.execute(stmt)

        self._session.flush()
