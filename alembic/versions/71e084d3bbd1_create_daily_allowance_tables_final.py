"""Create daily allowance tables final

Revision ID: 71e084d3bbd1
Revises: f4ceb91c05dc
Create Date: 2025-12-09 11:18:49.291437

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '71e084d3bbd1'
down_revision: Union[str, Sequence[str], None] = 'f4ceb91c05dc'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # MAIN TABLE
    op.create_table(
        "daily_allowance_sheet",
        sa.Column("da_sheet_id", sa.BigInteger(), primary_key=True, autoincrement=True),
        sa.Column("employee_name", sa.String(150), nullable=True),
        sa.Column("employee_number", sa.String(50), nullable=True),
        sa.Column("designation", sa.String(150), nullable=True),
        sa.Column("grade", sa.String(50), nullable=True),
        sa.Column("station", sa.String(100), nullable=True),
        sa.Column("department", sa.String(100), nullable=True),
        sa.Column("total_excl_gst", sa.Numeric(12, 2), nullable=True),
        sa.Column("total_gst", sa.Numeric(12, 2), nullable=True),
        sa.Column("total_incl_gst", sa.Numeric(12, 2), nullable=True),
        sa.Column("advance_taken", sa.Numeric(12, 2), nullable=True),
        sa.Column("amount_receivable_payable", sa.Numeric(12, 2), nullable=True),
        sa.Column("comments", sa.Text(), nullable=True),
        sa.Column("status", sa.String(50), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            nullable=True,
        ),
    )
 
    # DETAIL TABLE
    op.create_table(
        "daily_allowance_sheet_detail",
        sa.Column("da_sheet_detail_id", sa.BigInteger(), primary_key=True, autoincrement=True),
        sa.Column(
            "da_sheet_id",
            sa.BigInteger(),
            sa.ForeignKey("daily_allowance_sheet.da_sheet_id"),
            nullable=True,
        ),
        sa.Column("date", sa.Date(), nullable=True),
        sa.Column("time_duration", sa.String(50), nullable=True),
        sa.Column("travel_from", sa.String(100), nullable=True),
        sa.Column("travel_to", sa.String(100), nullable=True),
        sa.Column("distance_from_station", sa.String(20), nullable=True),
        sa.Column("purpose", sa.Text(), nullable=True),
        sa.Column("da_amount", sa.Numeric(12, 2), nullable=True),
        sa.Column("da_gst", sa.Numeric(12, 2), nullable=True),
        sa.Column("da_total", sa.Numeric(12, 2), nullable=True),
        sa.Column("da_proof", sa.String(255), nullable=True),
        sa.Column("remarks", sa.Text(), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
        ),
    )
 
    # MAIN HISTORY TABLE
    op.create_table(
        "daily_allowance_sheet_history",
        sa.Column("da_sheet_history_id", sa.BigInteger(), primary_key=True, autoincrement=True),
        sa.Column("da_sheet_id", sa.BigInteger(), nullable=True),
        sa.Column("employee_name", sa.String(150), nullable=True),
        sa.Column("employee_number", sa.String(50), nullable=True),
        sa.Column("designation", sa.String(150), nullable=True),
        sa.Column("grade", sa.String(50), nullable=True),
        sa.Column("station", sa.String(100), nullable=True),
        sa.Column("department", sa.String(100), nullable=True),
        sa.Column("total_excl_gst", sa.Numeric(12, 2), nullable=True),
        sa.Column("total_gst", sa.Numeric(12, 2), nullable=True),
        sa.Column("total_incl_gst", sa.Numeric(12, 2), nullable=True),
        sa.Column("advance_taken", sa.Numeric(12, 2), nullable=True),
        sa.Column("amount_receivable_payable", sa.Numeric(12, 2), nullable=True),
        sa.Column("comments", sa.Text(), nullable=True),
        sa.Column("status", sa.String(50), nullable=True),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
        ),
    )
 
    # DETAIL HISTORY TABLE
    op.create_table(
        "daily_allowance_sheet_detail_history",
        sa.Column("da_sheet_detail_history_id", sa.BigInteger(), primary_key=True, autoincrement=True),
        sa.Column("da_sheet_id", sa.BigInteger(), nullable=True),
        sa.Column("date", sa.Date(), nullable=True),
        sa.Column("time_duration", sa.String(50), nullable=True),
        sa.Column("travel_from", sa.String(100), nullable=True),
        sa.Column("travel_to", sa.String(100), nullable=True),
        sa.Column("distance_from_station", sa.String(20), nullable=True),
        sa.Column("purpose", sa.Text(), nullable=True),
        sa.Column("da_amount", sa.Numeric(12, 2), nullable=True),
        sa.Column("da_gst", sa.Numeric(12, 2), nullable=True),
        sa.Column("da_total", sa.Numeric(12, 2), nullable=True),
        sa.Column("da_proof", sa.String(255), nullable=True),
        sa.Column("remarks", sa.Text(), nullable=True),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
        ),
    )
 
 
def downgrade():
    op.drop_table("daily_allowance_sheet_detail_history")
    op.drop_table("daily_allowance_sheet_history")
    op.drop_table("daily_allowance_sheet_detail")
    op.drop_table("daily_allowance_sheet")
