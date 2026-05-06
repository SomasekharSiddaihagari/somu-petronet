"""change travel expense proofs to text

Revision ID: 9c73f329682a
Revises: 50948a079bc3
Create Date: 2026-01-09 16:28:27.269130

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9c73f329682a'
down_revision: Union[str, Sequence[str], None] = '50948a079bc3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade():
    # ---- travel_expense_sheet_detail ----
    op.alter_column(
        "travel_expense_sheet_detail",
        "air_rail_bus_proof",
        type_=sa.Text(),
        existing_type=sa.String(length=255),
        nullable=True
    )
    op.alter_column(
        "travel_expense_sheet_detail",
        "hotel_proof",
        type_=sa.Text(),
        existing_type=sa.String(length=255),
        nullable=True
    )
    op.alter_column(
        "travel_expense_sheet_detail",
        "daily_allowance_proof",
        type_=sa.Text(),
        existing_type=sa.String(length=255),
        nullable=True
    )
    op.alter_column(
        "travel_expense_sheet_detail",
        "local_conveyance_proof",
        type_=sa.Text(),
        existing_type=sa.String(length=255),
        nullable=True
    )
    op.alter_column(
        "travel_expense_sheet_detail",
        "other_proof",
        type_=sa.Text(),
        existing_type=sa.String(length=255),
        nullable=True
    )

    # ---- travel_expense_sheet_detail_history ----
    op.alter_column(
        "travel_expense_sheet_detail_history",
        "air_rail_bus_proof",
        type_=sa.Text(),
        existing_type=sa.String(length=255),
        nullable=True
    )
    op.alter_column(
        "travel_expense_sheet_detail_history",
        "hotel_proof",
        type_=sa.Text(),
        existing_type=sa.String(length=255),
        nullable=True
    )
    op.alter_column(
        "travel_expense_sheet_detail_history",
        "daily_allowance_proof",
        type_=sa.Text(),
        existing_type=sa.String(length=255),
        nullable=True
    )
    op.alter_column(
        "travel_expense_sheet_detail_history",
        "local_conveyance_proof",
        type_=sa.Text(),
        existing_type=sa.String(length=255),
        nullable=True
    )
    op.alter_column(
        "travel_expense_sheet_detail_history",
        "other_proof",
        type_=sa.Text(),
        existing_type=sa.String(length=255),
        nullable=True
    )


def downgrade():
    # ---- travel_expense_sheet_detail ----
    op.alter_column(
        "travel_expense_sheet_detail",
        "air_rail_bus_proof",
        type_=sa.String(length=255),
        existing_type=sa.Text(),
        nullable=True
    )
    op.alter_column(
        "travel_expense_sheet_detail",
        "hotel_proof",
        type_=sa.String(length=255),
        existing_type=sa.Text(),
        nullable=True
    )
    op.alter_column(
        "travel_expense_sheet_detail",
        "daily_allowance_proof",
        type_=sa.String(length=255),
        existing_type=sa.Text(),
        nullable=True
    )
    op.alter_column(
        "travel_expense_sheet_detail",
        "local_conveyance_proof",
        type_=sa.String(length=255),
        existing_type=sa.Text(),
        nullable=True
    )
    op.alter_column(
        "travel_expense_sheet_detail",
        "other_proof",
        type_=sa.String(length=255),
        existing_type=sa.Text(),
        nullable=True
    )

    # ---- travel_expense_sheet_detail_history ----
    op.alter_column(
        "travel_expense_sheet_detail_history",
        "air_rail_bus_proof",
        type_=sa.String(length=255),
        existing_type=sa.Text(),
        nullable=True
    )
    op.alter_column(
        "travel_expense_sheet_detail_history",
        "hotel_proof",
        type_=sa.String(length=255),
        existing_type=sa.Text(),
        nullable=True
    )
    op.alter_column(
        "travel_expense_sheet_detail_history",
        "daily_allowance_proof",
        type_=sa.String(length=255),
        existing_type=sa.Text(),
        nullable=True
    )
    op.alter_column(
        "travel_expense_sheet_detail_history",
        "local_conveyance_proof",
        type_=sa.String(length=255),
        existing_type=sa.Text(),
        nullable=True
    )
    op.alter_column(
        "travel_expense_sheet_detail_history",
        "other_proof",
        type_=sa.String(length=255),
        existing_type=sa.Text(),
        nullable=True
    )