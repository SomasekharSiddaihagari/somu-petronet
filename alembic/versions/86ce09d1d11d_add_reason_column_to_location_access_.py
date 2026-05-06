"""add reason column to location access tables

Revision ID: 86ce09d1d11d
Revises: c8f05c8be613
Create Date: 2026-03-06 11:54:25.489538

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '86ce09d1d11d'
down_revision: Union[str, Sequence[str], None] = 'c8f05c8be613'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():

    op.add_column(
        "location_access_approval",
        sa.Column("reason", sa.Text(), nullable=True)
    )


def downgrade():

    op.drop_column("location_access_approval", "reason")

