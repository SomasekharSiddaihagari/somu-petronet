"""add ms_logbook_id and technician_id to security guard tables

Revision ID: 45871a4859f1
Revises: 9ab4f413c50f
Create Date: 2026-03-17 18:03:03.541678

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '45871a4859f1'
down_revision: Union[str, Sequence[str], None] = '9ab4f413c50f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # =========================
    # MAIN TABLE
    # =========================
    op.add_column(
        "security_guard_report",
        sa.Column("ms_logbook_id", sa.Integer(), nullable=True)
    )

    op.add_column(
        "security_guard_report",
        sa.Column("technician_id", sa.Integer(), nullable=True)
    )

    # =========================
    # HISTORY TABLE
    # =========================
    op.add_column(
        "security_guard_report_history",
        sa.Column("ms_logbook_id", sa.Integer(), nullable=True)
    )

    op.add_column(
        "security_guard_report_history",
        sa.Column("technician_id", sa.Integer(), nullable=True)
    )


def downgrade():
    # =========================
    # HISTORY TABLE (DROP FIRST)
    # =========================
    op.drop_column("security_guard_report_history", "technician_id")
    op.drop_column("security_guard_report_history", "ms_logbook_id")

    # =========================
    # MAIN TABLE
    # =========================
    op.drop_column("security_guard_report", "technician_id")
    op.drop_column("security_guard_report", "ms_logbook_id")
