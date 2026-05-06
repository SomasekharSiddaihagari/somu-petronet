"""create line walker tables

Revision ID: 066eff7df2d4
Revises: d5c2e0d63f23
Create Date: 2026-01-20 12:51:32.194583

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '066eff7df2d4'
down_revision: Union[str, Sequence[str], None] = 'd5c2e0d63f23'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade():
    # -----------------------------
    # line_walker_master
    # -----------------------------
    op.create_table(
        "line_walker_master",
        sa.Column("line_walker_id", sa.Integer(), primary_key=True),
        sa.Column("document_no", sa.String(length=50), nullable=True),
        sa.Column("station_name", sa.String(length=100), nullable=True),
        sa.Column("station_incharge_name", sa.String(length=150), nullable=True),
        sa.Column("shift_name", sa.String(length=20), nullable=True),
        sa.Column("shift_start_time", sa.Time(), nullable=True),
        sa.Column("log_date", sa.Date(), nullable=True),
        sa.Column("reporting_location", sa.String(length=200), nullable=True),
        sa.Column("critical_report", sa.Text(), nullable=True),
        sa.Column("station_incharge_signature", sa.String(length=200), nullable=True),
        sa.Column("created_by", sa.Integer(), nullable=True),
        sa.Column("created_at", sa.DateTime(), server_default=sa.func.now(), nullable=True),
    )

    # -----------------------------
    # line_walker_master_history
    # -----------------------------
    op.create_table(
        "line_walker_master_history",
        sa.Column("history_id", sa.Integer(), primary_key=True),
        sa.Column("station_name", sa.String(length=100), nullable=True),
        sa.Column("line_walker_id", sa.Integer(), nullable=True),
        sa.Column("station_incharge_name", sa.String(length=150), nullable=True),
        sa.Column("shift_start_time", sa.Time(), nullable=True),
        sa.Column("shift_name", sa.String(length=10), nullable=True),
        sa.Column("reporting_location", sa.String(length=200), nullable=True),
        sa.Column("report_date", sa.Date(), nullable=True),
        sa.Column("log_date", sa.Date(), nullable=True),
        sa.Column("station_incharge_signature", sa.String(length=200), nullable=True),
        sa.Column("critical_report", sa.Text(), nullable=True),
        sa.Column("created_by", sa.Integer(), nullable=True),
        sa.Column("updated_at", sa.DateTime(), server_default=sa.func.now(), nullable=True),
    )

    # -----------------------------
    # line_walker_entry
    # -----------------------------
    op.create_table(
        "line_walker_entry",
        sa.Column("line_entry_id", sa.Integer(), primary_key=True),
        sa.Column(
            "line_walker_id",
            sa.Integer(),
            sa.ForeignKey("line_walker_master.line_walker_id", ondelete="CASCADE"),
            nullable=True,
        ),
        sa.Column("location_from", sa.String(length=100), nullable=True),
        sa.Column("location_to", sa.String(length=100), nullable=True),
        sa.Column("walker_name", sa.String(length=150), nullable=True),
        sa.Column("start_time", sa.Time(), nullable=True),
        sa.Column("start_officer_initials", sa.String(length=50), nullable=True),
        sa.Column("end_time", sa.Time(), nullable=True),
        sa.Column("end_officer_initials", sa.String(length=50), nullable=True),
        sa.Column("device_status", sa.String(length=100), nullable=True),
        sa.Column("remarks", sa.String(length=500), nullable=True),
        sa.Column("created_at", sa.DateTime(), server_default=sa.func.now(), nullable=True),
    )

    # -----------------------------
    # line_walker_entry_history
    # -----------------------------
    op.create_table(
        "line_walker_entry_history",
        sa.Column("history_id", sa.Integer(), primary_key=True),
        sa.Column("line_entry_id", sa.Integer(), nullable=True),
        sa.Column("line_walker_id", sa.Integer(), nullable=True),
        sa.Column("location_from", sa.String(length=100), nullable=True),
        sa.Column("location_to", sa.String(length=100), nullable=True),
        sa.Column("walker_name", sa.String(length=150), nullable=True),
        sa.Column("start_time", sa.Time(), nullable=True),
        sa.Column("start_officer_initials", sa.String(length=50), nullable=True),
        sa.Column("end_time", sa.Time(), nullable=True),
        sa.Column("end_officer_initials", sa.String(length=50), nullable=True),
        sa.Column("device_status", sa.String(length=100), nullable=True),
        sa.Column("remarks", sa.String(length=500), nullable=True),
        sa.Column("updated_by", sa.Integer(), nullable=True),
        sa.Column("created_at", sa.DateTime(), server_default=sa.func.now(), nullable=True),
    )


def downgrade():
    op.drop_table("line_walker_entry_history")
    op.drop_table("line_walker_entry")
    op.drop_table("line_walker_master_history")
    op.drop_table("line_walker_master")