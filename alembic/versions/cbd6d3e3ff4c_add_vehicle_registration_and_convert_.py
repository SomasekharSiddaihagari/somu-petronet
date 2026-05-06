"""add vehicle registration and convert document_upload to text

Revision ID: cbd6d3e3ff4c
Revises: e446b371acbf
Create Date: 2025-12-18 15:52:59.718585

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'cbd6d3e3ff4c'
down_revision: Union[str, Sequence[str], None] = 'e446b371acbf'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # --- UserVehicle Table ---
    op.add_column('user_vehicle',
        sa.Column('vehicle_registration_no', sa.String(), nullable=True)
    )
 
    # Change document_upload from VARCHAR → TEXT
    op.alter_column(
        'user_vehicle',
        'document_upload',
        type_=sa.Text(),
        existing_type=sa.String(),
        existing_nullable=True
    )
 
    # --- UserVehicleHistory Table ---
    op.add_column('user_vehicle_history',
        sa.Column('vehicle_registration_no', sa.String(), nullable=True)
    )
 
    op.alter_column(
        'user_vehicle_history',
        'document_upload',
        type_=sa.Text(),
        existing_type=sa.String(),
        existing_nullable=True
    )
 
 
def downgrade():
    # --- UserVehicle Table ---
    op.drop_column('user_vehicle', 'vehicle_registration_no')
 
    op.alter_column(
        'user_vehicle',
        'document_upload',
        type_=sa.String(),
        existing_type=sa.Text(),
        existing_nullable=True
    )
 
    # --- UserVehicleHistory Table ---
    op.drop_column('user_vehicle_history', 'vehicle_registration_no')
 
    op.alter_column(
        'user_vehicle_history',
        'document_upload',
        type_=sa.String(),
        existing_type=sa.Text(),
        existing_nullable=True
    )