"""add approved_at to outward_gate_pass tables

Revision ID: 5251412999cd
Revises: d4972cdc6757
Create Date: 2026-03-16 17:39:33.469557

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy import inspect


# revision identifiers, used by Alembic.
revision: str = '5251412999cd'
down_revision: Union[str, Sequence[str], None] = 'd4972cdc6757'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():

    tables = [
        "outward_gate_pass",
        "outward_gate_pass_history"
    ]

    conn = op.get_bind()
    inspector = inspect(conn)

    for table in tables:

        columns = [col["name"] for col in inspector.get_columns(table)]

        if "approved_at" not in columns:
            op.add_column(
                table,
                sa.Column("approved_at", sa.Date(), nullable=True)
            )


def downgrade():

    tables = [
        "outward_gate_pass",
        "outward_gate_pass_history"
    ]

    conn = op.get_bind()
    inspector = inspect(conn)

    for table in tables:

        columns = [col["name"] for col in inspector.get_columns(table)]

        if "approved_at" in columns:
            op.drop_column(table, "approved_at")
