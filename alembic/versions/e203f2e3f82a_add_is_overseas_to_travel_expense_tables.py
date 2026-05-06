"""add is_overseas to travel expense tables

Revision ID: e203f2e3f82a
Revises: f4a1c2360431
Create Date: 2025-12-11 14:30:00.941864

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e203f2e3f82a'
down_revision: Union[str, Sequence[str], None] = 'f4a1c2360431'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column(
        'travel_expense_sheet_detail',
        sa.Column('is_overseas', sa.Boolean(), nullable=True)
    )

    op.add_column(
        'travel_expense_sheet_detail_history',
        sa.Column('is_overseas', sa.Boolean(), nullable=True)
    )


def downgrade():
    op.drop_column('travel_expense_sheet_detail', 'is_overseas')
    op.drop_column('travel_expense_sheet_detail_history', 'is_overseas')
