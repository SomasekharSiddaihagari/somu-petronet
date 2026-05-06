"""add technician_id in master tables

Revision ID: e35932ba25fc
Revises: 87be6686f6e1
Create Date: 2026-03-13 11:39:07.780069

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e35932ba25fc'
down_revision: Union[str, Sequence[str], None] = '87be6686f6e1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


tables = [
    "kptcl_dkn_master",
    "kptcl_dkn_master_history",
    "kptcl_hsn_master",
    "kptcl_hsn_master_history",
    "kptcl_ner_master",
    "kptcl_ner_master_history",
    "daily_sampling_master",
    "daily_sampling_master_history",
]


def upgrade():
    for table in tables:

        op.add_column(table, sa.Column("technician_id", sa.Integer(), nullable=True))


def downgrade():
    for table in tables:
        op.drop_column(table, "technician_id")

