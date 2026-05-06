"""add document_details and comment

Revision ID: 296d1349a83b
Revises: 33ab4e34cfd7
Create Date: 2026-02-16 21:28:07.219309

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '296d1349a83b'
down_revision: Union[str, Sequence[str], None] = '33ab4e34cfd7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

tables = [
    "users",
    "users_history",
    "employee_family",
    "employee_family_history",
    "user_vehicle",
    "user_vehicle_history",
    "employee_bank",
    "employee_bank_history",
]


def upgrade():
    for table in tables:
        op.add_column(table, sa.Column("document_details", sa.Text(), nullable=True))
        op.add_column(table, sa.Column("comment", sa.Text(), nullable=True))


def downgrade():
    for table in tables:
        op.drop_column(table, "document_details")
        op.drop_column(table, "comment")