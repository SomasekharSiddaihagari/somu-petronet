"""add from and to dates

Revision ID: bb7dc0631438
Revises: 3f2d19d92b7f
Create Date: 2025-12-11 17:33:56.412941

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'bb7dc0631438'
down_revision: Union[str, Sequence[str], None] = '3f2d19d92b7f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade():

    # -------------------------------
    # 1) daily_allowance_sheet_detail
    # -------------------------------
    # Rename date -> from_date
    op.alter_column(
        'daily_allowance_sheet_detail',
        'date',
        new_column_name='from_date',
        existing_type=sa.Date()
    )

    # Add to_date
    op.add_column(
        'daily_allowance_sheet_detail',
        sa.Column('to_date', sa.Date(), nullable=True)
    )

    # --------------------------------------
    # 2) daily_allowance_sheet_detail_history
    # --------------------------------------
    # Rename date -> from_date
    op.alter_column(
        'daily_allowance_sheet_detail_history',
        'date',
        new_column_name='from_date',
        existing_type=sa.Date()
    )

    # Add to_date
    op.add_column(
        'daily_allowance_sheet_detail_history',
        sa.Column('to_date', sa.Date(), nullable=True)
    )


def downgrade():

    # -------------------------------
    # 1) daily_allowance_sheet_detail
    # -------------------------------
    op.drop_column('daily_allowance_sheet_detail', 'to_date')

    op.alter_column(
        'daily_allowance_sheet_detail',
        'from_date',
        new_column_name='date',
        existing_type=sa.Date()
    )

    # --------------------------------------
    # 2) daily_allowance_sheet_detail_history
    # --------------------------------------
    op.drop_column('daily_allowance_sheet_detail_history', 'to_date')

    op.alter_column(
        'daily_allowance_sheet_detail_history',
        'from_date',
        new_column_name='date',
        existing_type=sa.Date()
    )