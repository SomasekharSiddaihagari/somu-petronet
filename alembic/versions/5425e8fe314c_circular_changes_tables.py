"""circular changes tables

Revision ID: 5425e8fe314c
Revises: 484c30bcc438
Create Date: 2026-02-26 12:54:23.793168

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5425e8fe314c'
down_revision: Union[str, Sequence[str], None] = '484c30bcc438'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():

    # ===============================
    # circular_master
    # ===============================

    # make subcategory_id nullable
    op.alter_column(
        "circular_master",
        "subcategory_id",
        existing_type=sa.Integer(),
        nullable=True
    )

    # add reason column
    op.add_column(
        "circular_master",
        sa.Column("reason", sa.Text(), nullable=True)
    )

    # ===============================
    # circular_master_history
    # ===============================


    op.add_column(
        "circular_master_history",
        sa.Column("reason", sa.Text(), nullable=True)
    )


def downgrade():

    # remove reason column
    op.drop_column("circular_master", "reason")
    op.drop_column("circular_master_history", "reason")

    # make subcategory_id NOT NULL again
    op.alter_column(
        "circular_master",
        "subcategory_id",
        existing_type=sa.Integer(),
        nullable=False
    )

