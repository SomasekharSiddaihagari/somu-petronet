"""history of travel update

Revision ID: b46224953fb1
Revises: 18bd9f32f21c
Create Date: 2025-12-11 18:53:22.271463

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b46224953fb1'
down_revision: Union[str, Sequence[str], None] = '18bd9f32f21c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade():
    # Add missing approval tracking columns
    op.add_column('travel_expense_sheet_history', sa.Column('updated_by_supervisor', sa.Date(), nullable=True))
    op.add_column('travel_expense_sheet_history', sa.Column('updated_by_hr', sa.Date(), nullable=True))
    op.add_column('travel_expense_sheet_history', sa.Column('updated_by_md', sa.Date(), nullable=True))
    op.add_column('travel_expense_sheet_history', sa.Column('updated_by_finance', sa.Date(), nullable=True))
    op.add_column('travel_expense_sheet_history', sa.Column('supervisor_comments', sa.Text(), nullable=True))
    op.add_column('travel_expense_sheet_history', sa.Column('hr_comments', sa.Text(), nullable=True))
    op.add_column('travel_expense_sheet_history', sa.Column('finance_comments', sa.Text(), nullable=True))


def downgrade():
    # Remove the columns if downgrading
    op.drop_column('travel_expense_sheet_history', 'updated_by_supervisor')
    op.drop_column('travel_expense_sheet_history', 'updated_by_hr')
    op.drop_column('travel_expense_sheet_history', 'updated_by_md')
    op.drop_column('travel_expense_sheet_history', 'updated_by_finance')
    op.drop_column('travel_expense_sheet_history', 'supervisor_comments')
    op.drop_column('travel_expense_sheet_history', 'hr_comments')
    op.drop_column('travel_expense_sheet_history', 'finance_comments')