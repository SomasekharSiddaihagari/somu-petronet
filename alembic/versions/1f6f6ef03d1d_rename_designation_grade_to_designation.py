"""rename designation_grade to designation

Revision ID: 1f6f6ef03d1d
Revises: 12bd4937fa4a
Create Date: 2025-12-08 17:47:05.648331

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1f6f6ef03d1d'
down_revision: Union[str, Sequence[str], None] = '12bd4937fa4a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # Drop designation_grade from main table if exists
    op.execute("""
        DO $$
        BEGIN
            IF EXISTS (
                SELECT 1
                FROM information_schema.columns
                WHERE table_name='travel_expense_sheet'
                AND column_name='designation_grade'
            ) THEN
                ALTER TABLE travel_expense_sheet
                DROP COLUMN designation_grade;
            END IF;
        END$$;
    """)
    
    # Drop designation_grade from history table if exists
    op.execute("""
        DO $$
        BEGIN
            IF EXISTS (
                SELECT 1
                FROM information_schema.columns
                WHERE table_name='travel_expense_sheet_history'
                AND column_name='designation_grade'
            ) THEN
                ALTER TABLE travel_expense_sheet_history
                DROP COLUMN designation_grade;
            END IF;
        END$$;
    """)

def downgrade():
    # Optional: Recreate designation_grade if needed
    op.add_column('travel_expense_sheet', sa.Column('designation_grade', sa.String(100), nullable=True))
    op.add_column('travel_expense_sheet_history', sa.Column('designation_grade', sa.String(100), nullable=True))