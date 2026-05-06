"""add station_id to safety committee minutes

Revision ID: 36878207300d
Revises: b02c4c0e866b
Create Date: 2026-02-26 15:08:00.941759

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '36878207300d'
down_revision: Union[str, Sequence[str], None] = 'b02c4c0e866b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # ======================================
    # safety_committee_minutes
    # ======================================
    op.add_column(
        "safety_committee_minutes",
        sa.Column("station_id", sa.Integer(), nullable=True),
    )

    # ======================================
    # safety_committee_minutes_history
    # ======================================
    op.add_column(
        "safety_committee_minutes_history",
        sa.Column("station_id", sa.Integer(), nullable=True),
    )


def downgrade():
    op.drop_column("safety_committee_minutes", "station_id")
    op.drop_column("safety_committee_minutes_history", "station_id")

