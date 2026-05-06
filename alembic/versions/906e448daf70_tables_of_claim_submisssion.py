"""tables of claim submisssion

Revision ID: 906e448daf70
Revises: 8ff97cdafad6
Create Date: 2025-12-26 15:10:20.702274

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '906e448daf70'
down_revision: Union[str, Sequence[str], None] = '8ff97cdafad6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table(
        "asset_claim_submission",
        sa.Column("asset_claim_submission_id", sa.BigInteger(), primary_key=True),
 
        sa.Column("asset_claim_id", sa.BigInteger(), nullable=True),
 
        sa.Column("item_type", sa.String(150), nullable=True),
        sa.Column("item_name", sa.String(150), nullable=True),
        sa.Column("claim_amount", sa.Numeric(12, 2), nullable=True),
 
        sa.Column("vendor_name", sa.String(150), nullable=True),
        sa.Column("vendor_gstin", sa.String(50), nullable=True),
        sa.Column("vendor_address", sa.Text(), nullable=True),
        sa.Column("vendor_contact_no", sa.String(50), nullable=True),
        sa.Column("invoice_date", sa.Date(), nullable=True),
        sa.Column("invoice_no", sa.String(100), nullable=True),
 
        sa.Column("document_names", sa.Text(), nullable=True),
 
        sa.Column("declaration_accepted", sa.Boolean(), nullable=True),
 
        sa.Column("status", sa.String(30), nullable=True),
 
        sa.Column("created_by", sa.Integer(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_by", sa.Integer(), nullable=True),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True)
    )
 
    op.create_table(
        "asset_claim_submission_history",
        sa.Column(
            "asset_claim_submission_history_id",
            sa.BigInteger(),
            primary_key=True
        ),
 
        sa.Column("asset_claim_submission_id", sa.BigInteger(), nullable=True),
        sa.Column("asset_claim_id", sa.BigInteger(), nullable=True),
 
        sa.Column("item_type", sa.String(150), nullable=True),
        sa.Column("item_name", sa.String(150), nullable=True),
        sa.Column("claim_amount", sa.Numeric(12, 2), nullable=True),
 
        sa.Column("vendor_name", sa.String(150), nullable=True),
        sa.Column("vendor_gstin", sa.String(50), nullable=True),
        sa.Column("vendor_address", sa.Text(), nullable=True),
        sa.Column("vendor_contact_no", sa.String(50), nullable=True),
        sa.Column("invoice_date", sa.Date(), nullable=True),
        sa.Column("invoice_no", sa.String(100), nullable=True),
 
        sa.Column("document_names", sa.Text(), nullable=True),
 
        sa.Column("declaration_accepted", sa.Boolean(), nullable=True),
 
        sa.Column("status", sa.String(30), nullable=True),
 
        sa.Column("created_by", sa.Integer(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_by", sa.Integer(), nullable=True),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True)
    )
 
 
def downgrade():
    op.drop_table("asset_claim_submission_history")
    op.drop_table("asset_claim_submission")