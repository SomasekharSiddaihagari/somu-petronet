"""add head tech fields to allowance and travel tables

Revision ID: d0a0dbe55245
Revises: 36878207300d
Create Date: 2026-02-26 15:53:45.906875

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd0a0dbe55245'
down_revision: Union[str, Sequence[str], None] = '36878207300d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():

    tables = [
        "daily_allowance_sheet",
        "daily_allowance_sheet_history",
        "meal_allowance_sheet",
        "meal_allowance_sheet_history",
        "travel_expense_sheet",
        "travel_expense_sheet_history",
    ]

    for table in tables:
        op.add_column(table, sa.Column("updated_by_head_tech", sa.Date(), nullable=True))
        op.add_column(table, sa.Column("updated_by_head_tech_name", sa.String(length=150), nullable=True))
        op.add_column(table, sa.Column("head_tech_comments", sa.Text(), nullable=True))


def downgrade():

    tables = [
        "daily_allowance_sheet",
        "daily_allowance_sheet_history",
        "meal_allowance_sheet",
        "meal_allowance_sheet_history",
        "travel_expense_sheet",
        "travel_expense_sheet_history",
    ]

    for table in tables:
        op.drop_column(table, "head_tech_comments")
        op.drop_column(table, "updated_by_head_tech_name")
        op.drop_column(table, "updated_by_head_tech")