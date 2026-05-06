"""add user_id to investigation team

Revision ID: 33ab4e34cfd7
Revises: 3aa27244b8bb
Create Date: 2026-02-16 20:25:48.300956

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '33ab4e34cfd7'
down_revision: Union[str, Sequence[str], None] = '3aa27244b8bb'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column(
        "incident_investigation_team",
        sa.Column("user_id", sa.Integer(), nullable=True)
    )

    op.add_column(
        "incident_investigation_team_history",
        sa.Column("user_id", sa.Integer(), nullable=True)
    )


def downgrade():
    op.drop_column("incident_investigation_team", "user_id")
    op.drop_column("incident_investigation_team_history", "user_id")