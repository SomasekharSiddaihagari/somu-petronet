"""drop employee_identity_proof table

Revision ID: d3508842bc85
Revises: 580afdbb416b
Create Date: 2025-11-25 11:01:12.303667

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd3508842bc85'
down_revision: Union[str, Sequence[str], None] = '580afdbb416b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


 
 
def upgrade():

    # ✅ Drop the table safely (with CASCADE to avoid FK issues)

    op.execute("DROP TABLE IF EXISTS employee_identity_proof CASCADE")
 
 
def downgrade():

    # ✅ Recreate the table if rollback is needed

    op.create_table(

        'employee_identity_proof',

        sa.Column('eip_id', sa.Integer, primary_key=True),

        sa.Column('user_id', sa.Integer, sa.ForeignKey('users.user_id'), nullable=False),

        sa.Column('aadhaar', sa.String, nullable=True),

        sa.Column('aadhaar_file', sa.String, nullable=True),

        sa.Column('pan', sa.String, nullable=True),

        sa.Column('pan_file', sa.String, nullable=True),

        sa.Column('driving_license', sa.String, nullable=True),

        sa.Column('driving_license_file', sa.String, nullable=True),

        sa.Column('passport', sa.String, nullable=True),

        sa.Column('passport_file', sa.String, nullable=True),

    )

 