"""tables of out of claim rem

Revision ID: 326b55162cfd
Revises: 18fb030a5fad
Create Date: 2025-12-29 16:30:18.330015

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '326b55162cfd'
down_revision: Union[str, Sequence[str], None] = '18fb030a5fad'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():

    op.create_table(

        "out_of_pocket_claim",

        sa.Column("out_of_pocket_claim_id", sa.BigInteger(), primary_key=True),

        sa.Column("ra_claim_id", sa.BigInteger(), sa.ForeignKey("ra_claim.ra_claim_id")),

        sa.Column("claim_month_year", sa.String(20)),

        sa.Column("total_claims", sa.Integer()),

        sa.Column("total_amount", sa.Numeric(12, 2)),

        sa.Column("document_names", sa.Text()),

        sa.Column("remarks", sa.Text()),

        sa.Column("declaration_accepted", sa.Boolean()),

        sa.Column("status", sa.String(30)),
 
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
 
    op.create_table(

        "out_of_pocket_claim_entry",

        sa.Column("out_of_pocket_claim_entry_id", sa.BigInteger(), primary_key=True),

        sa.Column("out_of_pocket_claim_id", sa.BigInteger(),

                  sa.ForeignKey("out_of_pocket_claim.out_of_pocket_claim_id")),

        sa.Column("entry_type", sa.String(30)),

        sa.Column("hours", sa.Numeric(5, 2)),

        sa.Column("claim_date", sa.Date()),

        sa.Column("amount", sa.Numeric(12, 2)),

        sa.Column("justification", sa.Text()),

        sa.Column("created_at", sa.DateTime(), server_default=sa.func.now()),

    )
 
    op.create_table(

        "out_of_pocket_claim_history",

        sa.Column("out_of_pocket_claim_history_id", sa.BigInteger(), primary_key=True),

        sa.Column("out_of_pocket_claim_id", sa.BigInteger()),

        sa.Column("ra_claim_id", sa.BigInteger()),

        sa.Column("claim_month_year", sa.String(20)),

        sa.Column("total_claims", sa.Integer()),

        sa.Column("total_amount", sa.Numeric(12, 2)),

        sa.Column("document_names", sa.Text()),

        sa.Column("remarks", sa.Text()),

        sa.Column("declaration_accepted", sa.Boolean()),

        sa.Column("status", sa.String(30)),
 
        sa.Column("updated_by_supervisor", sa.Date()),

        sa.Column("updated_by_supervisor_name", sa.String(150)),

        sa.Column("supervisor_comment", sa.Text()),
 
        sa.Column("updated_by_hr", sa.Date()),

        sa.Column("updated_by_hr_name", sa.String(150)),

        sa.Column("hr_comment", sa.Text()),
 
        sa.Column("updated_by_finance", sa.Date()),

        sa.Column("updated_by_finance_name", sa.String(150)),

        sa.Column("finance_comment", sa.Text()),
 
        sa.Column("created_at", sa.DateTime(), server_default=sa.func.now()),

    )
 
    op.create_table(

        "out_of_pocket_claim_entry_history",

        sa.Column("out_of_pocket_claim_entry_history_id", sa.BigInteger(), primary_key=True),

        sa.Column("out_of_pocket_claim_entry_id", sa.BigInteger()),

        sa.Column("out_of_pocket_claim_id", sa.BigInteger()),

        sa.Column("entry_type", sa.String(30)),

        sa.Column("hours", sa.Numeric(5, 2)),

        sa.Column("claim_date", sa.Date()),

        sa.Column("amount", sa.Numeric(12, 2)),

        sa.Column("justification", sa.Text()),

        sa.Column("created_at", sa.DateTime(), server_default=sa.func.now()),

    )
 
 
def downgrade():

    op.drop_table("out_of_pocket_claim_entry_history")

    op.drop_table("out_of_pocket_claim_history")

    op.drop_table("out_of_pocket_claim_entry")

    op.drop_table("out_of_pocket_claim")

 