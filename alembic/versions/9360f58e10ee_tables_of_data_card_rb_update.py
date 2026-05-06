"""tables of data_Card rb update

Revision ID: 9360f58e10ee
Revises: cb924d455819
Create Date: 2025-12-29 13:27:50.244846

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9360f58e10ee'
down_revision: Union[str, Sequence[str], None] = 'cb924d455819'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade():

    # -------------------------------------------------

    # MOBILE BILL REIMBURSEMENT

    # -------------------------------------------------

    with op.batch_alter_table("mobile_bill_reimbursement") as batch_op:

        batch_op.add_column(

            sa.Column("monthly_limit", sa.Numeric(12, 2), nullable=True)

        )
 
    with op.batch_alter_table("mobile_bill_reimbursement_history") as batch_op:

        batch_op.add_column(

            sa.Column("monthly_limit", sa.Numeric(12, 2), nullable=True)

        )
 
    # -------------------------------------------------

    # DATA CARD REIMBURSEMENT

    # -------------------------------------------------

    with op.batch_alter_table("data_card_reimbursement") as batch_op:

        batch_op.add_column(

            sa.Column("bill_amount_total", sa.Numeric(12, 2), nullable=True)

        )
 
    with op.batch_alter_table("data_card_reimbursement_history") as batch_op:

        batch_op.add_column(

            sa.Column("bill_amount_total", sa.Numeric(12, 2), nullable=True)

        )
 
 
def downgrade():

    # -------------------------------------------------

    # DATA CARD REIMBURSEMENT

    # -------------------------------------------------

    with op.batch_alter_table("data_card_reimbursement_history") as batch_op:

        batch_op.drop_column("bill_amount_total")
 
    with op.batch_alter_table("data_card_reimbursement") as batch_op:

        batch_op.drop_column("bill_amount_total")
 
    # -------------------------------------------------

    # MOBILE BILL REIMBURSEMENT

    # -------------------------------------------------

    with op.batch_alter_table("mobile_bill_reimbursement_history") as batch_op:

        batch_op.drop_column("monthly_limit")
 
    with op.batch_alter_table("mobile_bill_reimbursement") as batch_op:

        batch_op.drop_column("monthly_limit")
 