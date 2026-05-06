"""add employee_vendor_code to users and users_history

Revision ID: 5f37516b02a2
Revises: 167a8cc511f7
Create Date: 2026-01-16 16:11:57.171598

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5f37516b02a2'
down_revision: Union[str, Sequence[str], None] = '167a8cc511f7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column(
        "users",
        sa.Column("employee_vendor_code", sa.String(length=255), nullable=True)
    )

    op.add_column(
        "users_history",
        sa.Column("employee_vendor_code", sa.String(length=255), nullable=True)
    )


def downgrade():
    op.drop_column("users", "employee_vendor_code")
    op.drop_column("users_history", "employee_vendor_code")