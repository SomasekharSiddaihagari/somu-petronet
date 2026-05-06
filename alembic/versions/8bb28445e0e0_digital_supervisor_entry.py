"""digital supervisor entry

Revision ID: 8bb28445e0e0
Revises: f1a1da79b9b3
Create Date: 2026-01-23 16:09:48.091868

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8bb28445e0e0'
down_revision: Union[str, Sequence[str], None] = 'f1a1da79b9b3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade():
    # =========================
    # supervisor_entry
    # =========================
    op.create_table(
        'supervisor_entry',
        sa.Column('sup_entry_id', sa.Integer(), primary_key=True),
        sa.Column('line_walker_id', sa.Integer(), nullable=True),
        sa.Column('sl_no', sa.Integer(), nullable=True),
        sa.Column('spread', sa.String(length=100), nullable=True),
        sa.Column('supervisor_name', sa.String(length=150), nullable=True),
        sa.Column('start_time', sa.Time(), nullable=True),
        sa.Column('end_time', sa.Time(), nullable=True),
        sa.Column('area_of_visit', sa.String(length=300), nullable=True),
        sa.Column('report', sa.String(length=500), nullable=True),
        sa.Column('officer_initials', sa.String(length=50), nullable=True),
        sa.Column('created_by', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.DateTime(), server_default=sa.func.now(), nullable=True),

        sa.ForeignKeyConstraint(
            ['line_walker_id'],
            ['line_walker_master.line_walker_id'],
            ondelete='CASCADE'
        )
    )

    # =========================
    # supervisor_entry_history
    # =========================
    op.create_table(
        'supervisor_entry_history',
        sa.Column('history_id', sa.Integer(), primary_key=True),
        sa.Column('sup_entry_id', sa.Integer(), nullable=True),
        sa.Column('line_walker_id', sa.Integer(), nullable=True),
        sa.Column('sl_no', sa.Integer(), nullable=True),
        sa.Column('spread', sa.String(length=100), nullable=True),
        sa.Column('supervisor_name', sa.String(length=150), nullable=True),
        sa.Column('start_time', sa.Time(), nullable=True),
        sa.Column('end_time', sa.Time(), nullable=True),
        sa.Column('area_of_visit', sa.String(length=300), nullable=True),
        sa.Column('report', sa.String(length=500), nullable=True),
        sa.Column('officer_initials', sa.String(length=50), nullable=True),
        sa.Column('created_by', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.DateTime(), server_default=sa.func.now(), nullable=True),
    )


def downgrade():
    op.drop_table('supervisor_entry_history')
    op.drop_table('supervisor_entry')