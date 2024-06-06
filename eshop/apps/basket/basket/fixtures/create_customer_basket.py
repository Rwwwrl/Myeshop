from sqlalchemy.orm import Session

from basket.domain.models.basketitem import BasketItem
from basket.domain.models.customer_basket import CustomerBasket

from eshop import settings


def create_customer_basket():
    with Session(settings.SQLALCHEMY_ENGINE) as session:
        customer_basket1 = CustomerBasket(buyer_id=1)
        basket_items1 = [
            BasketItem(
                basket=customer_basket1,
                product_id=1,
                product_name='product_name1',
                unit_price=10,
                quantity=1,
                picture_url='picture_url1',
            ),
            BasketItem(
                basket=customer_basket1,
                product_id=2,
                product_name='product_name2',
                unit_price=10,
                quantity=2,
                picture_url='picture_url2',
            ),
        ]

        customer_basket2 = CustomerBasket(buyer_id=2)
        basket_items2 = [
            BasketItem(
                basket=customer_basket2,
                product_id=1,
                product_name='product_name1',
                unit_price=10,
                quantity=1,
                picture_url='picture_url1',
            ),
            BasketItem(
                basket=customer_basket2,
                product_id=2,
                product_name='product_name2',
                unit_price=10,
                quantity=2,
                picture_url='picture_url2',
            ),
        ]

        session.add_all([
            customer_basket1,
            customer_basket2,
            *basket_items1,
            *basket_items2,
        ])

        session.commit()


if __name__ == '__main__':
    create_customer_basket()
