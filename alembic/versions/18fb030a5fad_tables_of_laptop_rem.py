"""tables of laptop rem

Revision ID: 18fb030a5fad
Revises: e493e6dffef4
Create Date: 2025-12-29 16:10:59.644371

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '18fb030a5fad'
down_revision: Union[str, Sequence[str], None] = 'e493e6dffef4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():

    # ---------------- MAIN TABLE ----------------

    op.create_table(

        "laptop_maintenance_reimbursement",

        sa.Column(

            "laptop_maintenance_reimbursement_id",

            sa.BigInteger(),

            primary_key=True

        ),
 
        sa.Column(

            "ra_claim_id",

            sa.BigInteger(),

            sa.ForeignKey("ra_claim.ra_claim_id", ondelete="CASCADE"),

            nullable=False

        ),
 
        sa.Column("date_of_purchase", sa.Date(), nullable=True),

        sa.Column("date_of_claim", sa.Date(), nullable=True),

        sa.Column("date_of_previous_claim", sa.Date(), nullable=True),
 
        sa.Column("amount_claimed", sa.Numeric(12, 2), nullable=True),
 
        sa.Column("annual_limit", sa.Numeric(12, 2), nullable=True),

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

        sa.Column(

            "created_at",

            sa.DateTime(timezone=True),

            server_default=sa.func.now()

        ),

        sa.Column("updated_by", sa.Integer(), nullable=True),

        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),

    )
 
    # ---------------- HISTORY TABLE ----------------

    op.create_table(

        "laptop_maintenance_reimbursement_history",

        sa.Column(

            "laptop_maintenance_reimbursement_history_id",

            sa.BigInteger(),

            primary_key=True

        ),
 
        sa.Column("laptop_maintenance_reimbursement_id", sa.BigInteger(), nullable=True),

        sa.Column("ra_claim_id", sa.BigInteger(), nullable=True),
 
        sa.Column("date_of_purchase", sa.Date(), nullable=True),

        sa.Column("date_of_claim", sa.Date(), nullable=True),

        sa.Column("date_of_previous_claim", sa.Date(), nullable=True),
 
        sa.Column("amount_claimed", sa.Numeric(12, 2), nullable=True),
 
        sa.Column("annual_limit", sa.Numeric(12, 2), nullable=True),

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

        sa.Column(

            "created_at",

            sa.DateTime(timezone=True),

            server_default=sa.func.now()

        ),

    )
 
 
def downgrade():

    op.drop_table("laptop_maintenance_reimbursement_history")

    op.drop_table("laptop_maintenance_reimbursement")
 