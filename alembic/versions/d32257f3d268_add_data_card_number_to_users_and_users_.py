"""add data_card_number to users and users_history

Revision ID: d32257f3d268
Revises: 6c1657a96ee6
Create Date: 2026-02-09 12:30:46.983147

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd32257f3d268'
down_revision: Union[str, Sequence[str], None] = '6c1657a96ee6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column('users', sa.Column('data_card_number', sa.String(length=50), nullable=True))
    op.add_column('users_history', sa.Column('data_card_number', sa.String(length=50), nullable=True))

def downgrade():
    op.drop_column('users', 'data_card_number')
    op.drop_column('users_history', 'data_card_number')