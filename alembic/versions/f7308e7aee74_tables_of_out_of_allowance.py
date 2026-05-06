"""tables of out of allowance

Revision ID: f7308e7aee74
Revises: 1dd8b71886b8
Create Date: 2025-12-29 18:02:22.020995

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f7308e7aee74'
down_revision: Union[str, Sequence[str], None] = '1dd8b71886b8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None



def upgrade():
    # ================= allowance_claim =================
    op.create_table(
        "allowance_claim",
        sa.Column("allowance_claim_id", sa.BigInteger(), primary_key=True),
 
        sa.Column(
            "ra_claim_id",
            sa.BigInteger(),
            sa.ForeignKey("ra_claim.ra_claim_id", ondelete="CASCADE"),
            nullable=False
        ),
 
        sa.Column("employee_name", sa.String(150)),
        sa.Column("employee_id", sa.String(50)),
        sa.Column("department", sa.String(100)),
        sa.Column("designation", sa.String(100)),
        sa.Column("station", sa.String(100)),
        sa.Column("grade", sa.String(50)),
 
        sa.Column("from_location", sa.String(100)),
        sa.Column("to_location", sa.String(100)),
        sa.Column("effective_transfer_date", sa.Date()),
        sa.Column("claim_date", sa.Date()),
 
        # Travel
        sa.Column("travel_from", sa.String(100)),
        sa.Column("travel_to", sa.String(100)),
        sa.Column("travel_mode", sa.String(50)),
        sa.Column("travel_date", sa.Date()),
        sa.Column("number_of_passengers", sa.Integer()),
        sa.Column("travel_amount", sa.Numeric(12, 2)),
        sa.Column("travel_remarks", sa.Text()),
        sa.Column("travel_documents", sa.Text()),
        sa.Column("include_travel", sa.Boolean()),
 
        # Displacement
        sa.Column("displacement_city", sa.String(100)),
        sa.Column("no_of_days_claimed", sa.Integer()),
        sa.Column("displacement_rate", sa.Numeric(10, 2)),
        sa.Column("displacement_amount", sa.Numeric(12, 2)),
        sa.Column("displacement_remarks", sa.Text()),
        sa.Column("displacement_documents", sa.Text()),
        sa.Column("include_displacement", sa.Boolean()),
 
        # Settling
        sa.Column("basic_pay_monthly", sa.Numeric(12, 2)),
        sa.Column("dearness_allowance_monthly", sa.Numeric(12, 2)),
        sa.Column("eligible_settling_amount", sa.Numeric(12, 2)),
        sa.Column("settling_remarks", sa.Text()),
        sa.Column("settling_documents", sa.Text()),
        sa.Column("include_settling", sa.Boolean()),
 
        # Household goods
        sa.Column("transport_mode", sa.String(50)),
        sa.Column("transport_distance_km", sa.Numeric(10, 2)),
        sa.Column("freight_amount", sa.Numeric(12, 2)),
        sa.Column("goods_transport_remarks", sa.Text()),
        sa.Column("goods_transport_documents", sa.Text()),
        sa.Column("include_goods_transport", sa.Boolean()),
 
        # Packaging
        sa.Column("amount_claimed_packaging", sa.Numeric(12, 2)),
        sa.Column("packaging_vendor", sa.String(150)),
        sa.Column("packaging_bill_no", sa.String(100)),
        sa.Column("packaging_remarks", sa.Text()),
        sa.Column("packaging_documents", sa.Text()),
        sa.Column("include_packaging", sa.Boolean()),
 
        # Insurance
        sa.Column("insurance_company", sa.String(150)),
        sa.Column("policy_no", sa.String(100)),
        sa.Column("insurance_amount", sa.Numeric(12, 2)),
        sa.Column("insurance_start_date", sa.Date()),
        sa.Column("insurance_end_date", sa.Date()),
        sa.Column("insurance_remarks", sa.Text()),
        sa.Column("insurance_documents", sa.Text()),
        sa.Column("include_insurance", sa.Boolean()),
 
        # Vehicle transport
        sa.Column("vehicle_type", sa.String(50)),
        sa.Column("vehicle_registration_no", sa.String(50)),
        sa.Column("vehicle_transport_mode", sa.String(50)),
        sa.Column("vehicle_transport_amount", sa.Numeric(12, 2)),
        sa.Column("vehicle_transport_remarks", sa.Text()),
        sa.Column("vehicle_transport_documents", sa.Text()),
        sa.Column("include_vehicle_transport", sa.Boolean()),
 
        # Totals
        sa.Column("total_travel", sa.Numeric(12, 2)),
        sa.Column("total_displacement", sa.Numeric(12, 2)),
        sa.Column("total_settling", sa.Numeric(12, 2)),
        sa.Column("total_goods_transport", sa.Numeric(12, 2)),
        sa.Column("total_packaging", sa.Numeric(12, 2)),
        sa.Column("total_insurance", sa.Numeric(12, 2)),
        sa.Column("total_vehicle_transport", sa.Numeric(12, 2)),
        sa.Column("total_admission", sa.Numeric(12, 2)),
        sa.Column("grand_total", sa.Numeric(12, 2)),
 
        sa.Column("remarks", sa.Text()),
        sa.Column("status", sa.String(30)),
 
        # Supervisor / HR / Finance
        sa.Column("updated_by_supervisor", sa.Date()),
        sa.Column("updated_by_supervisor_name", sa.String(150)),
        sa.Column("supervisor_comment", sa.Text()),
 
        sa.Column("updated_by_hr", sa.Date()),
        sa.Column("updated_by_hr_name", sa.String(150)),
        sa.Column("hr_comment", sa.Text()),
 
        sa.Column("updated_by_finance", sa.Date()),
        sa.Column("updated_by_finance_name", sa.String(150)),
        sa.Column("finance_comment", sa.Text()),
 
        sa.Column("created_by", sa.Integer()),
        sa.Column("created_at", sa.DateTime(), server_default=sa.func.now()),
        sa.Column("updated_by", sa.Integer()),
        sa.Column("updated_at", sa.DateTime()),
    )
 
    # ================= allowance_admission_child =================
    op.create_table(
        "allowance_admission_child",
        sa.Column("allowance_admission_child_id", sa.BigInteger(), primary_key=True),
        sa.Column(
            "allowance_claim_id",
            sa.BigInteger(),
            sa.ForeignKey("allowance_claim.allowance_claim_id", ondelete="CASCADE"),
            nullable=False
        ),
        sa.Column("child_name", sa.String(150)),
        sa.Column("relationship", sa.String(50)),
        sa.Column("class_studying", sa.String(50)),
        sa.Column("school_name", sa.String(150)),
        sa.Column("amount_claimed", sa.Numeric(12, 2)),
    )
 
 
def downgrade():
    op.drop_table("allowance_admission_child")
    op.drop_table("allowance_claim")