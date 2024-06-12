"""create tables: CatalogType, CatalogBrand and CatalogItem

Revision ID: 0dd2b4278e23
Revises: 
Create Date: 2024-06-12 07:35:13.785269

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '0dd2b4278e23'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'catalog_brand',
        sa.Column('id', sa.INTEGER(), nullable=False),
        sa.Column('brand', sa.String(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        schema='catalog'
    )
    op.create_table(
        'catalog_type',
        sa.Column('id', sa.INTEGER(), nullable=False),
        sa.Column('type', sa.String(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        schema='catalog'
    )
    op.create_table(
        'catalog_item',
        sa.Column('id', sa.INTEGER(), nullable=False),
        sa.Column('name', sa.VARCHAR(length=50), nullable=False),
        sa.Column('description', sa.TEXT(), nullable=False),
        sa.Column('price', sa.Float(), nullable=False),
        sa.Column('picture_filename', sa.String(), nullable=False),
        sa.Column('picture_url', sa.String(), nullable=False),
        sa.Column('catalog_type_id', sa.INTEGER(), nullable=False),
        sa.Column('catalog_brand_id', sa.INTEGER(), nullable=False),
        sa.Column('available_stock', sa.Integer(), nullable=False),
        sa.Column('restock_threshold', sa.Integer(), nullable=False),
        sa.Column('maxstock_threshold', sa.Integer(), nullable=False),
        sa.Column('on_reorder', sa.Boolean(), nullable=False),
        sa.ForeignKeyConstraint(
            ['catalog_brand_id'],
            ['catalog.catalog_brand.id'],
        ),
        sa.ForeignKeyConstraint(
            ['catalog_type_id'],
            ['catalog.catalog_type.id'],
        ),
        sa.PrimaryKeyConstraint('id'),
        schema='catalog'
    )


def downgrade() -> None:
    op.drop_table('catalog_item', schema='catalog')
    op.drop_table('catalog_type', schema='catalog')
    op.drop_table('catalog_brand', schema='catalog')
