"""add sap_assets_no to asset_claim tables

Revision ID: 0277f082b522
Revises: 210fa10c89e4
Create Date: 2026-02-13 19:02:41.816902

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0277f082b522'
down_revision: Union[str, Sequence[str], None] = '210fa10c89e4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column(
        'asset_claim',
        sa.Column('sap_assets_no', sa.Integer(), nullable=True)
    )

    op.add_column(
        'asset_claim_history',
        sa.Column('sap_assets_no', sa.Integer(), nullable=True)
    )


def downgrade():
    op.drop_column('asset_claim', 'sap_assets_no')
    op.drop_column('asset_claim_history', 'sap_assets_no')