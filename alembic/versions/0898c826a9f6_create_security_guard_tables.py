"""create security guard tables

Revision ID: 0898c826a9f6
Revises: 066eff7df2d4
Create Date: 2026-01-20 12:54:31.067365

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0898c826a9f6'
down_revision: Union[str, Sequence[str], None] = '066eff7df2d4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # -------------------------------------------------
    # security_guard_report (MASTER + ENTRY)
    # -------------------------------------------------
    op.create_table(
        "security_guard_report",
        sa.Column("security_guard_id", sa.Integer(), primary_key=True),

        # HEADER
        sa.Column("station_name", sa.String(length=100), nullable=True),
        sa.Column("station_incharge_name", sa.String(length=150), nullable=True),
        sa.Column("shift_code", sa.String(length=20), nullable=True),
        sa.Column("shift_start_time", sa.Time(), nullable=True),
        sa.Column("log_date", sa.Date(), nullable=True),
        sa.Column("document_number", sa.String(length=100), nullable=True),
        sa.Column("status", sa.String(length=50), nullable=True),

        # ENTRY / GRID
        sa.Column("location_name", sa.String(length=100), nullable=True),
        sa.Column("guard_shift", sa.String(length=10), nullable=True),
        sa.Column("security_guard_name", sa.String(length=150), nullable=True),
        sa.Column("duty_start_time", sa.Time(), nullable=True),
        sa.Column("duty_end_time", sa.Time(), nullable=True),
        sa.Column("battery_cp_volt", sa.Numeric(10, 4), nullable=True),
        sa.Column("battery_tel_volt", sa.Numeric(10, 4), nullable=True),
        sa.Column("power_status", sa.String(length=50), nullable=True),
        sa.Column("report_details", sa.Text(), nullable=True),
        sa.Column("officer_initials", sa.String(length=50), nullable=True),

        # FOOTER
        sa.Column("critical_report", sa.Text(), nullable=True),
        sa.Column("shift_a_signature", sa.String(length=255), nullable=True),
        sa.Column("shift_a_name", sa.String(length=100), nullable=True),
        sa.Column("shift_b_signature", sa.String(length=255), nullable=True),
        sa.Column("shift_b_name", sa.String(length=100), nullable=True),
        sa.Column("shift_c_signature", sa.String(length=255), nullable=True),
        sa.Column("shift_c_name", sa.String(length=100), nullable=True),
        sa.Column("station_incharge_signature", sa.String(length=255), nullable=True),
        sa.Column("station_incharge_signed_name", sa.String(length=100), nullable=True),

        # AUDIT
        sa.Column("created_by", sa.Integer(), nullable=True),
        sa.Column("created_at", sa.DateTime(), server_default=sa.func.now(), nullable=True),
    )

    # -------------------------------------------------
    # security_guard_report_history
    # -------------------------------------------------
    op.create_table(
        "security_guard_report_history",
        sa.Column("history_id", sa.Integer(), primary_key=True),

        # HEADER
        sa.Column("station_name", sa.String(length=100), nullable=True),
        sa.Column("station_incharge_name", sa.String(length=150), nullable=True),
        sa.Column("shift_code", sa.String(length=20), nullable=True),
        sa.Column("shift_start_time", sa.Time(), nullable=True),
        sa.Column("log_date", sa.Date(), nullable=True),
        sa.Column("document_number", sa.String(length=100), nullable=True),
        sa.Column("status", sa.String(length=50), nullable=True),

        # ENTRY / GRID
        sa.Column("location_name", sa.String(length=100), nullable=True),
        sa.Column("guard_shift", sa.String(length=10), nullable=True),
        sa.Column("security_guard_name", sa.String(length=150), nullable=True),
        sa.Column("duty_start_time", sa.Time(), nullable=True),
        sa.Column("duty_end_time", sa.Time(), nullable=True),
        sa.Column("battery_cp_volt", sa.Numeric(10, 4), nullable=True),
        sa.Column("battery_tel_volt", sa.Numeric(10, 4), nullable=True),
        sa.Column("power_status", sa.String(length=50), nullable=True),
        sa.Column("report_details", sa.Text(), nullable=True),
        sa.Column("officer_initials", sa.String(length=50), nullable=True),

        # FOOTER
        sa.Column("critical_report", sa.Text(), nullable=True),
        sa.Column("shift_a_signature", sa.String(length=255), nullable=True),
        sa.Column("shift_a_name", sa.String(length=100), nullable=True),
        sa.Column("shift_b_signature", sa.String(length=255), nullable=True),
        sa.Column("shift_b_name", sa.String(length=100), nullable=True),
        sa.Column("shift_c_signature", sa.String(length=255), nullable=True),
        sa.Column("shift_c_name", sa.String(length=100), nullable=True),
        sa.Column("station_incharge_signature", sa.String(length=255), nullable=True),
        sa.Column("station_incharge_signed_name", sa.String(length=100), nullable=True),

        # AUDIT
        sa.Column("created_by", sa.Integer(), nullable=True),
        sa.Column("created_at", sa.DateTime(), server_default=sa.func.now(), nullable=True),
    )


def downgrade():
    op.drop_table("security_guard_report_history")
    op.drop_table("security_guard_report")
