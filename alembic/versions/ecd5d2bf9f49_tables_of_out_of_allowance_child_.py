"""tables of out of allowance child  updgrade

Revision ID: ecd5d2bf9f49
Revises: 39bd8e41b367
Create Date: 2025-12-29 18:56:21.930406

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ecd5d2bf9f49'
down_revision: Union[str, Sequence[str], None] = '39bd8e41b367'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


from alembic import op

import sqlalchemy as sa
 
 

 
def upgrade():

    # =====================================================

    # allowance_claim

    # =====================================================

    op.add_column(

        "allowance_claim",

        sa.Column("maximum_eligible_days", sa.Integer(), nullable=True)

    )
 
    op.add_column(

        "allowance_claim",

        sa.Column(

            "amount_claimed_household_transport",

            sa.Numeric(12, 2),

            nullable=True

        )

    )
 
    op.add_column(

        "allowance_claim",

        sa.Column(

            "maximum_eligible_amount_packaging",

            sa.Numeric(12, 2),

            nullable=True

        )

    )
 
    op.add_column(

        "allowance_claim",

        sa.Column(

            "vehicle_transport_distance_km",

            sa.Numeric(10, 2),

            nullable=True

        )

    )
 
    # =====================================================

    # allowance_claim_history

    # =====================================================

    op.add_column(

        "allowance_claim_history",

        sa.Column("maximum_eligible_days", sa.Integer(), nullable=True)

    )
 
    op.add_column(

        "allowance_claim_history",

        sa.Column(

            "amount_claimed_household_transport",

            sa.Numeric(12, 2),

            nullable=True

        )

    )
 
    op.add_column(

        "allowance_claim_history",

        sa.Column(

            "maximum_eligible_amount_packaging",

            sa.Numeric(12, 2),

            nullable=True

        )

    )
 
    op.add_column(

        "allowance_claim_history",

        sa.Column(

            "vehicle_transport_distance_km",

            sa.Numeric(10, 2),

            nullable=True

        )

    )
 
    # =====================================================

    # allowance_admission_child

    # =====================================================

    op.add_column(

        "allowance_admission_child",

        sa.Column("remarks", sa.Text(), nullable=True)

    )
 
    op.add_column(

        "allowance_admission_child",

        sa.Column("document_names", sa.Text(), nullable=True)

    )
 
    # =====================================================

    # allowance_admission_child_history

    # =====================================================

    op.add_column(

        "allowance_admission_child_history",

        sa.Column("remarks", sa.Text(), nullable=True)

    )
 
    op.add_column(

        "allowance_admission_child_history",

        sa.Column("document_names", sa.Text(), nullable=True)

    )
 
 
def downgrade():

    # -------- admission child history --------

    op.drop_column("allowance_admission_child_history", "document_names")

    op.drop_column("allowance_admission_child_history", "remarks")
 
    # -------- admission child --------

    op.drop_column("allowance_admission_child", "document_names")

    op.drop_column("allowance_admission_child", "remarks")
 
    # -------- allowance claim history --------

    op.drop_column("allowance_claim_history", "vehicle_transport_distance_km")

    op.drop_column("allowance_claim_history", "maximum_eligible_amount_packaging")

    op.drop_column("allowance_claim_history", "amount_claimed_household_transport")

    op.drop_column("allowance_claim_history", "maximum_eligible_days")
 
    # -------- allowance claim --------

    op.drop_column("allowance_claim", "vehicle_transport_distance_km")

    op.drop_column("allowance_claim", "maximum_eligible_amount_packaging")

    op.drop_column("allowance_claim", "amount_claimed_household_transport")

    op.drop_column("allowance_claim", "maximum_eligible_days")

 