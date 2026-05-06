"""tables of claim submisssion claim_red_id

Revision ID: 3457143a1d86
Revises: 906e448daf70
Create Date: 2025-12-26 15:25:25.656178

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3457143a1d86'
down_revision: Union[str, Sequence[str], None] = '906e448daf70'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade():
    # Add to main table
    op.add_column(
        "asset_claim",
        sa.Column("claim_ref_id", sa.String(length=50), nullable=True)
    )
 
    # Add to history table
    op.add_column(
        "asset_claim_history",
        sa.Column("claim_ref_id", sa.String(length=50), nullable=True)
    )
 
 
def downgrade():
    op.drop_column("asset_claim_history", "claim_ref_id")
    op.drop_column("asset_claim", "claim_ref_id")