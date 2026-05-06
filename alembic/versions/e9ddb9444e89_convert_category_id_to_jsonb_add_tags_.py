"""convert category_id to jsonb, add tags jsonb, change version to jsonb

Revision ID: e9ddb9444e89
Revises: f354accf3411
"""

from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


revision: str = "e9ddb9444e89"
down_revision: Union[str, Sequence[str], None] = "f354accf3411"
branch_labels = None
depends_on = None


# ---------------------------------------------------------
# HELPER: check column type
# ---------------------------------------------------------
def column_is_jsonb(table, column):
    res = op.get_bind().execute(sa.text(f"""
        SELECT data_type
        FROM information_schema.columns
        WHERE table_name='{table}'
        AND column_name='{column}'
    """)).fetchone()
    if not res:
        return False
    return res[0] == "jsonb"


def upgrade():

    conn = op.get_bind()

    # =====================================================
    # 1. DROP FK SAFELY (if exists)
    # =====================================================
    conn.execute(sa.text("""
        DO $$
        BEGIN
            IF EXISTS (
                SELECT 1 FROM pg_constraint 
                WHERE conname='publisher_master_category_id_fkey'
            ) THEN
                ALTER TABLE publisher_master 
                DROP CONSTRAINT publisher_master_category_id_fkey;
            END IF;
        END$$;
    """))

    conn.execute(sa.text("""
        DO $$
        BEGIN
            IF EXISTS (
                SELECT 1 FROM pg_constraint 
                WHERE conname='publisher_master_history_category_id_fkey'
            ) THEN
                ALTER TABLE publisher_master_history 
                DROP CONSTRAINT publisher_master_history_category_id_fkey;
            END IF;
        END$$;
    """))

    # =====================================================
    # 2. category_id → JSONB (only if not already jsonb)
    # =====================================================
    if not column_is_jsonb("publisher_master", "category_id"):
        conn.execute(sa.text("""
            ALTER TABLE publisher_master
            ALTER COLUMN category_id TYPE jsonb
            USING to_jsonb(category_id);
        """))

    if not column_is_jsonb("publisher_master_history", "category_id"):
        conn.execute(sa.text("""
            ALTER TABLE publisher_master_history
            ALTER COLUMN category_id TYPE jsonb
            USING to_jsonb(category_id);
        """))

    # =====================================================
    # 3. ADD TAGS JSONB (if not exists)
    # =====================================================
    conn.execute(sa.text("""
        ALTER TABLE circular_master
        ADD COLUMN IF NOT EXISTS tags jsonb;
    """))

    conn.execute(sa.text("""
        ALTER TABLE circular_master_history
        ADD COLUMN IF NOT EXISTS tags jsonb;
    """))

    # =====================================================
    # 4. version → JSONB SAFE
    # =====================================================
    tables = [
        "circular_target_audience",
        "circular_target_audience_history",
        "circular_attachments",
        "circular_attachments_history",
    ]

    for t in tables:
        res = conn.execute(sa.text(f"""
            SELECT data_type 
            FROM information_schema.columns
            WHERE table_name='{t}' AND column_name='version'
        """)).fetchone()

        if res and res[0] != "jsonb":
            conn.execute(sa.text(f"""
                ALTER TABLE {t}
                ALTER COLUMN version TYPE jsonb
                USING to_jsonb(version);
            """))


def downgrade():
    # usually not required in prod CI/CD
    pass
