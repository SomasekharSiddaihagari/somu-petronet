"""add interest housing 24b

Revision ID: e1d6d38f32cd
Revises: 9cd2ed1e4703
Create Date: 2026-02-06 16:48:17.954325

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e1d6d38f32cd'
down_revision: Union[str, Sequence[str], None] = '9cd2ed1e4703'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():

    # user_finance
    op.add_column(
        'user_finance',
        sa.Column('interest_housing_24b', sa.Float(), nullable=True)
    )

    # user_finance_history
    op.add_column(
        'user_finance_history',
        sa.Column('interest_housing_24b', sa.Float(), nullable=True)
    )


def downgrade():

    op.drop_column('user_finance', 'interest_housing_24b')
    op.drop_column('user_finance_history', 'interest_housing_24b')