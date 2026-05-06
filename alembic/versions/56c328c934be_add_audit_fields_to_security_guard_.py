"""add audit fields to security guard report line tables

Revision ID: 56c328c934be
Revises: b2a9c58af964
Create Date: 2026-03-20 15:20:30.497605

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '56c328c934be'
down_revision: Union[str, Sequence[str], None] = 'b2a9c58af964'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # =========================
    # MAIN TABLE
    # =========================
    op.add_column(
        "security_guard_report_line",
        sa.Column("created_at", sa.DateTime(), server_default=sa.func.now())
    )
    op.add_column(
        "security_guard_report_line",
        sa.Column("created_by", sa.Integer(), nullable=True)
    )
    op.add_column(
        "security_guard_report_line",
        sa.Column("updated_at", sa.DateTime(), nullable=True)
    )
    op.add_column(
        "security_guard_report_line",
        sa.Column("updated_by", sa.Integer(), nullable=True)
    )

    # =========================
    # HISTORY TABLE
    # =========================
    op.add_column(
        "security_guard_report_line_history",
        sa.Column("created_at", sa.DateTime(), server_default=sa.func.now())
    )
    op.add_column(
        "security_guard_report_line_history",
        sa.Column("created_by", sa.Integer(), nullable=True)
    )
    op.add_column(
        "security_guard_report_line_history",
        sa.Column("updated_at", sa.DateTime(), nullable=True)
    )
    op.add_column(
        "security_guard_report_line_history",
        sa.Column("updated_by", sa.Integer(), nullable=True)
    )


def downgrade():
    # =========================
    # HISTORY TABLE (DROP FIRST)
    # =========================
    op.drop_column("security_guard_report_line_history", "updated_by")
    op.drop_column("security_guard_report_line_history", "updated_at")
    op.drop_column("security_guard_report_line_history", "created_by")
    op.drop_column("security_guard_report_line_history", "created_at")

    # =========================
    # MAIN TABLE
    # =========================
    op.drop_column("security_guard_report_line", "updated_by")
    op.drop_column("security_guard_report_line", "updated_at")
    op.drop_column("security_guard_report_line", "created_by")
    op.drop_column("security_guard_report_line", "created_at")
