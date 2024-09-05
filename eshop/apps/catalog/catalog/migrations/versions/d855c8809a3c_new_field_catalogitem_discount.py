"""new field: CatalogItem.discount

Revision ID: d855c8809a3c
Revises: 0dd2b4278e23
Create Date: 2024-09-05 10:51:25.404433

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = 'd855c8809a3c'
down_revision: Union[str, None] = '0dd2b4278e23'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

DEFAULT_DISCOUNT_VALUE: int = 0


def upgrade() -> None:
    op.add_column(
        'catalog_item',
        sa.Column('discount', sa.INTEGER(), nullable=True),
        schema='catalog',
    )

    op.get_bind().execute(
        statement=sa.text(
            """
            UPDATE catalog.catalog_item
            SET discount = :discount;
            """,
        ),
        parameters={'discount': DEFAULT_DISCOUNT_VALUE},
    )
    op.alter_column(
        table_name='catalog_item',
        column_name='discount',
        nullable=False,
        schema='catalog',
    )


def downgrade() -> None:
    op.drop_column('catalog_item', 'discount', schema='catalog')
