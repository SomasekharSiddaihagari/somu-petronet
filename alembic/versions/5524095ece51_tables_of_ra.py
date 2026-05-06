"""tables of ra

Revision ID: 5524095ece51
Revises: e4d82314a733
Create Date: 2025-12-29 12:37:07.887886

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5524095ece51'
down_revision: Union[str, Sequence[str], None] = 'e4d82314a733'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade():

    # -------------------------------------------------

    # RA CLAIM (MAIN)

    # -------------------------------------------------

    op.create_table(

        "ra_claim",

        sa.Column("ra_claim_id", sa.BigInteger(), primary_key=True),
 
        sa.Column("ra_claim_ref_id", sa.String(50), nullable=True),
 
        sa.Column("employee_name", sa.String(150), nullable=True),

        sa.Column("employee_id", sa.String(50), nullable=True),

        sa.Column("department", sa.String(100), nullable=True),

        sa.Column("designation", sa.String(100), nullable=True),

        sa.Column("station", sa.String(100), nullable=True),

        sa.Column("grade", sa.String(50), nullable=True),
 
        sa.Column("claim_module", sa.String(30), nullable=True),

        sa.Column("category", sa.String(150), nullable=True),
 
        sa.Column("status", sa.String(30), nullable=True),

        sa.Column("remarks", sa.Text(), nullable=True),
 
        # Supervisor

        sa.Column("updated_by_supervisor", sa.Date(), nullable=True),

        sa.Column("updated_by_supervisor_name", sa.String(150), nullable=True),
 
        # HR

        sa.Column("updated_by_hr", sa.Date(), nullable=True),

        sa.Column("updated_by_hr_name", sa.String(150), nullable=True),
 
        # Finance

        sa.Column("updated_by_finance", sa.Date(), nullable=True),

        sa.Column("updated_by_finance_name", sa.String(150), nullable=True),
 
        sa.Column("created_by", sa.Integer(), nullable=True),

        sa.Column(

            "created_at",

            sa.DateTime(timezone=True),

            server_default=sa.func.now()

        ),

        sa.Column("updated_by", sa.Integer(), nullable=True),

        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),

    )
 
    # -------------------------------------------------

    # RA CLAIM HISTORY

    # -------------------------------------------------

    op.create_table(

        "ra_claim_history",

        sa.Column("ra_claim_history_id", sa.BigInteger(), primary_key=True),
 
        sa.Column("ra_claim_id", sa.BigInteger(), nullable=True),

        sa.Column("ra_claim_ref_id", sa.String(50), nullable=True),
 
        sa.Column("employee_name", sa.String(150), nullable=True),

        sa.Column("employee_id", sa.String(50), nullable=True),

        sa.Column("department", sa.String(100), nullable=True),

        sa.Column("designation", sa.String(100), nullable=True),

        sa.Column("station", sa.String(100), nullable=True),

        sa.Column("grade", sa.String(50), nullable=True),
 
        sa.Column("claim_module", sa.String(30), nullable=True),

        sa.Column("category", sa.String(150), nullable=True),
 
        sa.Column("status", sa.String(30), nullable=True),

        sa.Column("remarks", sa.Text(), nullable=True),
 
        # Supervisor

        sa.Column("updated_by_supervisor", sa.Date(), nullable=True),

        sa.Column("updated_by_supervisor_name", sa.String(150), nullable=True),
 
        # HR

        sa.Column("updated_by_hr", sa.Date(), nullable=True),

        sa.Column("updated_by_hr_name", sa.String(150), nullable=True),
 
        # Finance

        sa.Column("updated_by_finance", sa.Date(), nullable=True),

        sa.Column("updated_by_finance_name", sa.String(150), nullable=True),
 
        sa.Column("created_by", sa.Integer(), nullable=True),

        sa.Column(

            "created_at",

            sa.DateTime(timezone=True),

            server_default=sa.func.now()

        ),

    )
 
 
def downgrade():

    op.drop_table("ra_claim_history")

    op.drop_table("ra_claim")
 