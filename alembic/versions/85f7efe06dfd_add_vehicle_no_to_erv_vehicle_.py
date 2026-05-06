"""add vehicle_no to erv vehicle inspection tables

Revision ID: 85f7efe06dfd
Revises: 56c328c934be
Create Date: 2026-03-20 15:49:48.645213

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '85f7efe06dfd'
down_revision: Union[str, Sequence[str], None] = '56c328c934be'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # =========================
    # MAIN TABLE
    # =========================
    op.add_column(
        "erv_vehicle_inspection_log",
        sa.Column("vehicle_no", sa.String(50), nullable=True)
    )

    # =========================
    # HISTORY TABLE
    # =========================
    op.add_column(
        "erv_vehicle_inspection_log_history",
        sa.Column("vehicle_no", sa.String(50), nullable=True)
    )


def downgrade():
    # =========================
    # HISTORY TABLE (DROP FIRST)
    # =========================
    op.drop_column("erv_vehicle_inspection_log_history", "vehicle_no")

    # =========================
    # MAIN TABLE
    # =========================
    op.drop_column("erv_vehicle_inspection_log", "vehicle_no")
