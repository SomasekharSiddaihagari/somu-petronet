"""add problem_statement to hse_incident_rca_5why

Revision ID: 3b89f5a3f7fc
Revises: 1b0c64646d35
Create Date: 2026-02-07 17:06:56.476876

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3b89f5a3f7fc'
down_revision: Union[str, Sequence[str], None] = '1b0c64646d35'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column(
        "hse_incident_rca_5why",
        sa.Column("problem_statement", sa.Text(), nullable=True)
    )


def downgrade():
    op.drop_column("hse_incident_rca_5why", "problem_statement")