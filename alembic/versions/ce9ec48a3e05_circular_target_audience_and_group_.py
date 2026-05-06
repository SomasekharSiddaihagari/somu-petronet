"""circular target audience and group master tables

Revision ID: ce9ec48a3e05
Revises: 00f15ddd722e
Create Date: 2026-02-05 12:56:26.085144

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'ce9ec48a3e05'
down_revision: Union[str, Sequence[str], None] = '00f15ddd722e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade():

    # ================================
    # circular_target_audience
    # ================================
    op.create_table(
        'circular_target_audience',

        sa.Column('audience_id', sa.Integer(), autoincrement=True, primary_key=True),

        sa.Column(
            'circular_id',
            sa.Integer(),
            sa.ForeignKey('circular_master.circular_id'),
            nullable=False
        ),

        sa.Column('audience_type', sa.String(length=50), nullable=True),
        sa.Column('audience_ref_id', sa.Integer(), nullable=True),

        sa.Column('is_deleted', sa.Boolean(), default=True),

        sa.Column('created_by', sa.Integer(), nullable=True),
        sa.Column('created_date', sa.DateTime(), nullable=True),

        sa.Column('updated_by', sa.Integer(), nullable=True),
        sa.Column('updated_date', sa.DateTime(), nullable=True),
    )

    # ================================
    # circular_target_audience_history
    # ================================
    op.create_table(
        'circular_target_audience_history',

        sa.Column('history_id', sa.Integer(), autoincrement=True, primary_key=True),

        sa.Column('circular_id', sa.Integer(), nullable=True),
        sa.Column('audience_type', sa.String(length=50), nullable=True),
        sa.Column('audience_ref_id', sa.Integer(), nullable=True),

        sa.Column('is_deleted', sa.Boolean(), default=False),

        sa.Column('created_by', sa.Integer(), nullable=True),
        sa.Column('created_date', sa.DateTime(), nullable=True),

        sa.Column('updated_by', sa.Integer(), nullable=True),
        sa.Column('updated_date', sa.DateTime(), nullable=True),
    )

    # ================================
    # group_master
    # ================================
    op.create_table(
        'group_master',

        sa.Column('group_id', sa.Integer(), autoincrement=True, primary_key=True),
        sa.Column('group_name', sa.String(length=150), nullable=False, unique=True),
        sa.Column('description', sa.Text(), nullable=True),

        sa.Column('employee_ids', postgresql.JSONB(), nullable=False),

        sa.Column('is_deleted', sa.Boolean(), default=False),

        sa.Column('created_date', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('created_by', sa.Integer(), nullable=True),

        sa.Column('updated_date', sa.DateTime(timezone=True), nullable=True),
        sa.Column('updated_by', sa.Integer(), nullable=True),
    )

    # ================================
    # group_master_history
    # ================================
    op.create_table(
        'group_master_history',

        sa.Column('history_id', sa.Integer(), autoincrement=True, primary_key=True),
        sa.Column('group_id', sa.Integer(), nullable=True),

        sa.Column('group_name', sa.String(length=150), nullable=False, unique=True),
        sa.Column('description', sa.Text(), nullable=True),

        sa.Column('employee_ids', postgresql.JSONB(), nullable=False),

        sa.Column('is_deleted', sa.Boolean(), default=False),

        sa.Column('created_date', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('created_by', sa.Integer(), nullable=True),

        sa.Column('updated_date', sa.DateTime(timezone=True), nullable=True),
        sa.Column('updated_by', sa.Integer(), nullable=True),
    )


def downgrade():
    op.drop_table('group_master_history')
    op.drop_table('group_master')
    op.drop_table('circular_target_audience_history')
    op.drop_table('circular_target_audience')