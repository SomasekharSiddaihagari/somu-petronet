"""Add stationid in admission

Revision ID: 0297ce46c8d4
Revises: 85689b09789a
Create Date: 2026-01-28 11:16:04.804015

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0297ce46c8d4'
down_revision: Union[str, Sequence[str], None] = '85689b09789a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade():
    # Add to main table
    op.add_column(
        'allowance_admission_child',
        sa.Column('station_id', sa.Integer(), nullable=True)
    )

    # Add to history table
    op.add_column(
        'allowance_admission_child_history',
        sa.Column('station_id', sa.Integer(), nullable=True)
    )


def downgrade():
    # Remove from main table
    op.drop_column('allowance_admission_child', 'station_id')

    # Remove from history table
    op.drop_column('allowance_admission_child_history', 'station_id')
