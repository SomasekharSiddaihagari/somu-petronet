"""meals columns alter

Revision ID: f14284729978
Revises: 0203df6fd6b1
Create Date: 2025-12-10 13:03:35.970212

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f14284729978'
down_revision: Union[str, Sequence[str], None] = '0203df6fd6b1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    tables = [
        "meal_allowance_sheet",
        "meal_allowance_sheet_history"
    ]

    for table in tables:
        # Check if column exists
        conn = op.get_bind()
        columns = [c['name'] for c in sa.inspect(conn).get_columns(table)]
        
        if 'designation_grade' in columns:
            # Rename column to 'designation'
            op.alter_column(
                table,
                'designation_grade',
                new_column_name='designation',
                existing_type=sa.String(),
                existing_nullable=True
            )
        else:
            # If designation_grade doesn't exist, create 'designation' if not exists
            if 'designation' not in columns:
                op.add_column(table, sa.Column('designation', sa.String(), nullable=True))


def downgrade():
    tables = [
        "meal_allowance_sheet",
        "meal_allowance_sheet_history"
    ]

    for table in tables:
        conn = op.get_bind()
        columns = [c['name'] for c in sa.inspect(conn).get_columns(table)]

        if 'designation' in columns and 'designation_grade' not in columns:
            # Rename 'designation' back to 'designation_grade'
            op.alter_column(
                table,
                'designation',
                new_column_name='designation_grade',
                existing_type=sa.String(),
                existing_nullable=True
            )