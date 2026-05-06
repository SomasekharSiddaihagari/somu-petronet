"""add technician and engineer fields to vibration temperature master tables

Revision ID: abed2f413369
Revises: 31c857809447
Create Date: 2026-03-12 11:26:38.058171

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'abed2f413369'
down_revision: Union[str, Sequence[str], None] = '31c857809447'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():

    tables = [
        "vibration_temperature_master_mlr",
        "vibration_temperature_master_mlr_history"
    ]

    for table in tables:
        op.add_column(table, sa.Column("shift_engineer_c_name", sa.String(length=100), nullable=True))
        op.add_column(table, sa.Column("shift_engineer_c_signature", sa.String(length=255), nullable=True))

        op.add_column(table, sa.Column("technician_a_name", sa.String(length=100), nullable=True))
        op.add_column(table, sa.Column("technician_a_id", sa.Integer(), nullable=True))

        op.add_column(table, sa.Column("technician_b_name", sa.String(length=100), nullable=True))
        op.add_column(table, sa.Column("technician_b_id", sa.Integer(), nullable=True))

        op.add_column(table, sa.Column("technician_c_id", sa.Integer(), nullable=True))


def downgrade():

    tables = [
        "vibration_temperature_master_mlr",
        "vibration_temperature_master_mlr_history"
    ]

    for table in tables:
        op.drop_column(table, "technician_c_id")
        op.drop_column(table, "technician_b_id")
        op.drop_column(table, "technician_b_name")
        op.drop_column(table, "technician_a_id")
        op.drop_column(table, "technician_a_name")
        op.drop_column(table, "shift_engineer_c_signature")
        op.drop_column(table, "shift_engineer_c_name")
