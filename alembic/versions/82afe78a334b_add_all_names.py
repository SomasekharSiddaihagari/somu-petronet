"""add all names

Revision ID: 82afe78a334b
Revises: f47117feb237
Create Date: 2025-12-11 15:47:56.951087

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '82afe78a334b'
down_revision: Union[str, Sequence[str], None] = 'f47117feb237'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # Add to travel_expense_sheet
    op.add_column(
        'travel_expense_sheet',
        sa.Column('updated_by_supervisor_name', sa.String(150), nullable=True)
    )
    op.add_column(
        'travel_expense_sheet',
        sa.Column('updated_by_hr_name', sa.String(150), nullable=True)
    )
    op.add_column(
        'travel_expense_sheet',
        sa.Column('updated_by_md_name', sa.String(150), nullable=True)
    )
    op.add_column(
        'travel_expense_sheet',
        sa.Column('updated_by_finance_name', sa.String(150), nullable=True)
    )

    # Add to travel_expense_sheet_history
    op.add_column(
        'travel_expense_sheet_history',
        sa.Column('updated_by_supervisor_name', sa.String(150), nullable=True)
    )
    op.add_column(
        'travel_expense_sheet_history',
        sa.Column('updated_by_hr_name', sa.String(150), nullable=True)
    )
    op.add_column(
        'travel_expense_sheet_history',
        sa.Column('updated_by_md_name', sa.String(150), nullable=True)
    )
    op.add_column(
        'travel_expense_sheet_history',
        sa.Column('updated_by_finance_name', sa.String(150), nullable=True)
    )


def downgrade():
    # Remove from travel_expense_sheet
    op.drop_column('travel_expense_sheet', 'updated_by_supervisor_name')
    op.drop_column('travel_expense_sheet', 'updated_by_hr_name')
    op.drop_column('travel_expense_sheet', 'updated_by_md_name')
    op.drop_column('travel_expense_sheet', 'updated_by_finance_name')

    # Remove from travel_expense_sheet_history
    op.drop_column('travel_expense_sheet_history', 'updated_by_supervisor_name')
    op.drop_column('travel_expense_sheet_history', 'updated_by_hr_name')
    op.drop_column('travel_expense_sheet_history', 'updated_by_md_name')
    op.drop_column('travel_expense_sheet_history', 'updated_by_finance_name')