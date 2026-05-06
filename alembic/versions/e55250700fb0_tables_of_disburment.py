"""tables of disburment

Revision ID: e55250700fb0
Revises: 1b8a9985d3a1
Create Date: 2025-12-26 16:04:13.935177

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e55250700fb0'
down_revision: Union[str, Sequence[str], None] = '1b8a9985d3a1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table(
        "asset_claim_disbursement",
        sa.Column("asset_claim_disbursement_id", sa.BigInteger(), primary_key=True),
 
        sa.Column("asset_claim_submission_id", sa.BigInteger(), nullable=True),
 
        sa.Column("claim_amount", sa.Numeric(12, 2), nullable=True),
        sa.Column("disbursed_amount", sa.Numeric(12, 2), nullable=True),
        sa.Column("payment_mode", sa.String(50), nullable=True),
        sa.Column("disbursement_date", sa.Date(), nullable=True),
 
        sa.Column("transaction_reference_no", sa.String(100), nullable=True),
 
        sa.Column("bank_name", sa.String(150), nullable=True),
        sa.Column("account_number", sa.String(50), nullable=True),
 
        sa.Column("remarks", sa.Text(), nullable=True),
 
        sa.Column("status", sa.String(30), nullable=True),
 
        sa.Column("created_by", sa.Integer(), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now()
        ),
        sa.Column("updated_by", sa.Integer(), nullable=True),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
    )
 
    op.create_table(
        "asset_claim_disbursement_history",
        sa.Column(
            "asset_claim_disbursement_history_id",
            sa.BigInteger(),
            primary_key=True
        ),
 
        sa.Column("asset_claim_disbursement_id", sa.BigInteger(), nullable=True),
        sa.Column("asset_claim_submission_id", sa.BigInteger(), nullable=True),
 
        sa.Column("claim_amount", sa.Numeric(12, 2), nullable=True),
        sa.Column("disbursed_amount", sa.Numeric(12, 2), nullable=True),
        sa.Column("payment_mode", sa.String(50), nullable=True),
        sa.Column("disbursement_date", sa.Date(), nullable=True),
 
        sa.Column("transaction_reference_no", sa.String(100), nullable=True),
 
        sa.Column("bank_name", sa.String(150), nullable=True),
        sa.Column("account_number", sa.String(50), nullable=True),
 
        sa.Column("remarks", sa.Text(), nullable=True),
 
        sa.Column("status", sa.String(30), nullable=True),
 
        sa.Column(
            "created_by", sa.Integer(), nullable=True
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now()
        ),
        sa.Column("updated_by", sa.Integer(), nullable=True),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
    )
 
 
def downgrade():
    op.drop_table("asset_claim_disbursement_history")
    op.drop_table("asset_claim_disbursement")