"""update circular target audience tables

Revision ID: 559a667b1cd9
Revises: a563598a2c05
Create Date: 2026-02-06
"""

from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers
revision: str = '559a667b1cd9'
down_revision: Union[str, Sequence[str], None] = 'a563598a2c05'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():

    # =====================================================
    # circular_target_audience
    # =====================================================

    # 1. Drop is_deleted
    op.drop_column('circular_target_audience', 'is_deleted')

    # 2. Convert Integer -> JSONB safely
    op.alter_column(
        'circular_target_audience',
        'audience_ref_id',
        existing_type=sa.Integer(),
        type_=postgresql.JSONB(),
        postgresql_using='to_jsonb(audience_ref_id)'
    )

    # 3. Fix created_date default from DB side
    op.alter_column(
        'circular_target_audience',
        'created_date',
        existing_type=sa.DateTime(),
        server_default=sa.text('now()')
    )

    # =====================================================
    # circular_target_audience_history
    # =====================================================

    # 1. Drop is_deleted
    op.drop_column('circular_target_audience_history', 'is_deleted')

    # 2. Convert Integer -> JSONB safely
    op.alter_column(
        'circular_target_audience_history',
        'audience_ref_id',
        existing_type=sa.Integer(),
        type_=postgresql.JSONB(),
        postgresql_using='to_jsonb(audience_ref_id)'
    )

    # 3. Fix created_date default
    op.alter_column(
        'circular_target_audience_history',
        'created_date',
        existing_type=sa.DateTime(),
        server_default=sa.text('now()')
    )


def downgrade():

    # =====================================================
    # circular_target_audience
    # =====================================================

    op.alter_column(
        'circular_target_audience',
        'audience_ref_id',
        existing_type=postgresql.JSONB(),
        type_=sa.Integer(),
        postgresql_using='(audience_ref_id)::integer'
    )

    op.add_column(
        'circular_target_audience',
        sa.Column('is_deleted', sa.Boolean(), nullable=True)
    )

    op.alter_column(
        'circular_target_audience',
        'created_date',
        server_default=None
    )

    # =====================================================
    # circular_target_audience_history
    # =====================================================

    op.alter_column(
        'circular_target_audience_history',
        'audience_ref_id',
        existing_type=postgresql.JSONB(),
        type_=sa.Integer(),
        postgresql_using='(audience_ref_id)::integer'
    )

    op.add_column(
        'circular_target_audience_history',
        sa.Column('is_deleted', sa.Boolean(), nullable=True)
    )

    op.alter_column(
        'circular_target_audience_history',
        'created_date',
        server_default=None
    )
