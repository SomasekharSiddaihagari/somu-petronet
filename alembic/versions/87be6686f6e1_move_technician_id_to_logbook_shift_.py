"""move technician_id to logbook_shift_master

Revision ID: 87be6686f6e1
Revises: 6ebc6d3428ff
Create Date: 2026-03-12 15:25:30.028706

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '87be6686f6e1'
down_revision: Union[str, Sequence[str], None] = '6ebc6d3428ff'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():

    # Remove from old tables
    op.drop_column("shift_handover_log", "technician_id")
    op.drop_column("shift_handover_log_history", "technician_id")

    # Add to correct tables
    op.add_column(
        "logbook_shift_master",
        sa.Column("technician_id", sa.Integer(), nullable=True)
    )

    op.add_column(
        "logbook_shift_master_history",
        sa.Column("technician_id", sa.Integer(), nullable=True)
    )


def downgrade():

    # Remove from new tables
    op.drop_column("logbook_shift_master", "technician_id")
    op.drop_column("logbook_shift_master_history", "technician_id")

    # Add back to old tables
    op.add_column(
        "shift_handover_log",
        sa.Column("technician_id", sa.Integer(), nullable=True)
    )

    op.add_column(
        "shift_handover_log_history",
        sa.Column("technician_id", sa.Integer(), nullable=True)
    )
