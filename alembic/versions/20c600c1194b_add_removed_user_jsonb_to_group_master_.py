"""add removed_user jsonb to group_master_history

Revision ID: 20c600c1194b
Revises: 05e3ea84b6cc
Create Date: 2026-03-20 12:01:03.505925

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = '20c600c1194b'
down_revision: Union[str, Sequence[str], None] = '05e3ea84b6cc'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column(
        "group_master_history",
        sa.Column(
            "removed_user",
            postgresql.JSONB(astext_type=sa.Text()),
            nullable=True
        )
    )


def downgrade():
    op.drop_column("group_master_history", "removed_user")
