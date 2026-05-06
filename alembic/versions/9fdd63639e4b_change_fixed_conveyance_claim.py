"""change fixed conveyance claim 

Revision ID: 9fdd63639e4b
Revises: 26e5f33f5338
Create Date: 2026-01-26 20:19:32.233868

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9fdd63639e4b'
down_revision: Union[str, Sequence[str], None] = '26e5f33f5338'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # ========== vehicle_cm_reimbursement ==========
    
    op.execute("""
        ALTER TABLE vehicle_cm_reimbursement
        ALTER COLUMN fixed_conveyance_claim
        TYPE BOOLEAN
        USING (
            CASE
                WHEN fixed_conveyance_claim = 1 THEN TRUE
                WHEN fixed_conveyance_claim = 0 THEN FALSE
                ELSE NULL
            END
        );
    """)

    op.add_column(
        "vehicle_cm_reimbursement",
        sa.Column("fixed_conveyance_claim_amount", sa.Integer(), nullable=True)
    )

    # ========== vehicle_cm_reimbursement_history ==========
    
    op.execute("""
        ALTER TABLE vehicle_cm_reimbursement_history
        ALTER COLUMN fixed_conveyance_claim
        TYPE BOOLEAN
        USING (
            CASE
                WHEN fixed_conveyance_claim = 1 THEN TRUE
                WHEN fixed_conveyance_claim = 0 THEN FALSE
                ELSE NULL
            END
        );
    """)

    op.add_column(
        "vehicle_cm_reimbursement_history",
        sa.Column("fixed_conveyance_claim_amount", sa.Integer(), nullable=True)
    )


def downgrade():
    # ========== vehicle_cm_reimbursement ==========
    
    op.drop_column("vehicle_cm_reimbursement", "fixed_conveyance_claim_amount")

    op.execute("""
        ALTER TABLE vehicle_cm_reimbursement
        ALTER COLUMN fixed_conveyance_claim
        TYPE INTEGER
        USING (
            CASE
                WHEN fixed_conveyance_claim = TRUE THEN 1
                WHEN fixed_conveyance_claim = FALSE THEN 0
                ELSE NULL
            END
        );
    """)

    # ========== vehicle_cm_reimbursement_history ==========
    
    op.drop_column("vehicle_cm_reimbursement_history", "fixed_conveyance_claim_amount")

    op.execute("""
        ALTER TABLE vehicle_cm_reimbursement_history
        ALTER COLUMN fixed_conveyance_claim
        TYPE INTEGER
        USING (
            CASE
                WHEN fixed_conveyance_claim = TRUE THEN 1
                WHEN fixed_conveyance_claim = FALSE THEN 0
                ELSE NULL
            END
        );
    """)