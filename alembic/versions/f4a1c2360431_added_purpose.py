"""added purpose

Revision ID: f4a1c2360431
Revises: 73e9dc8dd23e
Create Date: 2025-12-11 11:29:00.249038

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f4a1c2360431'
down_revision: Union[str, Sequence[str], None] = '73e9dc8dd23e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column(
        "daily_allowance_sheet",
        sa.Column("purpose", sa.String(length=255), nullable=True)
    )

    op.add_column(
        "daily_allowance_sheet_history",
        sa.Column("purpose", sa.String(length=255), nullable=True)
    )


def downgrade():
    op.drop_column("daily_allowance_sheet", "purpose")
    op.drop_column("daily_allowance_sheet_history", "purpose")