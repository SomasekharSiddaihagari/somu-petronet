"""add ms_logbook_id to pressure_log_master tables

Revision ID: 65d4a33f4155
Revises: 2c02f7a8b7a2
Create Date: 2026-03-09 11:04:53.221765

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '65d4a33f4155'
down_revision: Union[str, Sequence[str], None] = '2c02f7a8b7a2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():

    # Add column to pressure_log_master
    op.add_column(
        "pressure_log_master",
        sa.Column("ms_logbook_id", sa.Integer(), nullable=True)
    )

    # Add column to pressure_log_master_history
    op.add_column(
        "pressure_log_master_history",
        sa.Column("ms_logbook_id", sa.Integer(), nullable=True)
    )


def downgrade():

    # Remove columns if migration is rolled back
    op.drop_column("pressure_log_master_history", "ms_logbook_id")
    op.drop_column("pressure_log_master", "ms_logbook_id")
