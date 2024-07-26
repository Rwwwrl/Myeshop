from typing import List, final

from basket.infrastructure.persistence.postgres.customer_basket import (
    CustomerBasketORM,
    PostgresCustomerBasketRepository,
)

from catalog_cqrs_contract.event import CatalogItemPriceChangedEvent

from framework.cqrs.event import IEventHandler
from framework.sqlalchemy.session import Session

__all__ = ('CatalogItemPriceChangedEventHandler', )


@final
@CatalogItemPriceChangedEvent.handler
class CatalogItemPriceChangedEventHandler(IEventHandler):
    def handle(self, event: CatalogItemPriceChangedEvent) -> None:
        with Session() as session:
            customer_basket_repository = PostgresCustomerBasketRepository(session=session)
            with session.begin():
                customers_baskets = customer_basket_repository.all()

        updated_customers_baskets: List[CustomerBasketORM] = []
        for customer_basket in customers_baskets:
            for basket_item in customer_basket.data.basket_items:
                if basket_item.product_id == event.catalog_item_id:
                    basket_item.unit_price = event.new_price
                    updated_customers_baskets.append(customer_basket)

                    # в рамках одной корзины BasketItem`ы уникальны по значению `product_id`
                    break

        if updated_customers_baskets:
            with Session() as session:
                customer_basket_repository = PostgresCustomerBasketRepository(session=session)
                with session.begin():
                    for customer_basket in updated_customers_baskets:
                        customer_basket_repository.save(customer_basket_orm=customer_basket)
