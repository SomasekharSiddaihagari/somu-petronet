"""drop employee_identity_proof table

Revision ID: 2060d8ae7880
Revises: dc424bda2528
Create Date: 2025-11-27 11:05:07.036104

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2060d8ae7880'
down_revision: Union[str, Sequence[str], None] = 'dc424bda2528'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None



def upgrade():
    # ✅ Drop table safely
    op.drop_table('employee_identity_proof')
 
 
def downgrade():
    # Optional rollback (only if ever needed)
    op.create_table(
        'employee_identity_proof',
        sa.Column('eip_id', sa.Integer, primary_key=True),
        sa.Column('user_id', sa.Integer, sa.ForeignKey('users.user_id')),
        sa.Column('aadhaar', sa.String),
        sa.Column('aadhaar_file', sa.String),
        sa.Column('pan', sa.String),
        sa.Column('pan_file', sa.String),
        sa.Column('driving_license', sa.String),
        sa.Column('driving_license_file', sa.String),
        sa.Column('passport', sa.String),
        sa.Column('passport_file', sa.String),
    )