"""add ms_logbook_id to vibration temperature tables

Revision ID: 32e3327d9a75
Revises: c7e6bdfe4ade
Create Date: 2026-03-07 11:26:39.496015

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '32e3327d9a75'
down_revision: Union[str, Sequence[str], None] = 'c7e6bdfe4ade'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():

    tables = [
        "vibration_temperature_master_mlr",
        "vibration_temperature_master_ner"
    ]

    for table in tables:
        op.add_column(
            table,
            sa.Column("ms_logbook_id", sa.Integer(), nullable=True)
        )


def downgrade():

    tables = [
        "vibration_temperature_master_mlr",
        "vibration_temperature_master_ner"
    ]

    for table in tables:
        op.drop_column(table, "ms_logbook_id")
