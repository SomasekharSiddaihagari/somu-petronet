"""tables of claim

Revision ID: 8ff97cdafad6
Revises: 1e1034434ed6
Create Date: 2025-12-26 15:04:17.317489

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8ff97cdafad6'
down_revision: Union[str, Sequence[str], None] = '1e1034434ed6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table(
        "asset_claim",
        sa.Column("asset_claim_id", sa.BigInteger(), primary_key=True),
 
        sa.Column("employee_name", sa.String(150), nullable=True),
        sa.Column("employee_id", sa.String(50), nullable=True),
        sa.Column("department", sa.String(100), nullable=True),
        sa.Column("designation", sa.String(100), nullable=True),
        sa.Column("station", sa.String(100), nullable=True),
        sa.Column("grade", sa.String(50), nullable=True),
 
        sa.Column("claim_module", sa.String(50), nullable=True),
        sa.Column("category", sa.String(100), nullable=True),
        sa.Column("sub_category", sa.String(150), nullable=True),
        sa.Column("item_type", sa.String(100), nullable=True),
 
        sa.Column("total_entitlement_limit", sa.Numeric(12, 2), nullable=True),
        sa.Column("amount_utilized", sa.Numeric(12, 2), nullable=True),
        sa.Column("balance_available", sa.Numeric(12, 2), nullable=True),
 
        sa.Column("status", sa.String(30), nullable=True),
        sa.Column("remarks", sa.Text(), nullable=True),
 
        sa.Column("created_by", sa.Integer(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_by", sa.Integer(), nullable=True),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True)
    )
 
    op.create_table(
        "asset_claim_history",
        sa.Column("asset_claim_history_id", sa.BigInteger(), primary_key=True),
        sa.Column("asset_claim_id", sa.BigInteger(), nullable=True),
 
        sa.Column("employee_name", sa.String(150), nullable=True),
        sa.Column("employee_id", sa.String(50), nullable=True),
        sa.Column("department", sa.String(100), nullable=True),
        sa.Column("designation", sa.String(100), nullable=True),
        sa.Column("station", sa.String(100), nullable=True),
        sa.Column("grade", sa.String(50), nullable=True),
 
        sa.Column("claim_module", sa.String(50), nullable=True),
        sa.Column("category", sa.String(100), nullable=True),
        sa.Column("sub_category", sa.String(150), nullable=True),
        sa.Column("item_type", sa.String(100), nullable=True),
 
        sa.Column("total_entitlement_limit", sa.Numeric(12, 2), nullable=True),
        sa.Column("amount_utilized", sa.Numeric(12, 2), nullable=True),
        sa.Column("balance_available", sa.Numeric(12, 2), nullable=True),
 
        sa.Column("status", sa.String(30), nullable=True),
        sa.Column("remarks", sa.Text(), nullable=True),
 
        sa.Column("created_by", sa.Integer(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_by", sa.Integer(), nullable=True),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True)
    )
 
 
def downgrade():
    op.drop_table("asset_claim_history")
    op.drop_table("asset_claim")