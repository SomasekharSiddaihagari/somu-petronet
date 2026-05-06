"""add is_dollar to travel expense

Revision ID: a6f81c4827de
Revises: 5f37516b02a2
Create Date: 2026-01-19 11:27:02.161826

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a6f81c4827de'
down_revision: Union[str, Sequence[str], None] = '5f37516b02a2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column(
        "travel_expense_sheet",
        sa.Column("is_dollar", sa.Boolean(), nullable=True)
    )

    op.add_column(
        "travel_expense_sheet_history",
        sa.Column("is_dollar", sa.Boolean(), nullable=True)
    )


def downgrade():
    op.drop_column("travel_expense_sheet", "is_dollar")
    op.drop_column("travel_expense_sheet_history", "is_dollar")