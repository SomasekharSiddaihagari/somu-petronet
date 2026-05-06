"""add ms_logbook_id and technician_id to dg_250kva tables

Revision ID: d4972cdc6757
Revises: 6a24c8c68675
Create Date: 2026-03-16 12:10:57.394850

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy import inspect


# revision identifiers, used by Alembic.
revision: str = 'd4972cdc6757'
down_revision: Union[str, Sequence[str], None] = '6a24c8c68675'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():

    tables = [
        "dg_250kva_master",
        "dg_250kva_master_history"
    ]

    columns_to_add = [
        ("ms_logbook_id", sa.Integer()),
        ("technician_id", sa.Integer())
    ]

    conn = op.get_bind()
    inspector = inspect(conn)

    for table in tables:
        existing_columns = [col["name"] for col in inspector.get_columns(table)]

        for column_name, column_type in columns_to_add:
            if column_name not in existing_columns:
                op.add_column(
                    table,
                    sa.Column(column_name, column_type, nullable=True)
                )


def downgrade():

    tables = [
        "dg_250kva_master",
        "dg_250kva_master_history"
    ]

    columns = [
        "ms_logbook_id",
        "technician_id"
    ]

    conn = op.get_bind()
    inspector = inspect(conn)

    for table in tables:
        existing_columns = [col["name"] for col in inspector.get_columns(table)]

        for column in columns:
            if column in existing_columns:
                op.drop_column(table, column)
