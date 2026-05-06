"""add technician_id and ms_logbook_id to multiple tables

Revision ID: 0a286c4c2194
Revises: 7614c431e5b6
Create Date: 2026-03-23 18:14:32.261370

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0a286c4c2194'
down_revision: Union[str, Sequence[str], None] = '7614c431e5b6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # 🔹 Add mas_logbook_id (Integer)
    op.add_column(
        "fire_engine_test_master",
        sa.Column("mas_logbook_id", sa.Integer(), nullable=True)
    )

    op.add_column(
        "fire_engine_test_master_history",
        sa.Column("mas_logbook_id", sa.Integer(), nullable=True)
    )

    # 🔹 Add before_after_mrpl_qty (JSON)
    op.add_column(
        "tank_dip_memo",
        sa.Column("before_after_mrpl_qty", sa.JSON(), nullable=True)
    )

    op.add_column(
        "tank_dip_memo_history",
        sa.Column("before_after_mrpl_qty", sa.JSON(), nullable=True)
    )


def downgrade():
    # 🔻 Remove JSON columns
    op.drop_column("tank_dip_memo", "before_after_mrpl_qty")
    op.drop_column("tank_dip_memo_history", "before_after_mrpl_qty")

    # 🔻 Remove Integer columns
    op.drop_column("fire_engine_test_master", "mas_logbook_id")
    op.drop_column("fire_engine_test_master_history", "mas_logbook_id")