"""Rename designation_grade and add grade column

Revision ID: 12bd4937fa4a
Revises: d46b5f6ebe63
Create Date: 2025-12-08 17:38:44.054148

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '12bd4937fa4a'
down_revision: Union[str, Sequence[str], None] = 'd46b5f6ebe63'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


from alembic import op
import sqlalchemy as sa

from alembic import op
import sqlalchemy as sa


def upgrade():
    # Rename designation_grade → designation only if column exists and destination not duplicate
    op.execute("""
        DO $$
        BEGIN
            IF EXISTS (
                SELECT 1
                FROM information_schema.columns
                WHERE table_name='travel_expense_sheet_history'
                AND column_name='designation_grade'
            ) THEN
                -- Only rename if 'designation' doesn't already exist
                IF NOT EXISTS (
                    SELECT 1
                    FROM information_schema.columns
                    WHERE table_name='travel_expense_sheet_history'
                    AND column_name='designation'
                ) THEN
                    ALTER TABLE travel_expense_sheet_history
                    RENAME COLUMN designation_grade TO designation;
                END IF;
            END IF;
        END$$;
    """)

    
    op.execute("""
        DO $$
        BEGIN
            IF NOT EXISTS (
                SELECT 1 FROM information_schema.columns
                WHERE table_name='travel_expense_sheet_history'
                AND column_name='grade'
            ) THEN
                ALTER TABLE travel_expense_sheet_history
                ADD COLUMN grade VARCHAR(50);
            END IF;
        END$$;
    """)


def downgrade():
    pass   # optional
