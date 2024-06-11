"""dropped CustomerBasket.id, set CustomerBasket.buyer_id to the primary key

Revision ID: 3d262d4f0e7a
Revises: e129d01673b8
Create Date: 2024-06-07 12:14:51.181639

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '3d262d4f0e7a'
down_revision: Union[str, None] = 'e129d01673b8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_constraint('basket_item_basket_id_fkey', 'basket_item', schema='basket', type_='foreignkey')
    op.drop_column('customer_basket', 'id', schema='basket')

    op.create_primary_key(
        constraint_name='pk_customer_basket',
        table_name='customer_basket',
        columns=[
            'buyer_id',
        ],
        schema='basket',
    )

    op.alter_column(
        table_name='basket_item',
        column_name='basket_id',
        new_column_name='basket_buyer_id',
        schema='basket',
    )

    op.create_foreign_key(
        None,
        'basket_item',
        'customer_basket',
        ['basket_buyer_id'],
        ['buyer_id'],
        source_schema='basket',
        referent_schema='basket',
    )


def downgrade() -> None:
    # 1
    op.drop_constraint(
        constraint_name='basket_item_basket_buyer_id_fkey',
        table_name='basket_item',
        schema='basket',
        type_='foreignkey',
    )

    # 2
    op.drop_constraint(
        constraint_name='pk_customer_basket',
        table_name='customer_basket',
        type_='primary',
        schema='basket',
    )

    # 3
    op.add_column(
        'customer_basket',
        sa.Column(
            'id',
            sa.INTEGER(),
        ),
        schema='basket',
    )
    # yapf: disable
    op.execute(
        """
        UPDATE basket.customer_basket
        SET id = buyer_id;
        """
    )
    # yapf: enable
    op.alter_column(table_name='customer_basket', column_name='id', nullable=False, schema='basket')
    op.create_primary_key(
        None,
        'customer_basket',
        columns=[
            'id',
        ],
        schema='basket',
    )

    # 4
    op.alter_column(
        table_name='basket_item',
        column_name='basket_buyer_id',
        new_column_name='basket_id',
        schema='basket',
    )

    # 5
    op.create_foreign_key(
        None,
        'basket_item',
        'customer_basket',
        ['basket_id'],
        ['id'],
        source_schema='basket',
        referent_schema='basket',
    )
