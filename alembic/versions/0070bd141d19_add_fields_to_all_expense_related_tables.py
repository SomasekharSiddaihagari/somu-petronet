"""Add fields to all expense-related tables

Revision ID: 0070bd141d19
Revises: 71e084d3bbd1
Create Date: 2025-12-09 16:35:47.618060

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0070bd141d19'
down_revision: Union[str, Sequence[str], None] = '71e084d3bbd1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # -----------------------------------------------------------
    # 1. EXPENSE DETAILS (travel_expense_sheet_detail)
    # -----------------------------------------------------------
    op.add_column(
        "travel_expense_sheet_detail",
        sa.Column("from_location", sa.String(255), nullable=True)
    )
    op.add_column(
        "travel_expense_sheet_detail",
        sa.Column("to_location", sa.String(255), nullable=True)
    )

    # -----------------------------------------------------------
    # 2. DAILY ALLOWANCE (daily_allowance_sheet_detail)
    # -----------------------------------------------------------
    op.add_column(
        "daily_allowance_sheet_detail",
        sa.Column("from_location", sa.String(255), nullable=True)
    )
    op.add_column(
        "daily_allowance_sheet_detail",
        sa.Column("to_location", sa.String(255), nullable=True)
    )
    op.add_column(
        "daily_allowance_sheet_detail",
        sa.Column("from_date_time", sa.DateTime(), nullable=True)
    )
    op.add_column(
        "daily_allowance_sheet_detail",
        sa.Column("to_date_time", sa.DateTime(), nullable=True)
    )

    # -----------------------------------------------------------
    # 3. TRAVEL EXPENSE SHEET (travel_expense_sheet)
    # DATE fields instead of BigInteger
    # -----------------------------------------------------------
    op.add_column(
        "travel_expense_sheet",
        sa.Column("updated_by_supervisor", sa.Date(), nullable=True)
    )
    op.add_column(
        "travel_expense_sheet",
        sa.Column("updated_by_hr", sa.Date(), nullable=True)
    )
    op.add_column(
        "travel_expense_sheet",
        sa.Column("updated_by_md", sa.Date(), nullable=True)
    )
    op.add_column(
        "travel_expense_sheet",
        sa.Column("updated_by_finance", sa.Date(), nullable=True)
    )

    op.add_column(
        "travel_expense_sheet",
        sa.Column("supervisor_comments", sa.Text(), nullable=True)
    )
    op.add_column(
        "travel_expense_sheet",
        sa.Column("hr_comments", sa.Text(), nullable=True)
    )
    op.add_column(
        "travel_expense_sheet",
        sa.Column("finance_comments", sa.Text(), nullable=True)
    )


def downgrade():
    # EXPENSE DETAILS
    op.drop_column("travel_expense_sheet_detail", "from_location")
    op.drop_column("travel_expense_sheet_detail", "to_location")

    # DAILY ALLOWANCE
    op.drop_column("daily_allowance_sheet_detail", "from_location")
    op.drop_column("daily_allowance_sheet_detail", "to_location")
    op.drop_column("daily_allowance_sheet_detail", "from_date_time")
    op.drop_column("daily_allowance_sheet_detail", "to_date_time")

    # TRAVEL EXPENSE SHEET
    op.drop_column("travel_expense_sheet", "updated_by_supervisor")
    op.drop_column("travel_expense_sheet", "updated_by_hr")
    op.drop_column("travel_expense_sheet", "updated_by_md")
    op.drop_column("travel_expense_sheet", "updated_by_finance")
    op.drop_column("travel_expense_sheet", "supervisor_comments")
    op.drop_column("travel_expense_sheet", "hr_comments")
    op.drop_column("travel_expense_sheet", "finance_comments")