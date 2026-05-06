"""create security guard report line tables with extra column

Revision ID: 9ab4f413c50f
Revises: 39f564e00b48
Create Date: 2026-03-17 16:43:09.167744

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9ab4f413c50f'
down_revision: Union[str, Sequence[str], None] = '39f564e00b48'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # =========================
    # CREATE MAIN LINE TABLE
    # =========================
    op.create_table(
        "security_guard_report_line",

        sa.Column("sgrl_id", sa.Integer(), primary_key=True),

        sa.Column(
            "report_id",
            sa.Integer(),
            sa.ForeignKey(
                "security_guard_report.security_guard_id",
                ondelete="CASCADE"
            ),
            nullable=True
        ),

        sa.Column("security_guard_name", sa.String(150), nullable=True),
        sa.Column("security_guard_name_two", sa.String(150), nullable=True),

        sa.Column("duty_start_time", sa.Time(), nullable=True),
        sa.Column("duty_end_time", sa.Time(), nullable=True),

        sa.Column("battery_cp_volt", sa.Numeric(10, 4), nullable=True),
        sa.Column("battery_tel_volt", sa.Numeric(10, 4), nullable=True),

        sa.Column("power_status", sa.String(50), nullable=True),
        sa.Column("report_details", sa.Text(), nullable=True),
        sa.Column("officer_initials", sa.String(50), nullable=True),
    )

    # INDEX (optional but recommended)
    op.create_index(
        "ix_sgrl_report_id",
        "security_guard_report_line",
        ["report_id"]
    )

    # =========================
    # CREATE HISTORY LINE TABLE
    # =========================
    op.create_table(
        "security_guard_report_line_history",

        sa.Column("sgrl_history_id", sa.Integer(), primary_key=True),

        sa.Column(
            "history_id",
            sa.Integer(),
            sa.ForeignKey(
                "security_guard_report_history.history_id",
                ondelete="CASCADE"
            ),
            nullable=False
        ),

        sa.Column("sgrl_id", sa.Integer(), nullable=True),

        sa.Column("security_guard_name", sa.String(150), nullable=True),
        sa.Column("security_guard_name_two", sa.String(150), nullable=True),

        sa.Column("duty_start_time", sa.Time(), nullable=True),
        sa.Column("duty_end_time", sa.Time(), nullable=True),

        sa.Column("battery_cp_volt", sa.Numeric(10, 4), nullable=True),
        sa.Column("battery_tel_volt", sa.Numeric(10, 4), nullable=True),

        sa.Column("power_status", sa.String(50), nullable=True),
        sa.Column("report_details", sa.Text(), nullable=True),
        sa.Column("officer_initials", sa.String(50), nullable=True),
    )

    # INDEX (optional)
    op.create_index(
        "ix_sgrl_history_id",
        "security_guard_report_line_history",
        ["history_id"]
    )


def downgrade():
    # =========================
    # DROP HISTORY TABLE FIRST
    # =========================
    op.drop_index("ix_sgrl_history_id", table_name="security_guard_report_line_history")
    op.drop_table("security_guard_report_line_history")

    # =========================
    # DROP MAIN LINE TABLE
    # =========================
    op.drop_index("ix_sgrl_report_id", table_name="security_guard_report_line")
    op.drop_table("security_guard_report_line")
