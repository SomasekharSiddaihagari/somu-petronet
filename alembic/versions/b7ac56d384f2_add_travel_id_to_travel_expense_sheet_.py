"""add travel_id to travel_expense_sheet and history

Revision ID: b7ac56d384f2
Revises: 1d7a012baf76
Create Date: 2026-01-13 17:05:10.516367

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b7ac56d384f2'
down_revision: Union[str, Sequence[str], None] = '1d7a012baf76'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column(
        "travel_expense_sheet",
        sa.Column("travel_id", sa.BigInteger(), nullable=True)
    )

    op.add_column(
        "travel_expense_sheet_history",
        sa.Column("travel_id", sa.BigInteger(), nullable=True)
    )

def downgrade():
    op.drop_column("travel_expense_sheet_history", "travel_id")
    op.drop_column("travel_expense_sheet", "travel_id")