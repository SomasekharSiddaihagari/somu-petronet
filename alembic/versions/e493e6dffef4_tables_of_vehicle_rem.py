"""tables of vehicle rem

Revision ID: e493e6dffef4
Revises: e9a10d343c4f
Create Date: 2025-12-29 15:55:32.127201

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e493e6dffef4'
down_revision: Union[str, Sequence[str], None] = 'e9a10d343c4f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # ---------------- MAIN TABLE ----------------
    op.create_table(
        "vehicle_cm_reimbursement",
        sa.Column("vehicle_cm_reimbursement_id", sa.BigInteger(), primary_key=True),
 
        sa.Column(
            "ra_claim_id",
            sa.BigInteger(),
            sa.ForeignKey("ra_claim.ra_claim_id", ondelete="CASCADE"),
            nullable=False
        ),
 
        sa.Column("vehicle_name", sa.String(150), nullable=True),
        sa.Column("claim_month_year", sa.String(20), nullable=True),
 
        sa.Column("vehicle_no", sa.String(50), nullable=True),
        sa.Column("vehicle_type", sa.String(50), nullable=True),
        sa.Column("fuel_type", sa.String(50), nullable=True),
 
        sa.Column("rc_expiry_date", sa.Date(), nullable=True),
        sa.Column("insurance_expiry_date", sa.Date(), nullable=True),
 
        sa.Column("fuel_claim_amount", sa.Numeric(12, 2), nullable=True),
        sa.Column("applicable_fuel_rate", sa.Numeric(10, 2), nullable=True),
        sa.Column("fuel_claimed_liters", sa.Numeric(10, 2), nullable=True),
 
        sa.Column("maintenance_claim_amount", sa.Numeric(12, 2), nullable=True),
        sa.Column("fixed_conveyance_claim", sa.Boolean(), nullable=True),
 
        sa.Column("annual_entitlement_fuel", sa.Numeric(12, 2), nullable=True),
        sa.Column("annual_entitlement_maintenance", sa.Numeric(12, 2), nullable=True),
 
        sa.Column("monthly_ceiling_fuel", sa.Numeric(12, 2), nullable=True),
        sa.Column("monthly_ceiling_maintenance", sa.Numeric(12, 2), nullable=True),
 
        sa.Column("adjustment_previous_month_fuel", sa.Numeric(12, 2), nullable=True),
        sa.Column("adjustment_previous_month_maintenance", sa.Numeric(12, 2), nullable=True),
 
        sa.Column("net_available_balance_fuel", sa.Numeric(12, 2), nullable=True),
        sa.Column("net_available_balance_maintenance", sa.Numeric(12, 2), nullable=True),
 
        sa.Column("max_claim_allowed_fuel", sa.Numeric(12, 2), nullable=True),
        sa.Column("max_claim_allowed_maintenance", sa.Numeric(12, 2), nullable=True),
 
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
        "vehicle_cm_reimbursement_history",
        sa.Column("vehicle_cm_reimbursement_history_id", sa.BigInteger(), primary_key=True),
 
        sa.Column("vehicle_cm_reimbursement_id", sa.BigInteger(), nullable=True),
        sa.Column("ra_claim_id", sa.BigInteger(), nullable=True),
 
        sa.Column("vehicle_name", sa.String(150), nullable=True),
        sa.Column("claim_month_year", sa.String(20), nullable=True),
 
        sa.Column("vehicle_no", sa.String(50), nullable=True),
        sa.Column("vehicle_type", sa.String(50), nullable=True),
        sa.Column("fuel_type", sa.String(50), nullable=True),
 
        sa.Column("rc_expiry_date", sa.Date(), nullable=True),
        sa.Column("insurance_expiry_date", sa.Date(), nullable=True),
 
        sa.Column("fuel_claim_amount", sa.Numeric(12, 2), nullable=True),
        sa.Column("applicable_fuel_rate", sa.Numeric(10, 2), nullable=True),
        sa.Column("fuel_claimed_liters", sa.Numeric(10, 2), nullable=True),
 
        sa.Column("maintenance_claim_amount", sa.Numeric(12, 2), nullable=True),
        sa.Column("fixed_conveyance_claim", sa.Boolean(), nullable=True),
 
        sa.Column("annual_entitlement_fuel", sa.Numeric(12, 2), nullable=True),
        sa.Column("annual_entitlement_maintenance", sa.Numeric(12, 2), nullable=True),
 
        sa.Column("monthly_ceiling_fuel", sa.Numeric(12, 2), nullable=True),
        sa.Column("monthly_ceiling_maintenance", sa.Numeric(12, 2), nullable=True),
 
        sa.Column("adjustment_previous_month_fuel", sa.Numeric(12, 2), nullable=True),
        sa.Column("adjustment_previous_month_maintenance", sa.Numeric(12, 2), nullable=True),
 
        sa.Column("net_available_balance_fuel", sa.Numeric(12, 2), nullable=True),
        sa.Column("net_available_balance_maintenance", sa.Numeric(12, 2), nullable=True),
 
        sa.Column("max_claim_allowed_fuel", sa.Numeric(12, 2), nullable=True),
        sa.Column("max_claim_allowed_maintenance", sa.Numeric(12, 2), nullable=True),
 
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
    op.drop_table("vehicle_cm_reimbursement_history")
    op.drop_table("vehicle_cm_reimbursement")