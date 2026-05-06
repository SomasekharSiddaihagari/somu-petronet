"""vehicle table

Revision ID: e95ba06692f3
Revises: b46224953fb1
Create Date: 2025-12-18 15:10:53.313454

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e95ba06692f3'
down_revision: Union[str, Sequence[str], None] = 'b46224953fb1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade():
    op.create_table(
        'user_vehicle',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('user_id', sa.Integer, sa.ForeignKey('users.user_id', ondelete="CASCADE")),
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
        sa.Column('created_date', sa.Date(), nullable=True),
        sa.Column('modified_date', sa.Date(), nullable=True),
    )
 
 
def downgrade():
    op.drop_table('user_vehicle')