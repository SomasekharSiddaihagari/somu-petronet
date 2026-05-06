"""create user_finance_history table

Revision ID: f957a8986396
Revises: 6c7da82adac2
Create Date: 2025-11-25 15:33:09.855764

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f957a8986396'
down_revision: Union[str, Sequence[str], None] = '6c7da82adac2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade():
    op.create_table(
        'user_finance_history',
        sa.Column('history_id', sa.Integer, primary_key=True),
        sa.Column('user_finance_id', sa.Integer),
        sa.Column('user_id', sa.Integer),
 
        sa.Column('date', sa.Date),
        sa.Column('financial_year', sa.String),
        sa.Column('opting_for_concessional_rate', sa.String),
 
        sa.Column('residing_in_rented_house', sa.String),
        sa.Column('monthly_rent', sa.Float),
        sa.Column('landlord_name', sa.String),
        sa.Column('temporary_address', sa.Text),
 
        sa.Column('pension_plan', sa.String),
        sa.Column('lic_premium', sa.String),
        sa.Column('ppf', sa.String),
        sa.Column('ulip', sa.String),
        sa.Column('tuition_fees', sa.String),
        sa.Column('nsc', sa.String),
        sa.Column('nsc_interest', sa.String),
        sa.Column('housing_loan_repayment', sa.String),
        sa.Column('other_investments', sa.String),
 
        sa.Column('infrastructure_bond', sa.String),
        sa.Column('educational_loan_interest', sa.String),
        sa.Column('contribution_to_nps', sa.String),
 
        sa.Column('upload_document', sa.String),
        sa.Column('declaration_text', sa.Text),
        sa.Column('signature_name', sa.String),
 
        sa.Column('history_created_at', sa.DateTime)
    )
 
def downgrade():
    op.drop_table('user_finance_history')
