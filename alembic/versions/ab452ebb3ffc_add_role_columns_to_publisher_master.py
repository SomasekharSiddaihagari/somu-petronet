"""add role columns to publisher_master

Revision ID: ab452ebb3ffc
Revises: d9def7668b89
Create Date: 2026-02-26 10:57:54.497949

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ab452ebb3ffc'
down_revision: Union[str, Sequence[str], None] = 'd9def7668b89'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade():

    # -------------------------------
    # publisher_master table
    # -------------------------------
    op.add_column(
        "publisher_master",
        sa.Column("role_id", sa.Integer(), nullable=True)
    )

    op.add_column(
        "publisher_master",
        sa.Column("role_name", sa.String(length=50), nullable=True)
    )

    # -------------------------------
    # publisher_master_history table
    # -------------------------------
    op.add_column(
        "publisher_master_history",
        sa.Column("role_id", sa.Integer(), nullable=True)
    )

    op.add_column(
        "publisher_master_history",
        sa.Column("role_name", sa.String(length=50), nullable=True)
    )


def downgrade():

    # -------------------------------
    # publisher_master_history
    # -------------------------------
    op.drop_column("publisher_master_history", "role_name")
    op.drop_column("publisher_master_history", "role_id")

    # -------------------------------
    # publisher_master
    # -------------------------------
    op.drop_column("publisher_master", "role_name")
    op.drop_column("publisher_master", "role_id")