"""add to_date and change datetime in travel expense

Revision ID: 4d7cc0f0b10c
Revises: d32257f3d268
Create Date: 2026-02-09 16:01:16.511803

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4d7cc0f0b10c'
down_revision: Union[str, Sequence[str], None] = 'd32257f3d268'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():

    # ✅ 1. Add to_date column (DATE only)
    op.add_column(
        "travel_requisition",
        sa.Column("to_date", sa.Date(), nullable=True)
    )

    op.add_column(
        "travel_requisition_history",
        sa.Column("to_date", sa.Date(), nullable=True)
    )

    # ✅ 2. Change from_date Date → DateTime
    op.alter_column(
        "travel_expense_sheet_detail",
        "from_date",
        existing_type=sa.Date(),
        type_=sa.DateTime(),
        existing_nullable=True
    )

    # ✅ 3. Change to_date Date → DateTime
    op.alter_column(
        "travel_expense_sheet_detail",
        "to_date",
        existing_type=sa.Date(),
        type_=sa.DateTime(),
        existing_nullable=True
    )


def downgrade():

    # 🔻 revert datetime back to date
    op.alter_column(
        "travel_expense_sheet_detail",
        "from_date",
        existing_type=sa.DateTime(),
        type_=sa.Date(),
        existing_nullable=True
    )

    op.alter_column(
        "travel_expense_sheet_detail",
        "to_date",
        existing_type=sa.DateTime(),
        type_=sa.Date(),
        existing_nullable=True
    )

    # 🔻 remove added column
    op.drop_column("travel_requisition", "to_date")
    op.drop_column("travel_requisition_history", "to_date")