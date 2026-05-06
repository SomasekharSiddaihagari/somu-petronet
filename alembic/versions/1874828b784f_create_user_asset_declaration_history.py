"""create user_asset_declaration_history

Revision ID: 1874828b784f
Revises: f957a8986396
Create Date: 2025-11-25 15:46:20.874624

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1874828b784f'
down_revision: Union[str, Sequence[str], None] = 'f957a8986396'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table(
        'user_asset_declaration_history',
        sa.Column('history_id', sa.Integer, primary_key=True),
 
        sa.Column('asset_id', sa.Integer),
        sa.Column('user_id', sa.Integer),
 
        sa.Column('date', sa.Date),
        sa.Column('financial_year', sa.String),
        sa.Column('document', sa.String),
 
        sa.Column('asset_type', sa.String),
 
        sa.Column('details', sa.Text),
        sa.Column('held_in_name', sa.String),
        sa.Column('acquisition_date', sa.Date),
        sa.Column('nature', sa.String),
        sa.Column('party', sa.String),
        sa.Column('finance_amount', sa.Float),
        sa.Column('source_of_finance', sa.String),
        sa.Column('profit_amount', sa.Float),
 
        sa.Column('history_created_at', sa.DateTime)
    )
 
def downgrade():
    op.drop_table('user_asset_declaration_history')