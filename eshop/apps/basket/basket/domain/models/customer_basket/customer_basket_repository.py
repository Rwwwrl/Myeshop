from typing import List

from sqlalchemy import delete, insert, select
from sqlalchemy.orm import Session, selectinload

from basket import hints

from .customer_basket import CustomerBasket
from ..basket_item import BasketItem


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

    def update(self, customer_basket: CustomerBasket) -> None:
        # yapf: disable
        self._session.execute(
            delete(
                BasketItem,
            ).where(
                BasketItem.basket_buyer_id == customer_basket.buyer_id,
            ),
        )
        # yapf: enable

        params: List[dict] = []
        for basket_item in customer_basket.basket_items:
            params.append(
                {
                    'basket_buyer_id': customer_basket.buyer_id,
                    'product_id': basket_item.product_id,
                    'product_name': basket_item.product_name,
                    'unit_price': basket_item.unit_price,
                    'quantity': basket_item.quantity,
                    'picture_url': basket_item.picture_url,
                },
            )
        self._session.execute(
            insert(BasketItem),
            params=params,
        )
