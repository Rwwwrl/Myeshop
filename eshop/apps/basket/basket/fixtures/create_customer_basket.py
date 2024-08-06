from basket.infrastructure.persistence.postgres.customer_basket.customer_basket_orm import (
    BasketItem,
    CustomerBasketORM,
    Data,
)

from framework.sqlalchemy.session import Session


def create_customer_basket():
    customer_basket1 = CustomerBasketORM(
        buyer_id=1,
        data=Data(
            basket_items=[
                BasketItem(
                    id=1,
                    product_id=1,
                    product_name='name1',
                    unit_price=10,
                    quantity=1,
                    picture_url='media/catalog_item1.jpg',
                ),
                BasketItem(
                    id=2,
                    product_id=2,
                    product_name='name2',
                    unit_price=20,
                    quantity=2,
                    picture_url='media/catalog_item2.jpg',
                ),
            ],
        ),
    )

    with Session() as session:
        with session.begin():
            session.add(customer_basket1)


if __name__ == '__main__':
    create_customer_basket()
