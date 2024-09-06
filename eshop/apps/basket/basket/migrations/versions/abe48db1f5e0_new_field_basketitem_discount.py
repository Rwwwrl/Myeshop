"""new field: BasketItem.discount

Revision ID: abe48db1f5e0
Revises: 9630ba02fd4f
Create Date: 2024-09-06 14:12:19.735622

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

from psycopg2.extras import Json

# revision identifiers, used by Alembic.
revision: str = 'abe48db1f5e0'
down_revision: Union[str, None] = '9630ba02fd4f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

DISCOUNT_VALUE_FOR_OLD_ENTRYS: int = 0

__doc__ = (
    """
    Нам не нужно через DDL "добавлять" поле discount, т.к CustomerBasket лежит в документоориентированном виде,
    т.е. BasketItem является ключом в словаре CustomerBasket.data .
    Нo нужно сохранить обратную совместимость - то есть добавить дефолтное значение discount для всех
    старых записей BasketItem.
    """
)


def upgrade() -> None:
    connection = op.get_bind()
    customer_baskets = connection.execute(sa.text("SELECT buyer_id, data FROM basket.customer_basket")).all()

    for customer_basket in customer_baskets:
        customer_basket = customer_basket._asdict()
        buyer_id = customer_basket['buyer_id']
        data = customer_basket['data']

        for basket_item in data['basket_items']:
            basket_item['discount'] = DISCOUNT_VALUE_FOR_OLD_ENTRYS

        connection.execute(
            statement=sa.text(
                """
                UPDATE basket.customer_basket
                SET data = :data
                WHERE buyer_id = :buyer_id
                """,
            ),
            parameters={
                "data": Json(data),
                "buyer_id": buyer_id,
            },
        )


def downgrade() -> None:
    connection = op.get_bind()
    customer_baskets = connection.execute(sa.text("SELECT buyer_id, data FROM basket.customer_basket")).all()

    for customer_basket in customer_baskets:
        customer_basket = customer_basket._asdict()
        buyer_id = customer_basket['buyer_id']
        data = customer_basket['data']

        for basket_item in data['basket_items']:
            del basket_item['discount']

        connection.execute(
            statement=sa.text(
                """
                UPDATE basket.customer_basket
                SET data = :data
                WHERE buyer_id = :buyer_id
                """,
            ),
            parameters={
                "data": Json(data),
                "buyer_id": buyer_id,
            },
        )
