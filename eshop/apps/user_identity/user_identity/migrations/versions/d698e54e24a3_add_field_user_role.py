"""add field user.role

Revision ID: d698e54e24a3
Revises: 7401a67498ee
Create Date: 2024-07-26 11:58:29.088843

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

from user_identity.domain.models.user.user import UserRoleEnum

# revision identifiers, used by Alembic.
revision: str = 'd698e54e24a3'
down_revision: Union[str, None] = '7401a67498ee'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

userroleenum = sa.Enum(UserRoleEnum.ADMIN.value, UserRoleEnum.CUSTOMER.value, name='userroleenum')


def upgrade() -> None:
    userroleenum.create(op.get_bind(), checkfirst=True)

    op.add_column(
        'user',
        sa.Column(
            'role',
            userroleenum,
            nullable=False,
            server_default=UserRoleEnum.CUSTOMER.value,
        ),
        schema='user_identity',
    )

    # в рамках добавление поля мы задали дефолтное значение,
    # оно нужно только чтобы провернуть миграцию. Глобально нам не нужно дефолтное значение.
    op.alter_column(
        table_name='user',
        column_name='role',
        schema='user_identity',
        server_default=None,
    )


def downgrade() -> None:
    op.drop_column(
        'user',
        'role',
        schema='user_identity',
    )

    userroleenum.drop(op.get_bind(), checkfirst=True)
