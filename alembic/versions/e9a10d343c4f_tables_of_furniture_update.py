"""tables of furniture update

Revision ID: e9a10d343c4f
Revises: 9360f58e10ee
Create Date: 2025-12-29 15:24:11.827250

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e9a10d343c4f'
down_revision: Union[str, Sequence[str], None] = '9360f58e10ee'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade():
    # ---------------- MAIN TABLE ----------------
    op.create_table(
        "furniture_rm_reimbursement",
        sa.Column("furniture_rm_reimbursement_id", sa.BigInteger(), primary_key=True),
 
        sa.Column(
            "ra_claim_id",
            sa.BigInteger(),
            sa.ForeignKey("ra_claim.ra_claim_id", ondelete="CASCADE"),
            nullable=False
        ),
 
        sa.Column("furniture_name", sa.String(150), nullable=True),
        sa.Column("claim_month_year", sa.String(20), nullable=True),
 
        sa.Column("total_cost_under_policy", sa.Numeric(12, 2), nullable=True),
        sa.Column("expenditure_claimed", sa.Numeric(12, 2), nullable=True),
        sa.Column("maximum_eligible_amount", sa.Numeric(12, 2), nullable=True),
        sa.Column("amount_claimed", sa.Numeric(12, 2), nullable=True),
        sa.Column("eligible_amount", sa.Numeric(12, 2), nullable=True),
 
        sa.Column("document_names", sa.Text(), nullable=True),
        sa.Column("remarks", sa.Text(), nullable=True),
 
        sa.Column("declaration_accepted", sa.Boolean(), nullable=True),
        sa.Column("status", sa.String(30), nullable=True),
 
        # Supervisor
        sa.Column("updated_by_supervisor", sa.Date(), nullable=True),
        sa.Column("updated_by_supervisor_name", sa.String(150), nullable=True),
        sa.Column("supervisor_comment", sa.Text(), nullable=True),
 
        # HR
        sa.Column("updated_by_hr", sa.Date(), nullable=True),
        sa.Column("updated_by_hr_name", sa.String(150), nullable=True),
        sa.Column("hr_comment", sa.Text(), nullable=True),
 
        # Finance
        sa.Column("updated_by_finance", sa.Date(), nullable=True),
        sa.Column("updated_by_finance_name", sa.String(150), nullable=True),
        sa.Column("finance_comment", sa.Text(), nullable=True),
 
        sa.Column("created_by", sa.Integer(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_by", sa.Integer(), nullable=True),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
    )
 
    # ---------------- HISTORY TABLE ----------------
    op.create_table(
        "furniture_rm_reimbursement_history",
        sa.Column("furniture_rm_reimbursement_history_id", sa.BigInteger(), primary_key=True),
 
        sa.Column("furniture_rm_reimbursement_id", sa.BigInteger(), nullable=True),
        sa.Column("ra_claim_id", sa.BigInteger(), nullable=True),
 
        sa.Column("furniture_name", sa.String(150), nullable=True),
        sa.Column("claim_month_year", sa.String(20), nullable=True),
 
        sa.Column("total_cost_under_policy", sa.Numeric(12, 2), nullable=True),
        sa.Column("expenditure_claimed", sa.Numeric(12, 2), nullable=True),
        sa.Column("maximum_eligible_amount", sa.Numeric(12, 2), nullable=True),
        sa.Column("amount_claimed", sa.Numeric(12, 2), nullable=True),
        sa.Column("eligible_amount", sa.Numeric(12, 2), nullable=True),
 
        sa.Column("document_names", sa.Text(), nullable=True),
        sa.Column("remarks", sa.Text(), nullable=True),
 
        sa.Column("declaration_accepted", sa.Boolean(), nullable=True),
        sa.Column("status", sa.String(30), nullable=True),
 
        # Supervisor
        sa.Column("updated_by_supervisor", sa.Date(), nullable=True),
        sa.Column("updated_by_supervisor_name", sa.String(150), nullable=True),
        sa.Column("supervisor_comment", sa.Text(), nullable=True),
 
        # HR
        sa.Column("updated_by_hr", sa.Date(), nullable=True),
        sa.Column("updated_by_hr_name", sa.String(150), nullable=True),
        sa.Column("hr_comment", sa.Text(), nullable=True),
 
        # Finance
        sa.Column("updated_by_finance", sa.Date(), nullable=True),
        sa.Column("updated_by_finance_name", sa.String(150), nullable=True),
        sa.Column("finance_comment", sa.Text(), nullable=True),
 
        sa.Column("created_by", sa.Integer(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
 
 
def downgrade():
    op.drop_table("furniture_rm_reimbursement_history")
    op.drop_table("furniture_rm_reimbursement")