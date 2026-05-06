"""change fixed conveyance claim amount to int

Revision ID: 26e5f33f5338
Revises: f51ecabb2aff
Create Date: 2026-01-25 00:19:12.995287

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '26e5f33f5338'
down_revision: Union[str, Sequence[str], None] = 'f51ecabb2aff'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade():
    # vehicle_cm_reimbursement
    op.execute("""
        ALTER TABLE vehicle_cm_reimbursement
        ALTER COLUMN fixed_conveyance_claim
        TYPE INTEGER
        USING CASE
            WHEN fixed_conveyance_claim = TRUE THEN 1
            WHEN fixed_conveyance_claim = FALSE THEN 0
            ELSE NULL
        END
    """)

    # vehicle_cm_reimbursement_history
    op.execute("""
        ALTER TABLE vehicle_cm_reimbursement_history
        ALTER COLUMN fixed_conveyance_claim
        TYPE INTEGER
        USING CASE
            WHEN fixed_conveyance_claim = TRUE THEN 1
            WHEN fixed_conveyance_claim = FALSE THEN 0
            ELSE NULL
        END
    """)


def downgrade():
    op.execute("""
        ALTER TABLE vehicle_cm_reimbursement
        ALTER COLUMN fixed_conveyance_claim
        TYPE BOOLEAN
        USING fixed_conveyance_claim::BOOLEAN
    """)

    op.execute("""
        ALTER TABLE vehicle_cm_reimbursement_history
        ALTER COLUMN fixed_conveyance_claim
        TYPE BOOLEAN
        USING fixed_conveyance_claim::BOOLEAN
    """)