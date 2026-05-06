"""change start_time and stop_time to datetime in dg tables

Revision ID: 7614c431e5b6
Revises: 5ce07be26e80
Create Date: 2026-03-23 11:32:30.824422

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7614c431e5b6'
down_revision: Union[str, Sequence[str], None] = '5ce07be26e80'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # =========================
    # MAIN TABLE
    # =========================
    op.alter_column(
        "dg_250kva_entry",
        "start_time",
        existing_type=sa.Time(),
        type_=sa.DateTime(),
        existing_nullable=True
    )

    op.alter_column(
        "dg_250kva_entry",
        "stop_time",
        existing_type=sa.Time(),
        type_=sa.DateTime(),
        existing_nullable=True
    )

    # =========================
    # HISTORY TABLE
    # =========================
    op.alter_column(
        "dg_250kva_entry_history",
        "start_time",
        existing_type=sa.Time(),
        type_=sa.DateTime(),
        existing_nullable=True
    )

    op.alter_column(
        "dg_250kva_entry_history",
        "stop_time",
        existing_type=sa.Time(),
        type_=sa.DateTime(),
        existing_nullable=True
    )


def upgrade():
    # =========================
    # MAIN TABLE
    # =========================
    op.execute("""
        ALTER TABLE dg_250kva_entry
        ALTER COLUMN start_time TYPE TIMESTAMP
        USING (CURRENT_DATE + start_time)
    """)

    op.execute("""
        ALTER TABLE dg_250kva_entry
        ALTER COLUMN stop_time TYPE TIMESTAMP
        USING (CURRENT_DATE + stop_time)
    """)

    # =========================
    # HISTORY TABLE
    # =========================
    op.execute("""
        ALTER TABLE dg_250kva_entry_history
        ALTER COLUMN start_time TYPE TIMESTAMP
        USING (CURRENT_DATE + start_time)
    """)

    op.execute("""
        ALTER TABLE dg_250kva_entry_history
        ALTER COLUMN stop_time TYPE TIMESTAMP
        USING (CURRENT_DATE + stop_time)
    """)


def downgrade():
    # revert back if needed
    op.execute("""
        ALTER TABLE dg_250kva_entry
        ALTER COLUMN start_time TYPE TIME
        USING start_time::time
    """)

    op.execute("""
        ALTER TABLE dg_250kva_entry
        ALTER COLUMN stop_time TYPE TIME
        USING stop_time::time
    """)

    op.execute("""
        ALTER TABLE dg_250kva_entry_history
        ALTER COLUMN start_time TYPE TIME
        USING start_time::time
    """)

    op.execute("""
        ALTER TABLE dg_250kva_entry_history
        ALTER COLUMN stop_time TYPE TIME
        USING stop_time::time
    """)
