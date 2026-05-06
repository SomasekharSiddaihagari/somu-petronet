"""hse id

Revision ID: 6d846fa79e12
Revises: 25f958b0e274
Create Date: 2026-02-18 23:33:53.626004

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6d846fa79e12'
down_revision: Union[str, Sequence[str], None] = '25f958b0e274'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # ✅ add to capa_report
    op.add_column(
        "capa_report",
        sa.Column("hse_head_id", sa.Integer(), nullable=True)
    )
 
    # ✅ add to capa_report_history
    op.add_column(
        "capa_report_history",
        sa.Column("hse_head_id", sa.Integer(), nullable=True)
    )
 
 
def downgrade():
    # 🔻 remove from history
    op.drop_column("capa_report_history", "hse_head_id")
 
    # 🔻 remove from master
    op.drop_column("capa_report", "hse_head_id")