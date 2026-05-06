"""add created_by and updated_by to capa_report

Revision ID: 4d4ca7e4f34e
Revises: 452914b7eb61
Create Date: 2026-02-03 18:30:29.615532

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4d4ca7e4f34e'
down_revision: Union[str, Sequence[str], None] = '452914b7eb61'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade():

    # Add columns to capa_report
    op.add_column(
        "capa_report",
        sa.Column("created_by", sa.Integer(), nullable=True)
    )
    op.add_column(
        "capa_report",
        sa.Column("updated_by", sa.Integer(), nullable=True)
    )

    # Add columns to capa_report_history
    op.add_column(
        "capa_report_history",
        sa.Column("created_by", sa.Integer(), nullable=True)
    )
    op.add_column(
        "capa_report_history",
        sa.Column("updated_by", sa.Integer(), nullable=True)
    )

def downgrade():

    op.drop_column("capa_report", "updated_by")
    op.drop_column("capa_report", "created_by")

    op.drop_column("capa_report_history", "updated_by")
    op.drop_column("capa_report_history", "created_by")