"""history dates

Revision ID: 18bd9f32f21c
Revises: bb7dc0631438
Create Date: 2025-12-11 17:52:07.664793

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '18bd9f32f21c'
down_revision: Union[str, Sequence[str], None] = 'bb7dc0631438'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def column_exists(table, column):
    conn = op.get_bind()
    result = conn.execute(
        sa.text("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name = :table
              AND column_name = :column
        """), {"table": table, "column": column}
    )
    return result.first() is not None


def upgrade():
    if not column_exists("daily_allowance_sheet_detail_history", "from_date"):
        op.add_column("daily_allowance_sheet_detail_history", sa.Column("from_date", sa.Date(), nullable=True))

    if not column_exists("daily_allowance_sheet_detail_history", "from_location"):
        op.add_column("daily_allowance_sheet_detail_history", sa.Column("from_location", sa.String(255), nullable=True))

    if not column_exists("daily_allowance_sheet_detail_history", "to_location"):
        op.add_column("daily_allowance_sheet_detail_history", sa.Column("to_location", sa.String(255), nullable=True))

    if not column_exists("daily_allowance_sheet_detail_history", "from_date_time"):
        op.add_column("daily_allowance_sheet_detail_history", sa.Column("from_date_time", sa.DateTime(timezone=True), nullable=True))

    if not column_exists("daily_allowance_sheet_detail_history", "to_date_time"):
        op.add_column("daily_allowance_sheet_detail_history", sa.Column("to_date_time", sa.DateTime(timezone=True), nullable=True))

    if not column_exists("daily_allowance_sheet_detail_history", "created_at"):
        op.add_column("daily_allowance_sheet_detail_history", sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text('now()')))

def downgrade():
    op.drop_column('daily_allowance_sheet_detail_history', 'created_at')
    op.drop_column('daily_allowance_sheet_detail_history', 'to_date_time')
    op.drop_column('daily_allowance_sheet_detail_history', 'from_date_time')
    op.drop_column('daily_allowance_sheet_detail_history', 'to_location')
    op.drop_column('daily_allowance_sheet_detail_history', 'from_location')
    op.drop_column('daily_allowance_sheet_detail_history', 'from_date')