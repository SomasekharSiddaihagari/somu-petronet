"""add ms_logbook_id to line_walker_master tables

Revision ID: 31c857809447
Revises: 550d0b68875f
Create Date: 2026-03-12 10:50:45.823512

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '31c857809447'
down_revision: Union[str, Sequence[str], None] = '550d0b68875f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():

    tables = [
        "line_walker_master",
        "line_walker_master_history"
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
        "line_walker_master",
        "line_walker_master_history"
    ]

    for table in tables:
        op.drop_column(
            table,
            "ms_logbook_id"
        )
