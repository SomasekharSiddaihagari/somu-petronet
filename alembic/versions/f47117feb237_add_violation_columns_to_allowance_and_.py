"""add violation columns to allowance and expense tables

Revision ID: f47117feb237
Revises: 7b814791d7ad
Create Date: 2025-12-11 15:14:59.576750

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f47117feb237'
down_revision: Union[str, Sequence[str], None] = '7b814791d7ad'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # ----- Meal Allowance -----
    op.add_column(
        "meal_allowance_sheet",
        sa.Column("violation", sa.String(length=255), nullable=True)
    )
    op.add_column(
        "meal_allowance_sheet_history",
        sa.Column("violation", sa.String(length=255), nullable=True)
    )

    # ----- Travel Expense -----
    op.add_column(
        "travel_expense_sheet",
        sa.Column("violation", sa.String(length=255), nullable=True)
    )
    op.add_column(
        "travel_expense_sheet_history",
        sa.Column("violation", sa.String(length=255), nullable=True)
    )

    # ----- Daily Allowance -----
    op.add_column(
        "daily_allowance_sheet",
        sa.Column("violation", sa.String(length=255), nullable=True)
    )
    op.add_column(
        "daily_allowance_sheet_history",
        sa.Column("violation", sa.String(length=255), nullable=True)
    )


def downgrade():
    # ----- Meal Allowance -----
    op.drop_column("meal_allowance_sheet", "violation")
    op.drop_column("meal_allowance_sheet_history", "violation")

    # ----- Travel Expense -----
    op.drop_column("travel_expense_sheet", "violation")
    op.drop_column("travel_expense_sheet_history", "violation")

    # ----- Daily Allowance -----
    op.drop_column("daily_allowance_sheet", "viilation")
    op.drop_column("daily_allowance_sheet_history", "violation")