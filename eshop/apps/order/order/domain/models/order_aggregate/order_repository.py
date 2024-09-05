from typing import final

from pydantic import BaseModel
from pydantic.types import PositiveInt

from sqlalchemy import insert
from sqlalchemy.orm import Mapped, mapped_column

from framework.sqlalchemy.dialects.postgres.pydantic_type import PydanticType

from order.app_config import OrderAppConfig

from .address import Address
from .order import Order

__all__ = ('OrderRepository', )


class Data(BaseModel):
    address: str
    buyer_id: PositiveInt
    buyer_username: str


class OrderORM(OrderAppConfig.get_sqlalchemy_base()):

    __tablename__ = 'order'

    id: Mapped[int] = mapped_column(primary_key=True)
    # order лежит в документо-ориентированном виде
    data: Mapped[Data] = mapped_column(PydanticType(Data))


@final
class OrderRepository:
    def create(self, address: Address, buyer_id: PositiveInt, buyer_username: str) -> Order:
        # yapf: disable
        id_of_created_entry = insert(
            OrderORM,
        ).values(
            data=Data(
                address=address,
                buyer_id=buyer_id,
                buyer_username=buyer_username,
            ),
        ).returning(
            OrderORM.id,
        )
        # yapf: enable
        return Order(
            id=id_of_created_entry,
            address=address,
            buyer_id=buyer_id,
            buyer_username=buyer_username,
        )
