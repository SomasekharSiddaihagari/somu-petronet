"""add sap_assets_no to asset claim disbursement tables

Revision ID: f354accf3411
Revises: 908b2e232afb
Create Date: 2026-02-13 22:48:42.851392

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f354accf3411'
down_revision: Union[str, Sequence[str], None] = '908b2e232afb'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column(
        "asset_claim_disbursement",
        sa.Column("sap_assets_no", sa.BigInteger(), nullable=True)
    )

    op.add_column(
        "asset_claim_disbursement_history",
        sa.Column("sap_assets_no", sa.BigInteger(), nullable=True)
    )


def downgrade():
    op.drop_column("asset_claim_disbursement", "sap_assets_no")
    op.drop_column("asset_claim_disbursement_history", "sap_assets_no")