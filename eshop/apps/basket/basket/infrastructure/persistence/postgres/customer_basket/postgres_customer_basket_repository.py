from sqlalchemy import select
from sqlalchemy.orm import Session

from basket import hints

from .customer_basket_orm import CustomerBasketORM

__all__ = ('PostgresCustomerBasketRepository', )


class NotFoundError(Exception):
    pass


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

    def save(self, customer_basket_orm: CustomerBasketORM) -> None:
        pass
