"""add ms_logbook_id to safety checklist tables and is_acknowledged to shift_handover_task_history

Revision ID: 38173b013b1d
Revises: 3f6860a59906
Create Date: 2026-03-07 14:53:55.172928

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '38173b013b1d'
down_revision: Union[str, Sequence[str], None] = '3f6860a59906'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():

    # ---------------------------------------------------
    # Add ms_logbook_id to safety checklist tables
    # ---------------------------------------------------
    op.add_column(
        "daily_safety_checklist",
        sa.Column("ms_logbook_id", sa.Integer(), nullable=True)
    )

    op.add_column(
        "daily_safety_checklist_history",
        sa.Column("ms_logbook_id", sa.Integer(), nullable=True)
    )

    # ---------------------------------------------------
    # Add is_acknowledged to shift_handover_task_history
    # ---------------------------------------------------
    op.add_column(
        "shift_handover_task_history",
        sa.Column("is_acknowledged", sa.Boolean(), nullable=True)
    )


def downgrade():

    # Remove fields in reverse order
    op.drop_column("shift_handover_task_history", "is_acknowledged")

    op.drop_column("daily_safety_checklist_history", "ms_logbook_id")

    op.drop_column("daily_safety_checklist", "ms_logbook_id")
