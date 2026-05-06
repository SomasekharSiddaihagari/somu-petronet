"""add financial_year to employee_form_12c tables updated

Revision ID: b5b9557b73c4
Revises: dffe4c99f4a6
Create Date: 2025-11-28 17:11:07.236629

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b5b9557b73c4'
down_revision: Union[str, Sequence[str], None] = 'dffe4c99f4a6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # Add column to main table
    op.add_column(
        'employee_form_12c',
        sa.Column('financial_year', sa.String(), nullable=True)
    )
 
    # Add column to history table
    op.add_column(
        'employee_form_12c_history',
        sa.Column('financial_year', sa.String(), nullable=True)
    )
 
 
def downgrade():
    op.drop_column('employee_form_12c', 'financial_year')
    op.drop_column('employee_form_12c_history', 'financial_year')