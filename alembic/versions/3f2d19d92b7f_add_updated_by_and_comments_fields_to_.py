"""Add updated_by and comments fields to meal & daily allowance sheets

Revision ID: 3f2d19d92b7f
Revises: 82afe78a334b
Create Date: 2025-12-11 16:00:13.799567

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3f2d19d92b7f'
down_revision: Union[str, Sequence[str], None] = '82afe78a334b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def add_columns(table):
    op.add_column(table, sa.Column("updated_by_supervisor", sa.Date(), nullable=True))
    op.add_column(table, sa.Column("updated_by_supervisor_name", sa.String(150), nullable=True))

    op.add_column(table, sa.Column("updated_by_hr", sa.Date(), nullable=True))
    op.add_column(table, sa.Column("updated_by_hr_name", sa.String(150), nullable=True))

    op.add_column(table, sa.Column("updated_by_md", sa.Date(), nullable=True))
    op.add_column(table, sa.Column("updated_by_md_name", sa.String(150), nullable=True))

    op.add_column(table, sa.Column("updated_by_finance", sa.Date(), nullable=True))
    op.add_column(table, sa.Column("updated_by_finance_name", sa.String(150), nullable=True))

    op.add_column(table, sa.Column("supervisor_comments", sa.Text(), nullable=True))
    op.add_column(table, sa.Column("hr_comments", sa.Text(), nullable=True))
    op.add_column(table, sa.Column("finance_comments", sa.Text(), nullable=True))


def upgrade():
    # Meal Allowance
    add_columns("meal_allowance_sheet")
    add_columns("meal_allowance_sheet_history")

    # Daily Allowance
    add_columns("daily_allowance_sheet")
    add_columns("daily_allowance_sheet_history")


def downgrade():
    cols = [
        "updated_by_supervisor",
        "updated_by_supervisor_name",
        "updated_by_hr",
        "updated_by_hr_name",
        "updated_by_md",
        "updated_by_md_name",
        "updated_by_finance",
        "updated_by_finance_name",
        "supervisor_comments",
        "hr_comments",
        "finance_comments",
    ]

    for table in [
        "meal_allowance_sheet",
        "meal_allowance_sheet_history",
        "daily_allowance_sheet",
        "daily_allowance_sheet_history",
    ]:
        for col in cols:
            op.drop_column(table, col)
