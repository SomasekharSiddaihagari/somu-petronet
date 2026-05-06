"""create circular_user_activity and history tables

Revision ID: 9cd2ed1e4703
Revises: f8bd6ad0c2ad
Create Date: 2026-02-06 15:59:42.345157

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9cd2ed1e4703'
down_revision: Union[str, Sequence[str], None] = 'f8bd6ad0c2ad'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # ---------------- main table ----------------
    op.create_table(
        'circular_user_activity',
        sa.Column('circular_user_activity_id', sa.Integer(), primary_key=True, index=True),
        sa.Column('circular_id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),

        sa.Column('is_read', sa.Boolean(), default=False),
        sa.Column('is_acknowledged', sa.Boolean(), default=False),

        sa.Column('read_at', sa.DateTime(), nullable=True),
        sa.Column('acknowledged_at', sa.DateTime(), nullable=True),

        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
    )

    # ---------------- history table ----------------
    op.create_table(
        'circular_user_activity_history',
        sa.Column('history_id', sa.Integer(), primary_key=True, index=True),
        sa.Column('circular_user_activity_id', sa.Integer(), nullable=False),

        sa.Column('circular_id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),

        sa.Column('is_read', sa.Boolean(), default=False),
        sa.Column('is_acknowledged', sa.Boolean(), default=False),

        sa.Column('read_at', sa.DateTime(), nullable=True),
        sa.Column('acknowledged_at', sa.DateTime(), nullable=True),

        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),

        sa.Column('action', sa.String(), nullable=True),
    )


def downgrade():
    op.drop_table('circular_user_activity_history')
    op.drop_table('circular_user_activity')