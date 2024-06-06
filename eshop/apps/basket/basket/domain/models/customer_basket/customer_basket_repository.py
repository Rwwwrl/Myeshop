from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from basket import hints

from .customer_basket import CustomerBasket
from ..basketitem import BasketItem


class NotFoundError(Exception):
    pass


class CustomerBasketRepository:
    def __init__(self, session: Session):
        self._session = session

    def get_by_id(self, id: hints.CustomerBasketId) -> CustomerBasket:
        # yapf: disable
        stmt = select(
            CustomerBasket,
        ).select_from(
            CustomerBasket,
        ).join(
            BasketItem,
        ).where(
            CustomerBasket.id == id,
        ).options(
            selectinload(
                CustomerBasket.basket_items,
            ),
        )
        # yapf: enable
        customer_basket = self._session.scalar(stmt)

        if customer_basket is None:
            raise NotFoundError(f'id = {id}')

        return customer_basket
