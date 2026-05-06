"""add active column to user_vehicle

Revision ID: ddfe4549073e
Revises: 3b89f5a3f7fc
Create Date: 2026-02-07 17:27:02.377291

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ddfe4549073e'
down_revision: Union[str, Sequence[str], None] = '3b89f5a3f7fc'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column(
        "user_vehicle",
        sa.Column("active", sa.Boolean(), nullable=True)
    )


def downgrade():
    op.drop_column("user_vehicle", "active")