from __future__ import annotations

from typing import List, TYPE_CHECKING

from sqlalchemy import CheckConstraint, DECIMAL, ForeignKey, INTEGER, VARCHAR
from sqlalchemy.orm import Mapped, mapped_column, relationship

from basket import hints
from basket.app_config import BasketAppConfig

if TYPE_CHECKING:
    from .customer_basket import CustomerBasket


class FieldIsInvalid(Exception):
    pass


class BasketItem(BasketAppConfig.get_sqlalchemy_base()):

    __tablename__ = 'basket_item'

    id: Mapped[hints.BasketItemId] = mapped_column(INTEGER, primary_key=True)
    basket_id: Mapped[hints.CustomerBasketId] = mapped_column(ForeignKey('customer_basket.id'))
    product_id: Mapped[hints.ProductId] = mapped_column(INTEGER)
    product_name: Mapped[hints.ProductName] = mapped_column(VARCHAR(50))
    unit_price: Mapped[hints.Price] = mapped_column(DECIMAL)
    quantity: Mapped[hints.Quantity] = mapped_column(INTEGER)
    picture_url: Mapped[hints.PictureUrl] = mapped_column(VARCHAR(255))

    basket: Mapped[CustomerBasket] = relationship(back_populates='basket_items')

    __table_args__ = (
        CheckConstraint(unit_price > 0, name='unit_price_is_positive'),
        CheckConstraint(quantity > 0, name='quantity_is_positive'),
    )

    def validate(self) -> None:
        # TODO ручная валидация уйдет в задаче ESHOP-48, за валидацию будет отвечать pydantic

        exceptions: List[FieldIsInvalid] = []

        if self.unit_price < 0:
            exceptions.append(FieldIsInvalid('field = unit_price'))

        if self.quantity < 0:
            exceptions.append(FieldIsInvalid('field = quantity'))

        if exceptions:
            raise ExceptionGroup('basket item is invalid', exceptions)
