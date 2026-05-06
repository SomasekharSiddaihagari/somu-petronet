"""add owned_by to asset_claim_submission tables

Revision ID: f4e60d584385
Revises: 77f1a6786c44
Create Date: 2025-12-31 11:11:33.008056

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f4e60d584385'
down_revision: Union[str, Sequence[str], None] = '77f1a6786c44'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # ---- MAIN TABLE ----
    op.add_column(
        "asset_claim_submission",
        sa.Column("owned_by", sa.Text(), nullable=True)
    )

    # ---- HISTORY TABLE ----
    op.add_column(
        "asset_claim_submission_history",
        sa.Column("owned_by", sa.Text(), nullable=True)
    )


def downgrade():
    # ---- HISTORY TABLE ----
    op.drop_column(
        "asset_claim_submission_history",
        "owned_by"
    )

    # ---- MAIN TABLE ----
    op.drop_column(
        "asset_claim_submission",
        "owned_by"
    )
