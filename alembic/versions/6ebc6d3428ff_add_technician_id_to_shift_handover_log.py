"""add technician_id to shift handover log

Revision ID: 6ebc6d3428ff
Revises: a37b88e094e1
Create Date: 2026-03-12 15:13:10.629413

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6ebc6d3428ff'
down_revision: Union[str, Sequence[str], None] = 'a37b88e094e1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column(
        "shift_handover_log",
        sa.Column("technician_id", sa.Integer(), nullable=True)
    )

    op.add_column(
        "shift_handover_log_history",
        sa.Column("technician_id", sa.Integer(), nullable=True)
    )


def downgrade():
    op.drop_column("shift_handover_log", "technician_id")
    op.drop_column("shift_handover_log_history", "technician_id")
