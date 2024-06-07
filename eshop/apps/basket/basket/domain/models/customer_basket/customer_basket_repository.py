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

    def get_by_buyer_id(self, buyer_id: hints.CustomerId) -> CustomerBasket:
        # yapf: disable
        stmt = select(
            CustomerBasket,
        ).select_from(
            CustomerBasket,
        ).join(
            BasketItem,
        ).where(
            CustomerBasket.buyer_id == buyer_id,
        ).options(
            selectinload(
                CustomerBasket.basket_items,
            ),
        )
        # yapf: enable
        customer_basket = self._session.scalar(stmt)

        if customer_basket is None:
            raise NotFoundError(f'buyer_id = {buyer_id}')

        return customer_basket
