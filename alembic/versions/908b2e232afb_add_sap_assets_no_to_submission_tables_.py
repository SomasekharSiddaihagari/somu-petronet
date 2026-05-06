"""add sap_assets_no to submission tables and remove from claim tables

Revision ID: 908b2e232afb
Revises: 67f51fdc4b02
Create Date: 2026-02-13 21:58:16.494788

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '908b2e232afb'
down_revision: Union[str, Sequence[str], None] = '67f51fdc4b02'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():

    # -----------------------------

    # ADD sap_assets_no (BIGINT)

    # -----------------------------

    op.add_column(

        "asset_claim_submission",

        sa.Column("sap_assets_no", sa.BigInteger(), nullable=True)

    )
 
    op.add_column(

        "asset_claim_submission_history",

        sa.Column("sap_assets_no", sa.BigInteger(), nullable=True)

    )
 
    # -----------------------------

    # REMOVE sap_assets_no (INT)

    # -----------------------------

    op.drop_column("asset_claim", "sap_assets_no")

    op.drop_column("asset_claim_history", "sap_assets_no")
 
 
def downgrade():

    # -----------------------------

    # ADD BACK sap_assets_no (INT)

    # -----------------------------

    op.add_column(

        "asset_claim",

        sa.Column("sap_assets_no", sa.Integer(), nullable=True)

    )
 
    op.add_column(

        "asset_claim_history",

        sa.Column("sap_assets_no", sa.Integer(), nullable=True)

    )
 
    # -----------------------------

    # REMOVE BIGINT FROM SUBMISSION

    # -----------------------------

    op.drop_column("asset_claim_submission", "sap_assets_no")

    op.drop_column("asset_claim_submission_history", "sap_assets_no")
 