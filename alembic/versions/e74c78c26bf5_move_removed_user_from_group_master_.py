"""move removed_user from group_master_history to circular_master_history

Revision ID: e74c78c26bf5
Revises: 20c600c1194b
Create Date: 2026-03-20 12:06:21.124899

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = 'e74c78c26bf5'
down_revision: Union[str, Sequence[str], None] = '20c600c1194b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # =========================
    # REMOVE FROM OLD TABLE
    # =========================
    op.drop_column("group_master_history", "removed_user")

    # =========================
    # ADD TO NEW TABLE
    # =========================
    op.add_column(
        "circular_master_history",
        sa.Column(
            "removed_user",
            postgresql.JSONB(astext_type=sa.Text()),
            nullable=True
        )
    )


def downgrade():
    # =========================
    # REMOVE FROM NEW TABLE
    # =========================
    op.drop_column("circular_master_history", "removed_user")

    # =========================
    # ADD BACK TO OLD TABLE
    # =========================
    op.add_column(
        "group_master_history",
        sa.Column(
            "removed_user",
            postgresql.JSONB(astext_type=sa.Text()),
            nullable=True
        )
    )
