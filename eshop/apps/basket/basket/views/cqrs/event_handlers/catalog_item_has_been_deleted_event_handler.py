from typing import List, final

from basket.infrastructure.persistence.postgres.customer_basket import (
    CustomerBasketORM,
    PostgresCustomerBasketRepository,
)

from catalog_cqrs_contract.event import CatalogItemHasBeenDeletedEvent

from framework.cqrs.event import IEventHandler

__all__ = ('CatalogItemHasBeenDeletedEventHandler', )


@final
@CatalogItemHasBeenDeletedEvent.handler
class CatalogItemHasBeenDeletedEventHandler(IEventHandler):
    def handle(self, event: CatalogItemHasBeenDeletedEvent) -> None:
        customer_basket_repository = PostgresCustomerBasketRepository(session=event.context.session)
        customers_baskets = customer_basket_repository.all()

        updated_customers_baskets: List[CustomerBasketORM] = []
        for customer_basket in customers_baskets:
            updated_list_of_basket_items: List[CustomerBasketORM] = []
            for basket_item in customer_basket.data.basket_items:
                if basket_item.product_id != event.catalog_item_id:
                    updated_list_of_basket_items.append(basket_item)
                else:
                    updated_customers_baskets.append(customer_basket)

            customer_basket.data.basket_items = updated_list_of_basket_items

        if updated_customers_baskets:
            for customer_basket in updated_customers_baskets:
                customer_basket_repository.save(customer_basket_orm=customer_basket)
