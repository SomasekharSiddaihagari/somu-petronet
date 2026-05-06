"""tables of user and assets

Revision ID: 8480797f7970
Revises: ecd5d2bf9f49
Create Date: 2025-12-30 13:13:59.049232

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8480797f7970'
down_revision: Union[str, Sequence[str], None] = 'ecd5d2bf9f49'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # -------- USERS --------
    op.add_column(
        "users",
        sa.Column("blood_group", sa.Text(), nullable=True)
    )
    op.add_column(
        "users_history",
        sa.Column("blood_group", sa.Text(), nullable=True)
    )

    # -------- ASSET CLAIM --------
    op.add_column(
        "asset_claim",
        sa.Column("claim_date", sa.Date(), nullable=True)
    )
    op.add_column(
        "asset_claim",
        sa.Column("bought_back", sa.Boolean(), nullable=True)
    )
    op.add_column(
        "asset_claim",
        sa.Column("buy_back_date", sa.Date(), nullable=True)
    )

    op.add_column(
        "asset_claim_history",
        sa.Column("claim_date", sa.Date(), nullable=True)
    )
    op.add_column(
        "asset_claim_history",
        sa.Column("bought_back", sa.Boolean(), nullable=True)
    )
    op.add_column(
        "asset_claim_history",
        sa.Column("buy_back_date", sa.Date(), nullable=True)
    )


def downgrade():
    # -------- ASSET CLAIM --------
    op.drop_column("asset_claim_history", "buy_back_date")
    op.drop_column("asset_claim_history", "bought_back")
    op.drop_column("asset_claim_history", "claim_date")

    op.drop_column("asset_claim", "buy_back_date")
    op.drop_column("asset_claim", "bought_back")
    op.drop_column("asset_claim", "claim_date")

    # -------- USERS --------
    op.drop_column("users_history", "blood_group")
    op.drop_column("users", "blood_group")