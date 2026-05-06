"""add removed_user to circular_target_audience_history

Revision ID: b2a9c58af964
Revises: e74c78c26bf5
Create Date: 2026-03-20 12:27:55.038734

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = 'b2a9c58af964'
down_revision: Union[str, Sequence[str], None] = 'e74c78c26bf5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column(
        "circular_target_audience_history",
        sa.Column(
            "removed_user",
            postgresql.JSONB(astext_type=sa.Text()),
            nullable=True
        )
    )


def downgrade():
    op.drop_column("circular_target_audience_history", "removed_user")
