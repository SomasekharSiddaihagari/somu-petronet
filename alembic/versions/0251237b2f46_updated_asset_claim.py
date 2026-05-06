"""updated asset claim

Revision ID: 0251237b2f46
Revises: e8eb91af28e3
Create Date: 2026-01-02 18:49:35.193975

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0251237b2f46'
down_revision: Union[str, Sequence[str], None] = 'e8eb91af28e3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # asset_claim
    op.add_column(
        "asset_claim",
        sa.Column("buy_back_submitted_date", sa.Date(), nullable=True)
    )

    # asset_claim_history
    op.add_column(
        "asset_claim_history",
        sa.Column("buy_back_submitted_date", sa.Date(), nullable=True)
    )


def downgrade():
    # asset_claim_history
    op.drop_column("asset_claim_history", "buy_back_submitted_date")

    # asset_claim
    op.drop_column("asset_claim", "buy_back_submitted_date")
