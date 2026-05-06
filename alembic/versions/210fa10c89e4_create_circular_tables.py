"""create circular tables

Revision ID: 210fa10c89e4
Revises: 06389f4afa0e
Create Date: 2026-02-11 20:07:54.815977

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '210fa10c89e4'
down_revision: Union[str, Sequence[str], None] = '06389f4afa0e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column(
        "circular_target_audience",
        sa.Column("version", sa.Integer(), nullable=False, server_default="1")
    )

    op.add_column(
        "circular_target_audience_history",
        sa.Column("version", sa.Integer(), nullable=False, server_default="1")
    )

    # remove default after creation (optional clean)
    op.alter_column("circular_target_audience", "version", server_default=None)
    op.alter_column("circular_target_audience_history", "version", server_default=None)


def downgrade():
    op.drop_column("circular_target_audience", "version")
    op.drop_column("circular_target_audience_history", "version")