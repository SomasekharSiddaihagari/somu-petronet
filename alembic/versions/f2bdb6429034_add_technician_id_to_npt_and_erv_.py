"""add technician_id to npt and erv logbook tables

Revision ID: f2bdb6429034
Revises: d3236d53962f
Create Date: 2026-03-16 11:52:04.094075

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy import inspect


# revision identifiers, used by Alembic.
revision: str = 'f2bdb6429034'
down_revision: Union[str, Sequence[str], None] = 'd3236d53962f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():

    tables = [
        "npt_report_master",
        "npt_report_master_history",
        "erv_logbook_master",
        "erv_logbook_master_history"
    ]

    conn = op.get_bind()
    inspector = inspect(conn)

    for table in tables:

        columns = [col["name"] for col in inspector.get_columns(table)]

        if "technician_id" not in columns:
            op.add_column(
                table,
                sa.Column("technician_id", sa.Integer(), nullable=True)
            )


def downgrade():

    tables = [
        "npt_report_master",
        "npt_report_master_history",
        "erv_logbook_master",
        "erv_logbook_master_history"
    ]

    conn = op.get_bind()
    inspector = inspect(conn)

    for table in tables:

        columns = [col["name"] for col in inspector.get_columns(table)]

        if "technician_id" in columns:
            op.drop_column(table, "technician_id")
