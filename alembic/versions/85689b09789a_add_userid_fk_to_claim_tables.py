"""Add userid FK to claim tables

Revision ID: 85689b09789a
Revises: ca2e625a2e74
Create Date: 2026-01-27 16:32:59.932465

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '85689b09789a'
down_revision: Union[str, Sequence[str], None] = 'ca2e625a2e74'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade():
    # ==============================
    # MAIN TABLE: allowance_admission_child
    # ==============================

    # Drop any FK on userid safely (Postgres)
    op.execute("""
    DO $$
    DECLARE
        constraint_name text;
    BEGIN
        SELECT conname INTO constraint_name
        FROM pg_constraint
        WHERE conrelid = 'allowance_admission_child'::regclass
          AND contype = 'f';

        IF constraint_name IS NOT NULL THEN
            EXECUTE format(
                'ALTER TABLE allowance_admission_child DROP CONSTRAINT %I',
                constraint_name
            );
        END IF;
    END$$;
    """)

    # Rename column userid -> user_id (MAIN)
    op.alter_column(
        "allowance_admission_child",
        "userid",
        new_column_name="user_id",
        existing_type=sa.Integer(),
    )

    # ==============================
    # HISTORY TABLE
    # ==============================

    # Rename column userid -> user_id (HISTORY)
    op.alter_column(
        "allowance_admission_child_history",
        "userid",
        new_column_name="user_id",
        existing_type=sa.BigInteger(),
    )


def downgrade():
    # ==============================
    # HISTORY TABLE
    # ==============================
    op.alter_column(
        "allowance_admission_child_history",
        "user_id",
        new_column_name="userid",
        existing_type=sa.BigInteger(),
    )

    # ==============================
    # MAIN TABLE
    # ==============================
    op.alter_column(
        "allowance_admission_child",
        "user_id",
        new_column_name="userid",
        existing_type=sa.Integer(),
    )