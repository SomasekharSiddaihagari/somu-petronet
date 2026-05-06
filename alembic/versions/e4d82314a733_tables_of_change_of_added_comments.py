"""tables of change of added comments

Revision ID: e4d82314a733
Revises: a98796e0523c
Create Date: 2025-12-29 11:18:31.443684

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e4d82314a733'
down_revision: Union[str, Sequence[str], None] = 'a98796e0523c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


 
# Fields to add

def approval_columns():

    return [

        sa.Column("updated_by_supervisor", sa.Date(), nullable=True),

        sa.Column("updated_by_supervisor_name", sa.String(150), nullable=True),
 
        sa.Column("updated_by_hr", sa.Date(), nullable=True),

        sa.Column("updated_by_hr_name", sa.String(150), nullable=True),
 
        sa.Column("updated_by_finance", sa.Date(), nullable=True),

        sa.Column("updated_by_finance_name", sa.String(150), nullable=True),

    ]
 
 
# All tables to update

TABLES = [

    "asset_claim",

    "asset_claim_submission",

    "asset_claim_disbursement",

    "encashment_main",

    "leave_encashment",
 
    "asset_claim_history",

    "asset_claim_submission_history",

    "asset_claim_disbursement_history",

    "encashment_main_history",

    "leave_encashment_history",

]
 
 
def upgrade():

    for table in TABLES:

        with op.batch_alter_table(table) as batch_op:

            for column in approval_columns():

                batch_op.add_column(column)
 
 
def downgrade():

    for table in TABLES:

        with op.batch_alter_table(table) as batch_op:

            batch_op.drop_column("updated_by_finance_name")

            batch_op.drop_column("updated_by_finance")

            batch_op.drop_column("updated_by_hr_name")

            batch_op.drop_column("updated_by_hr")

            batch_op.drop_column("updated_by_supervisor_name")

            batch_op.drop_column("updated_by_supervisor")

 
