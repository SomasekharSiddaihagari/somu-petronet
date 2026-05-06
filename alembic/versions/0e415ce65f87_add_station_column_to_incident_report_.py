"""add station column to incident report tables

Revision ID: 0e415ce65f87
Revises: 4d4ca7e4f34e
Create Date: 2026-02-04 11:33:45.917427
"""

from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '0e415ce65f87'
down_revision: Union[str, Sequence[str], None] = '4d4ca7e4f34e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column(
        "incident_report",
        sa.Column("station", sa.Integer(), nullable=True)
    )

    op.add_column(
        "incident_report_history",
        sa.Column("station", sa.Integer(), nullable=True)
    )


def downgrade():
    op.drop_column("incident_report_history", "station")
    op.drop_column("incident_report", "station")
