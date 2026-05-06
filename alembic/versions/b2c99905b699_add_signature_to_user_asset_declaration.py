"""add signature to user_asset_declaration

Revision ID: b2c99905b699
Revises: d3508842bc85
Create Date: 2025-11-25 11:26:33.330928

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b2c99905b699'
down_revision: Union[str, Sequence[str], None] = 'd3508842bc85'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column(
        'user_asset_declaration',
        sa.Column('signature', sa.Text(), nullable=True)
    )
 
 
def downgrade():
    op.drop_column('user_asset_declaration', 'signature')