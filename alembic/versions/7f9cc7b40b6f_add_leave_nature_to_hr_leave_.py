"""add leave_nature to hr leave application tables

Revision ID: 7f9cc7b40b6f
Revises: cbd6d3e3ff4c
Create Date: 2025-12-18 18:34:04.218238

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7f9cc7b40b6f'
down_revision: Union[str, Sequence[str], None] = 'cbd6d3e3ff4c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # ---- main table ----
    op.add_column(
        "hr_leave_application",
        sa.Column("leave_nature", sa.String(length=50), nullable=True)
    )

    # ---- history table ----
    op.add_column(
        "hr_leave_application_history",
        sa.Column("leave_nature", sa.String(length=50), nullable=True)
    )


def downgrade():
    # ---- history table ----
    op.drop_column("hr_leave_application_history", "leave_nature")

    # ---- main table ----
    op.drop_column("hr_leave_application", "leave_nature")