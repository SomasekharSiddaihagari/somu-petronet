"""update travel expense tables

Revision ID: 7b814791d7ad
Revises: e203f2e3f82a
Create Date: 2025-12-11 15:07:43.746629

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7b814791d7ad'
down_revision: Union[str, Sequence[str], None] = 'e203f2e3f82a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # ----- travel_expense_sheet_detail -----
    with op.batch_alter_table("travel_expense_sheet_detail") as batch_op:
        batch_op.alter_column("date", new_column_name="from_date")
        batch_op.add_column(sa.Column("to_date", sa.Date(), nullable=True))

    # ----- travel_expense_sheet_detail_history -----
    with op.batch_alter_table("travel_expense_sheet_detail_history") as batch_op:
        batch_op.alter_column("date", new_column_name="from_date")
        batch_op.add_column(sa.Column("to_date", sa.Date(), nullable=True))

    # ----- travel_expense_sheet -----
    op.add_column(
        "travel_expense_sheet",
        sa.Column("travel_mode", sa.String(length=100), nullable=True)
    )

    # ----- travel_expense_sheet_history -----
    op.add_column(
        "travel_expense_sheet_history",
        sa.Column("travel_mode", sa.String(length=100), nullable=True)
    )


def downgrade():
    # ----- travel_expense_sheet_detail -----
    with op.batch_alter_table("travel_expense_sheet_detail") as batch_op:
        batch_op.drop_column("to_date")
        batch_op.alter_column("from_date", new_name="date")

    # ----- travel_expense_sheet_detail_history -----
    with op.batch_alter_table("travel_expense_sheet_detail_history") as batch_op:
        batch_op.drop_column("to_date")
        batch_op.alter_column("from_date", new_name="date")

    # ----- travel_expense_sheet -----
    op.drop_column("travel_expense_sheet", "travel_mode")

    # ----- travel_expense_sheet_history -----
    op.drop_column("travel_expense_sheet_history", "travel_mode")
