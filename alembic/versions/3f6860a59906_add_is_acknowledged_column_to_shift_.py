"""add is_acknowledged column to shift_handover_task

Revision ID: 3f6860a59906
Revises: 32e3327d9a75
Create Date: 2026-03-07 12:36:33.892859

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3f6860a59906'
down_revision: Union[str, Sequence[str], None] = '32e3327d9a75'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column(
        "shift_handover_task",
        sa.Column(
            "is_acknowledged",
            sa.Boolean(),
            nullable=True
        )
    )


def downgrade():
    op.drop_column("shift_handover_task", "is_acknowledged")
