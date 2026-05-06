"""add brought_back_date to asset_claim tables

Revision ID: 1c77bd4e3b1e
Revises: 895ec1834212
Create Date: 2026-01-12 14:47:15.584016

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1c77bd4e3b1e'
down_revision: Union[str, Sequence[str], None] = '895ec1834212'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column(
        "asset_claim",
        sa.Column("brought_back_date", sa.Date(), nullable=True)
    )
    op.add_column(
        "asset_claim_history",
        sa.Column("brought_back_date", sa.Date(), nullable=True)
    )


def downgrade():
    op.drop_column("asset_claim_history", "brought_back_date")
    op.drop_column("asset_claim", "brought_back_date")