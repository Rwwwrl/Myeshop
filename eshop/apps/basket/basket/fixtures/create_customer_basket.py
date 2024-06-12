from sqlalchemy.orm import Session

from basket.domain.models.basket_item import BasketItem
from basket.domain.models.customer_basket import CustomerBasket

from eshop import settings


def create_customer_basket():
    with Session(settings.SQLALCHEMY_ENGINE) as session:
        customer_basket1 = CustomerBasket(buyer_id=1)
        basket_items1 = [
            BasketItem(
                id=1,
                basket=customer_basket1,
                product_id=1,
                product_name='name1',
                unit_price=10,
                quantity=1,
                picture_url='root/filename1',
            ),
            BasketItem(
                id=2,
                basket=customer_basket1,
                product_id=2,
                product_name='name2',
                unit_price=20,
                quantity=2,
                picture_url='root/filename2',
            ),
        ]

        session.add_all([
            customer_basket1,
            *basket_items1,
        ])

        session.commit()


if __name__ == '__main__':
    create_customer_basket()
