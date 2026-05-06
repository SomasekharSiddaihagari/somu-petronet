"""recreate pressure_log_entry and history

Revision ID: 4caeaa34d57a
Revises: 038bdccd59fe
Create Date: 2026-01-28 17:43:33.729389

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4caeaa34d57a'
down_revision: Union[str, Sequence[str], None] = '038bdccd59fe'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade():
    # ============================
    # DROP OLD TABLES
    # ============================
    op.drop_table('pressure_log_entry_history')
    op.drop_table('pressure_log_entry')

    # ============================
    # CREATE pressure_log_entry
    # ============================
    op.create_table(
        'pressure_log_entry',
        sa.Column('pressure_entry_id', sa.Integer(), primary_key=True, autoincrement=True),

        sa.Column('pressure_id', sa.Integer(), sa.ForeignKey('pressure_log_master.pressure_id', ondelete='CASCADE'), nullable=True),

        sa.Column('sv1_in', sa.String(200), nullable=True),
        sa.Column('sv1_out', sa.String(200), nullable=True),

        sa.Column('sv2_in', sa.String(200), nullable=True),
        sa.Column('sv2_out', sa.String(200), nullable=True),

        sa.Column('sv3_in', sa.String(200), nullable=True),
        sa.Column('sv3_out', sa.String(200), nullable=True),

        sa.Column('sv4_in', sa.String(200), nullable=True),
        sa.Column('sv4_out', sa.String(200), nullable=True),

        sa.Column('sv5_in', sa.String(200), nullable=True),
        sa.Column('sv5_out', sa.String(200), nullable=True),

        sa.Column('sv6_in', sa.String(200), nullable=True),
        sa.Column('sv6_out', sa.String(200), nullable=True),

        sa.Column('sv7_in', sa.String(200), nullable=True),
        sa.Column('sv7_out', sa.String(200), nullable=True),

        sa.Column('sv8_in', sa.String(200), nullable=True),
        sa.Column('sv8_out', sa.String(200), nullable=True),

        sa.Column('sv9_in', sa.String(200), nullable=True),
        sa.Column('sv9_out', sa.String(200), nullable=True),

        sa.Column('sv10_in', sa.String(200), nullable=True),
        sa.Column('sv10_out', sa.String(200), nullable=True),

        sa.Column('entry_date', sa.Date(), nullable=True),
        sa.Column('entry_time', sa.Time(), nullable=True),

        sa.Column('mangalore_1', sa.String(200), nullable=True),
        sa.Column('mangalore_2', sa.String(200), nullable=True),

        sa.Column('neriya_1', sa.String(200), nullable=True),
        sa.Column('neriya_2', sa.String(200), nullable=True),
        sa.Column('neriya_3', sa.String(200), nullable=True),

        sa.Column('hassan_1', sa.String(200), nullable=True),
        sa.Column('hassan_2', sa.String(200), nullable=True),

        sa.Column('ip_1', sa.String(200), nullable=True),
        sa.Column('ip_2', sa.String(200), nullable=True),

        sa.Column('devangonthi_1', sa.String(200), nullable=True),
        sa.Column('devangonthi_2', sa.String(200), nullable=True),

        sa.Column('created_at', sa.DateTime(), server_default=sa.func.now(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.Column('created_by', sa.Integer(), nullable=True),
        sa.Column('updated_by', sa.Integer(), nullable=True),
    )

    # ============================
    # CREATE pressure_log_entry_history
    # ============================
    op.create_table(
        'pressure_log_entry_history',
        sa.Column('history_id', sa.Integer(), primary_key=True, autoincrement=True),

        sa.Column('pressure_entry_id', sa.Integer(), nullable=True),
        sa.Column('pressure_id', sa.Integer(), nullable=True),

        sa.Column('sv1_in', sa.String(200), nullable=True),
        sa.Column('sv1_out', sa.String(200), nullable=True),

        sa.Column('sv2_in', sa.String(200), nullable=True),
        sa.Column('sv2_out', sa.String(200), nullable=True),

        sa.Column('sv3_in', sa.String(200), nullable=True),
        sa.Column('sv3_out', sa.String(200), nullable=True),

        sa.Column('sv4_in', sa.String(200), nullable=True),
        sa.Column('sv4_out', sa.String(200), nullable=True),

        sa.Column('sv5_in', sa.String(200), nullable=True),
        sa.Column('sv5_out', sa.String(200), nullable=True),

        sa.Column('sv6_in', sa.String(200), nullable=True),
        sa.Column('sv6_out', sa.String(200), nullable=True),

        sa.Column('sv7_in', sa.String(200), nullable=True),
        sa.Column('sv7_out', sa.String(200), nullable=True),

        sa.Column('sv8_in', sa.String(200), nullable=True),
        sa.Column('sv8_out', sa.String(200), nullable=True),

        sa.Column('sv9_in', sa.String(200), nullable=True),
        sa.Column('sv9_out', sa.String(200), nullable=True),

        sa.Column('sv10_in', sa.String(200), nullable=True),
        sa.Column('sv10_out', sa.String(200), nullable=True),

        sa.Column('entry_date', sa.Date(), nullable=True),
        sa.Column('entry_time', sa.Time(), nullable=True),

        sa.Column('mangalore_1', sa.String(200), nullable=True),
        sa.Column('mangalore_2', sa.String(200), nullable=True),

        sa.Column('neriya_1', sa.String(200), nullable=True),
        sa.Column('neriya_2', sa.String(200), nullable=True),
        sa.Column('neriya_3', sa.String(200), nullable=True),

        sa.Column('hassan_1', sa.String(200), nullable=True),
        sa.Column('hassan_2', sa.String(200), nullable=True),

        sa.Column('ip_1', sa.String(200), nullable=True),
        sa.Column('ip_2', sa.String(200), nullable=True),

        sa.Column('devangonthi_1', sa.String(200), nullable=True),
        sa.Column('devangonthi_2', sa.String(200), nullable=True),

        sa.Column('created_at', sa.DateTime(), server_default=sa.func.now(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.Column('created_by', sa.Integer(), nullable=True),
        sa.Column('updated_by', sa.Integer(), nullable=True),
    )


def downgrade():
    op.drop_table('pressure_log_entry_history')
    op.drop_table('pressure_log_entry')