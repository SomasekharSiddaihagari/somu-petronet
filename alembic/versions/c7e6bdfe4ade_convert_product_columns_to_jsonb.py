"""convert product columns to jsonb

Revision ID: c7e6bdfe4ade
Revises: bd4963637fbb
Create Date: 2026-03-06 17:02:55.390039

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c7e6bdfe4ade'
down_revision: Union[str, Sequence[str], None] = 'bd4963637fbb'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():

    tables = [
        "mfm_log_master_dkn",
        "mfm_log_master_dkn_history"
    ]

    columns = [
        "euro_hsd",
        "bsv_hsd",
        "sk_o",
        "ms",
        "total_product"
    ]

    for table in tables:
        for column in columns:
            op.execute(f"""
                ALTER TABLE {table}
                ALTER COLUMN {column}
                TYPE jsonb
                USING to_jsonb({column})
            """)


def downgrade():

    tables = [
        "mfm_log_master_dkn",
        "mfm_log_master_dkn_history"
    ]

    columns = [
        "euro_hsd",
        "bsv_hsd",
        "sk_o",
        "ms",
        "total_product"
    ]

    for table in tables:
        for column in columns:
            op.execute(f"""
                ALTER TABLE {table}
                ALTER COLUMN {column}
                TYPE double precision
                USING ({column})::double precision
            """)
