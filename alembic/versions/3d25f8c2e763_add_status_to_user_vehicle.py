"""add status to user vehicle

Revision ID: 3d25f8c2e763
Revises: f4e60d584385
Create Date: 2026-01-02 15:42:05.441901

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3d25f8c2e763'
down_revision: Union[str, Sequence[str], None] = 'f4e60d584385'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # user_vehicle
    op.add_column(
        "user_vehicle",
        sa.Column("status", sa.String(), nullable=True)
    )

    # user_vehicle_history
    op.add_column(
        "user_vehicle_history",
        sa.Column("status", sa.String(), nullable=True)
    )


def downgrade():
    # user_vehicle_history
    op.drop_column("user_vehicle_history", "status")

    # user_vehicle
    op.drop_column("user_vehicle", "status")