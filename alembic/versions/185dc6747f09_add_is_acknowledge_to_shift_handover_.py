"""add is_acknowledge to shift_handover_log tables

Revision ID: 185dc6747f09
Revises: dee00085b8ef
Create Date: 2026-03-10 15:35:41.445732

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '185dc6747f09'
down_revision: Union[str, Sequence[str], None] = 'dee00085b8ef'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():

    tables = [
        "shift_handover_log",
        "shift_handover_log_history"
    ]

    for table in tables:
        op.add_column(
            table,
            sa.Column(
                "is_acknowledge",
                sa.Boolean(),
                nullable=True
            )
        )


def downgrade():

    tables = [
        "shift_handover_log",
        "shift_handover_log_history"
    ]

    for table in tables:
        op.drop_column(
            table,
            "is_acknowledge"
        )
