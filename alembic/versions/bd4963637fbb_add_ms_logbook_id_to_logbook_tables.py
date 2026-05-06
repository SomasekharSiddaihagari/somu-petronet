"""add ms_logbook_id to logbook tables

Revision ID: bd4963637fbb
Revises: 86ce09d1d11d
Create Date: 2026-03-06 12:18:37.403890

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'bd4963637fbb'
down_revision: Union[str, Sequence[str], None] = '86ce09d1d11d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    tables = [
        "mfm_log_hsn2_master",
        "mfm_log_hsn2_master_history",
        "mfm_log_hsn_master",
        "mfm_log_hsn_master_history",
        "mfm_log_mlr_master",
        "mfm_log_mlr_master_history",
        "mfm_log_ner_master",
        "mfm_log_ner_master_history"
    ]

    for table in tables:
        op.add_column(
            table,
            sa.Column("ms_logbook_id", sa.Integer(), nullable=True)
        )


def downgrade():
    tables = [
        "mfm_log_hsn2_master",
        "mfm_log_hsn2_master_history",
        "mfm_log_hsn_master",
        "mfm_log_hsn_master_history",
        "mfm_log_mlr_master",
        "mfm_log_mlr_master_history",
        "mfm_log_ner_master",
        "mfm_log_ner_master_history"
    ]

    for table in tables:
        op.drop_column(table, "ms_logbook_id")
