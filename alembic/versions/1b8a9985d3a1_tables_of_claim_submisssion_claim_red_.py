"""tables of claim submisssion claim_red_id comments

Revision ID: 1b8a9985d3a1
Revises: 3457143a1d86
Create Date: 2025-12-26 15:54:54.132191

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1b8a9985d3a1'
down_revision: Union[str, Sequence[str], None] = '3457143a1d86'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade():
    # ---- MAIN TABLE ----
    op.add_column(
        "asset_claim_submission",
        sa.Column("residual_value_percent", sa.Numeric(5, 2), nullable=True)
    )
    op.add_column(
        "asset_claim",
        sa.Column("residual_value_amount", sa.Numeric(12, 2), nullable=True)
    )
    op.add_column(
        "asset_claim",
        sa.Column("amount_to_be_disbursed", sa.Numeric(12, 2), nullable=True)
    )
    op.add_column(
        "asset_claim",
        sa.Column("hr_comment", sa.Text(), nullable=True)
    )
    op.add_column(
        "asset_claim",
        sa.Column("finance_comment", sa.Text(), nullable=True)
    )
    op.add_column(
        "asset_claim",
        sa.Column("supervisor_comment", sa.Text(), nullable=True)
    )
 
    # ---- HISTORY TABLE ----
    op.add_column(
        "asset_claim_submission_history",
        sa.Column("residual_value_percent", sa.Numeric(5, 2), nullable=True)
    )
    op.add_column(
        "asset_claim_history",
        sa.Column("residual_value_amount", sa.Numeric(12, 2), nullable=True)
    )
    op.add_column(
        "asset_claim_history",
        sa.Column("amount_to_be_disbursed", sa.Numeric(12, 2), nullable=True)
    )
    op.add_column(
        "asset_claim_history",
        sa.Column("hr_comment", sa.Text(), nullable=True)
    )
    op.add_column(
        "asset_claim_history",
        sa.Column("finance_comment", sa.Text(), nullable=True)
    )
    op.add_column(
        "asset_claim_history",
        sa.Column("supervisor_comment", sa.Text(), nullable=True)
    )
 
 
def downgrade():
    # ---- HISTORY TABLE ----
    op.drop_column("asset_claim_history", "finance_comment")
    op.drop_column("asset_claim_history", "hr_comment")
    op.drop_column("asset_claim_history", "amount_to_be_disbursed")
    op.drop_column("asset_claim_history", "residual_value_amount")
    op.drop_column("asset_claim_history", "residual_value_percent")
 
    # ---- MAIN TABLE ----
    op.drop_column("asset_claim", "finance_comment")
    op.drop_column("asset_claim", "hr_comment")
    op.drop_column("asset_claim", "amount_to_be_disbursed")
    op.drop_column("asset_claim", "residual_value_amount")
    op.drop_column("asset_claim", "residual_value_percent")