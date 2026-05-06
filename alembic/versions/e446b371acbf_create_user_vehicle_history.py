"""create user_vehicle_history

Revision ID: e446b371acbf
Revises: e95ba06692f3
Create Date: 2025-12-18 15:26:19.157606

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e446b371acbf'
down_revision: Union[str, Sequence[str], None] = 'e95ba06692f3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None



def upgrade():
    op.create_table(
        'user_vehicle_history',
        sa.Column('history_id', sa.Integer, primary_key=True, index=True),
 
        sa.Column('user_id', sa.Integer),
 
        sa.Column('vehicle_type', sa.String(), nullable=True),
        sa.Column('vehicle_make', sa.String(), nullable=True),
        sa.Column('vehicle_model', sa.String(), nullable=True),
        sa.Column('color', sa.String(), nullable=True),
        sa.Column('fuel_type', sa.String(), nullable=True),
 
        sa.Column('rc_expiry_date', sa.Date(), nullable=True),
        sa.Column('insurance_provider', sa.String(), nullable=True),
        sa.Column('insurance_policy_number', sa.String(), nullable=True),
        sa.Column('insurance_expiry_date', sa.Date(), nullable=True),
        sa.Column('puc_expiry_date', sa.Date(), nullable=True),
 
        sa.Column('document_upload', sa.String(), nullable=True),
 
        sa.Column('history_created_at', sa.DateTime(), nullable=True),
    )
 
 
def downgrade():
    op.drop_table('user_vehicle_history')