"""add status to hse incident investigation master

Revision ID: 20086854bac1
Revises: 743e3208a1bd
Create Date: 2026-02-18 12:04:04.069168

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '20086854bac1'
down_revision: Union[str, Sequence[str], None] = '743e3208a1bd'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column(
        "hse_incident_investigation_master",
        sa.Column("status", sa.String(length=50), nullable=True)
    )

    op.add_column(
        "hse_incident_investigation_master_history",
        sa.Column("status", sa.String(length=50), nullable=True)
    )


def downgrade():
    op.drop_column("hse_incident_investigation_master", "status")
    op.drop_column("hse_incident_investigation_master_history", "status")