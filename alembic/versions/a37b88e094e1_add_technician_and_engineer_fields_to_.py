"""add technician and engineer fields to vibration_temperature_master_ner tables

Revision ID: a37b88e094e1
Revises: 516db58a3996
Create Date: 2026-03-12 12:07:22.656004

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a37b88e094e1'
down_revision: Union[str, Sequence[str], None] = '516db58a3996'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():

    tables = [
        "vibration_temperature_master_ner",
        "vibration_temperature_master_ner_history"
    ]

    for table in tables:
        op.add_column(
            table,
            sa.Column("shift_engineer_c_name", sa.String(length=100), nullable=True)
        )

        op.add_column(
            table,
            sa.Column("technician_a_id", sa.Integer(), nullable=True)
        )

        op.add_column(
            table,
            sa.Column("technician_b_id", sa.Integer(), nullable=True)
        )

        op.add_column(
            table,
            sa.Column("technician_c_id", sa.Integer(), nullable=True)
        )


def downgrade():

    tables = [
        "vibration_temperature_master_ner",
        "vibration_temperature_master_ner_history"
    ]

    for table in tables:
        op.drop_column(table, "technician_c_id")
        op.drop_column(table, "technician_b_id")
        op.drop_column(table, "technician_a_id")
        op.drop_column(table, "shift_engineer_c_name")
