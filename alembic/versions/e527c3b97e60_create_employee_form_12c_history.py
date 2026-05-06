"""create employee_form_12c_history

Revision ID: e527c3b97e60
Revises: 1874828b784f
Create Date: 2025-11-25 15:54:10.877184

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e527c3b97e60'
down_revision: Union[str, Sequence[str], None] = '1874828b784f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table(
        'employee_form_12c_history',
        sa.Column('history_id', sa.Integer, primary_key=True),
        sa.Column('form_id', sa.Integer),
        sa.Column('user_id', sa.Integer),
 
        sa.Column('self_alv', sa.String),
        sa.Column('lo1_alv', sa.String),
        sa.Column('lo2_alv', sa.String),
 
        sa.Column('self_municipal_tax', sa.String),
        sa.Column('lo1_municipal_tax', sa.String),
        sa.Column('lo2_municipal_tax', sa.String),
 
        sa.Column('self_annual_value', sa.String),
        sa.Column('lo1_annual_value', sa.String),
        sa.Column('lo2_annual_value', sa.String),
 
        sa.Column('self_less_30', sa.String),
        sa.Column('lo1_less_30', sa.String),
        sa.Column('lo2_less_30', sa.String),
 
        sa.Column('house_type_self', sa.String),
        sa.Column('house_type_lo1', sa.String),
        sa.Column('house_type_lo2', sa.String),
 
        sa.Column('self_interest', sa.String),
        sa.Column('lo1_interest', sa.String),
        sa.Column('lo2_interest', sa.String),
 
        sa.Column('self_loan_date', sa.Date),
        sa.Column('lo1_loan_date', sa.Date),
        sa.Column('lo2_loan_date', sa.Date),
 
        sa.Column('self_one_fifth_interest', sa.String),
        sa.Column('lo1_one_fifth_interest', sa.String),
        sa.Column('lo2_one_fifth_interest', sa.String),
 
        sa.Column('self_net_income', sa.String),
        sa.Column('lo1_net_income', sa.String),
        sa.Column('lo2_net_income', sa.String),
 
        sa.Column('self_tds_self_lease', sa.String),
        sa.Column('lo1_tds_self_lease', sa.String),
        sa.Column('lo2_tds_self_lease', sa.String),
 
        sa.Column('self_cess_self_lease', sa.String),
        sa.Column('lo1_cess_self_lease', sa.String),
        sa.Column('lo2_cess_self_lease', sa.String),
 
        sa.Column('self_capital_gains', sa.String),
        sa.Column('lo1_capital_gains', sa.String),
        sa.Column('lo2_capital_gains', sa.String),
 
        sa.Column('self_other_sources', sa.String),
        sa.Column('lo1_other_sources', sa.String),
        sa.Column('lo2_other_sources', sa.String),
 
        sa.Column('self_aggregate_items', sa.String),
        sa.Column('lo1_aggregate_items', sa.String),
        sa.Column('lo2_aggregate_items', sa.String),
 
        sa.Column('self_tds_other_income', sa.String),
        sa.Column('lo1_tds_other_income', sa.String),
        sa.Column('lo2_tds_other_income', sa.String),
 
        sa.Column('self_cess_other_income', sa.String),
        sa.Column('lo1_cess_other_income', sa.String),
        sa.Column('lo2_cess_other_income', sa.String),
 
        sa.Column('self_total_tds', sa.String),
        sa.Column('lo1_total_tds', sa.String),
        sa.Column('lo2_total_tds', sa.String),
 
        sa.Column('self_total_cess', sa.String),
        sa.Column('lo1_total_cess', sa.String),
        sa.Column('lo2_total_cess', sa.String),
 
        sa.Column('upload_document', sa.String),
        sa.Column('declared_place', sa.String),
        sa.Column('declared_date', sa.Date),
        sa.Column('signature_name', sa.String),
 
        sa.Column('history_created_at', sa.DateTime)
    )
 
 
def downgrade():
    op.drop_table('employee_form_12c_history')