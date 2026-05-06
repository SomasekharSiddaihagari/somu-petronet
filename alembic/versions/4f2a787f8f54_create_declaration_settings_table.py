"""create declaration_settings table

Revision ID: 4f2a787f8f54
Revises: b2c99905b699
Create Date: 2025-11-25 12:56:11.569654

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4f2a787f8f54'
down_revision: Union[str, Sequence[str], None] = 'b2c99905b699'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None



def upgrade():
    op.create_table(
        'declaration_settings',
        sa.Column('dec_id', sa.Integer, primary_key=True),
        sa.Column('declaration_type', sa.String(50), nullable=False, unique=True),
        sa.Column('opening_date', sa.Date, nullable=True),
        sa.Column('closing_date', sa.Date, nullable=True),
        sa.Column('is_active', sa.Boolean, default=False)
    )
def downgrade():
    op.drop_table('declaration_settings')