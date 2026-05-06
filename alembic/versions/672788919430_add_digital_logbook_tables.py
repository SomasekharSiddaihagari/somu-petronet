"""add digital logbook tables

Revision ID: 672788919430
Revises: d0a0dbe55245
Create Date: 2026-02-28 12:13:14.270476

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '672788919430'
down_revision: Union[str, Sequence[str], None] = 'd0a0dbe55245'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

"""create digital logbook tables

Revision ID: 20260228_digital_logbook
Revises: 
Create Date: 2026-02-28
"""

from alembic import op
import sqlalchemy as sa




def upgrade():

    # -----------------------------
    # 1️⃣ digital_logbook
    # -----------------------------
    op.create_table(
        'digital_logbook',

        sa.Column('logbook_id', sa.Integer(), primary_key=True, autoincrement=True),

        sa.Column('logbook_ref_no', sa.String(length=50), nullable=True),

        sa.Column('station', sa.String(length=100), nullable=True),
        sa.Column('station_in_charge', sa.String(length=100), nullable=True),
        sa.Column('shift', sa.String(length=20), nullable=True),

        sa.Column('log_date', sa.Date(), nullable=True),
        sa.Column('start_time', sa.Time(), nullable=True),

        sa.Column('handed_over_by', sa.String(length=100), nullable=True),
        sa.Column('taken_over_by', sa.String(length=100), nullable=True),

        # Moved fields
        sa.Column('dkn', sa.String(length=50), nullable=True),
        sa.Column('hsn', sa.String(length=50), nullable=True),
        sa.Column('ner', sa.String(length=50), nullable=True),
        sa.Column('mlr', sa.String(length=50), nullable=True),

        sa.Column('sv1', sa.String(length=50), nullable=True),
        sa.Column('sv2', sa.String(length=50), nullable=True),
        sa.Column('sv3', sa.String(length=50), nullable=True),
        sa.Column('sv4', sa.String(length=50), nullable=True),
        sa.Column('sv5', sa.String(length=50), nullable=True),
        sa.Column('sv6', sa.String(length=50), nullable=True),
        sa.Column('sv7', sa.String(length=50), nullable=True),
        sa.Column('sv8', sa.String(length=50), nullable=True),
        sa.Column('sv9', sa.String(length=50), nullable=True),
        sa.Column('sv10', sa.String(length=50), nullable=True),

        sa.Column('technician_id', sa.Integer(), nullable=True),

        sa.Column('is_shift_closed', sa.Boolean(), nullable=True),
        sa.Column('ms_logbook_id', sa.Integer(), nullable=True),

        sa.Column('created_at', sa.DateTime(), server_default=sa.func.now(), nullable=True),
        sa.Column('created_by', sa.Integer(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.Column('updated_by', sa.Integer(), nullable=True),
    )

    # -----------------------------
    # 2️⃣ digital_logbook_history
    # -----------------------------
    op.create_table(
        'digital_logbook_history',

        sa.Column('history_id', sa.Integer(), primary_key=True, autoincrement=True),

        sa.Column('logbook_id', sa.Integer(), nullable=True),
        sa.Column('logbook_ref_no', sa.String(length=50), nullable=True),

        sa.Column('station', sa.String(length=100), nullable=True),
        sa.Column('station_in_charge', sa.String(length=100), nullable=True),
        sa.Column('shift', sa.String(length=20), nullable=True),

        sa.Column('log_date', sa.Date(), nullable=True),
        sa.Column('start_time', sa.Time(), nullable=True),

        sa.Column('handed_over_by', sa.String(length=100), nullable=True),
        sa.Column('taken_over_by', sa.String(length=100), nullable=True),

        sa.Column('dkn', sa.String(length=50), nullable=True),
        sa.Column('hsn', sa.String(length=50), nullable=True),
        sa.Column('ner', sa.String(length=50), nullable=True),
        sa.Column('mlr', sa.String(length=50), nullable=True),

        sa.Column('sv1', sa.String(length=50), nullable=True),
        sa.Column('sv2', sa.String(length=50), nullable=True),
        sa.Column('sv3', sa.String(length=50), nullable=True),
        sa.Column('sv4', sa.String(length=50), nullable=True),
        sa.Column('sv5', sa.String(length=50), nullable=True),
        sa.Column('sv6', sa.String(length=50), nullable=True),
        sa.Column('sv7', sa.String(length=50), nullable=True),
        sa.Column('sv8', sa.String(length=50), nullable=True),
        sa.Column('sv9', sa.String(length=50), nullable=True),
        sa.Column('sv10', sa.String(length=50), nullable=True),

        sa.Column('technician_id', sa.Integer(), nullable=True),

        sa.Column('is_shift_closed', sa.Boolean(), nullable=True),
        sa.Column('ms_logbook_id', sa.Integer(), nullable=True),

        sa.Column('created_at', sa.DateTime(), server_default=sa.func.now(), nullable=True),
        sa.Column('created_by', sa.Integer(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.Column('updated_by', sa.Integer(), nullable=True),
    )

    # -----------------------------
    # 3️⃣ digital_logbook_entry
    # -----------------------------
    op.create_table(
        'digital_logbook_entry',

        sa.Column('entry_id', sa.Integer(), primary_key=True, autoincrement=True),

        sa.Column(
            'logbook_id',
            sa.Integer(),
            sa.ForeignKey('digital_logbook.logbook_id', ondelete='CASCADE'),
            nullable=True
        ),

        sa.Column('entry_time', sa.Time(), nullable=True),
        sa.Column('location', sa.String(length=100), nullable=True),
        sa.Column('logs', sa.Text(), nullable=True),

        sa.Column('created_at', sa.DateTime(), server_default=sa.func.now(), nullable=True),
        sa.Column('created_by', sa.Integer(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.Column('updated_by', sa.Integer(), nullable=True),
    )

    # -----------------------------
    # 4️⃣ digital_logbook_entry_history
    # -----------------------------
    op.create_table(
        'digital_logbook_entry_history',

        sa.Column('history_id', sa.Integer(), primary_key=True, autoincrement=True),

        sa.Column('entry_id', sa.Integer(), nullable=True),

        sa.Column(
            'logbook_id',
            sa.Integer(),
            sa.ForeignKey('digital_logbook.logbook_id', ondelete='CASCADE'),
            nullable=True
        ),

        sa.Column('entry_time', sa.Time(), nullable=True),
        sa.Column('location', sa.String(length=100), nullable=True),
        sa.Column('logs', sa.Text(), nullable=True),

        sa.Column('created_at', sa.DateTime(), server_default=sa.func.now(), nullable=True),
        sa.Column('created_by', sa.Integer(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.Column('updated_by', sa.Integer(), nullable=True),
    )


def downgrade():
    op.drop_table('digital_logbook_entry_history')
    op.drop_table('digital_logbook_entry')
    op.drop_table('digital_logbook_history')
    op.drop_table('digital_logbook')