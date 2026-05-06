"""add location_name and shift to security_guard_report_line

Revision ID: 05e3ea84b6cc
Revises: 45871a4859f1
Create Date: 2026-03-18 22:37:50.079961

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '05e3ea84b6cc'
down_revision: Union[str, Sequence[str], None] = '45871a4859f1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # =========================
    # MAIN LINE TABLE
    # =========================
    op.add_column(
        "security_guard_report_line",
        sa.Column("location_name", sa.String(100), nullable=True)
    )

    op.add_column(
        "security_guard_report_line",
        sa.Column("shift", sa.String(10), nullable=True)
    )

    # =========================
    # HISTORY LINE TABLE
    # =========================
    op.add_column(
        "security_guard_report_line_history",
        sa.Column("location_name", sa.String(100), nullable=True)
    )

    op.add_column(
        "security_guard_report_line_history",
        sa.Column("shift", sa.String(10), nullable=True)
    )


def downgrade():
    # =========================
    # HISTORY TABLE (DROP FIRST)
    # =========================
    op.drop_column("security_guard_report_line_history", "shift")
    op.drop_column("security_guard_report_line_history", "location_name")

    # =========================
    # MAIN TABLE
    # =========================
    op.drop_column("security_guard_report_line", "shift")
    op.drop_column("security_guard_report_line", "location_name")
