from typing import Annotated, List, Set, Union

from pydantic import BaseModel, field_validator

from sqlalchemy import INTEGER
from sqlalchemy.orm import Mapped, mapped_column

from typing_extensions import Doc

from basket import hints
from basket.app_config import BasketAppConfig

from framework.sqlalchemy.dialects.postgres.pydantic_type import PydanticType

__all__ = ('CustomerBasketORM', )


class BasketItem(BaseModel):
    id: Annotated[
        Union[hints.BasketItemId, None],
        Doc(
            '''
            None в случае, если объет находится в стадии "Transient"

            не является глобальным идентификатором! значение уникально
            в рамках одной корзины
            ''',
        ),
    ]

    product_id: hints.ProductId
    product_name: hints.ProductName
    unit_price: hints.Price
    quantity: hints.Quantity
    picture_url: hints.PictureUrl


class Data(BaseModel):
    basket_items: List[BasketItem]

    # TODO подумать, возможно эти констрейнты лучше вынести на уровень бд
    @field_validator('basket_items')
    @classmethod
    def basket_item_id_unique(cls, value: List[BasketItem]) -> List[BasketItem]:
        checked_ids: Set[hints.BasketItemId] = set([])
        for basket_item in value:
            if basket_item.id is None:
                continue

            if basket_item.id in checked_ids:
                raise ValueError(f'basket item id must be unique, duplicated id = {basket_item.id}')

            checked_ids.add(basket_item.id)

        return value

    @field_validator('basket_items')
    @classmethod
    def product_id_unique(cls, value: List[BasketItem]) -> List[BasketItem]:
        checked_ids: Set[hints.ProductId] = set([])
        for basket_item in value:
            if basket_item.product_id in checked_ids:
                raise ValueError(
                    f'basket item product_id must be unique, duplicated product_id = {basket_item.product_id}',
                )

            checked_ids.add(basket_item.product_id)

        return value


# TODO: удалить суффикс ORM
class CustomerBasketORM(BasketAppConfig.get_sqlalchemy_base()):

    __tablename__ = 'customer_basket'

    # customer_basket лежит в документо-ориентированном виде
    buyer_id: Mapped[hints.BuyerId] = mapped_column(INTEGER, primary_key=True)
    data: Mapped[Data] = mapped_column(PydanticType(Data))
