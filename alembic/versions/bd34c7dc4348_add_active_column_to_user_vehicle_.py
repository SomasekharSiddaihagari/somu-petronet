"""add active column to user_vehicle_history

Revision ID: bd34c7dc4348
Revises: ddfe4549073e
Create Date: 2026-02-07 18:08:28.375935

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'bd34c7dc4348'
down_revision: Union[str, Sequence[str], None] = 'ddfe4549073e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column(
        "user_vehicle_history",
        sa.Column("active", sa.Boolean(), nullable=True)
    )


def downgrade():
    op.drop_column("user_vehicle_history", "active")