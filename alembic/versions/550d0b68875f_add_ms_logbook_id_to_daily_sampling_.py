"""add ms_logbook_id to daily sampling master tables

Revision ID: 550d0b68875f
Revises: e1bb8a177f1c
Create Date: 2026-03-11 16:30:05.173787

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '550d0b68875f'
down_revision: Union[str, Sequence[str], None] = 'e1bb8a177f1c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column(
        "daily_sampling_master",
        sa.Column("ms_logbook_id", sa.Integer(), nullable=True)
    )

    op.add_column(
        "daily_sampling_master_history",
        sa.Column("ms_logbook_id", sa.Integer(), nullable=True)
    )


def downgrade():
    op.drop_column("daily_sampling_master_history", "ms_logbook_id")
    op.drop_column("daily_sampling_master", "ms_logbook_id")
