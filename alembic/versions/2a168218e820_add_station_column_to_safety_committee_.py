"""add station column to safety committee tables

Revision ID: 2a168218e820
Revises: d2893aa6a575
Create Date: 2026-02-26 13:49:26.391810

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2a168218e820'
down_revision: Union[str, Sequence[str], None] = 'd2893aa6a575'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade():
    # Add station column to safety_committee_minutes
    op.add_column(
        "safety_committee_minutes",
        sa.Column("station", sa.Integer(), nullable=True)
    )

    # Add station column to safety_committee_minutes_history
    op.add_column(
        "safety_committee_minutes_history",
        sa.Column("station", sa.Integer(), nullable=True)
    )


def downgrade():
    # Remove station column from safety_committee_minutes
    op.drop_column("safety_committee_minutes", "station")

    # Remove station column from safety_committee_minutes_history
    op.drop_column("safety_committee_minutes_history", "station")