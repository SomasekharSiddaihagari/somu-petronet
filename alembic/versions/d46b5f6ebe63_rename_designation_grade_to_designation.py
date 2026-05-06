"""Rename designation_grade to designation

Revision ID: d46b5f6ebe63
Revises: 9a0f5498c537
Create Date: 2025-12-08 17:19:30.917001

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd46b5f6ebe63'
down_revision: Union[str, Sequence[str], None] = '9a0f5498c537'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade():
    # MAIN TABLE
    op.alter_column(
        'travel_expense_sheet',
        'designation_grade',
        new_column_name='designation'
    )

    # HISTORY TABLE
    op.alter_column(
        'travel_expense_sheet_history',
        'grade',
        new_column_name='designation'
    )


def downgrade():
    # MAIN TABLE
    op.alter_column(
        'travel_expense_sheet',
        'designation',
        new_column_name='designation_grade'
    )

    # HISTORY TABLE
    op.alter_column(
        'travel_expense_sheet_history',
        'designation',
        new_column_name='grade'
    )