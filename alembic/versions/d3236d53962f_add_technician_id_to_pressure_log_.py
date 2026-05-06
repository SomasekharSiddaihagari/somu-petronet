"""add technician_id to pressure_log_master tables

Revision ID: d3236d53962f
Revises: c6c9cb37983f
Create Date: 2026-03-16 11:31:58.806053

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd3236d53962f'
down_revision: Union[str, Sequence[str], None] = 'c6c9cb37983f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():

    op.add_column(
        "pressure_log_master",
        sa.Column("technician_id", sa.Integer(), nullable=True)
    )

    op.add_column(
        "pressure_log_master_history",
        sa.Column("technician_id", sa.Integer(), nullable=True)
    )


def downgrade():

    op.drop_column("pressure_log_master", "technician_id")

    op.drop_column("pressure_log_master_history", "technician_id")
