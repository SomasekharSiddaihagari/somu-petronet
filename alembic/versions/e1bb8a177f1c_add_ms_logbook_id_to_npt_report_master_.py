"""add ms_logbook_id to npt_report_master tables

Revision ID: e1bb8a177f1c
Revises: 185dc6747f09
Create Date: 2026-03-11 11:25:36.056194

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e1bb8a177f1c'
down_revision: Union[str, Sequence[str], None] = '185dc6747f09'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():

    tables = [
        "npt_report_master",
        "npt_report_master_history"
    ]

    for table in tables:
        op.add_column(
            table,
            sa.Column(
                "ms_logbook_id",
                sa.Integer(),
                nullable=True
            )
        )


def downgrade():

    tables = [
        "npt_report_master",
        "npt_report_master_history"
    ]

    for table in tables:
        op.drop_column(
            table,
            "ms_logbook_id"
        )
