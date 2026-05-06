"""add user profile status fields

Revision ID: b735ac649360
Revises: e1d6d38f32cd
Create Date: 2026-02-06 18:17:34.631124

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b735ac649360'
down_revision: Union[str, Sequence[str], None] = 'e1d6d38f32cd'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():

    # users table
    op.add_column('users', sa.Column('status_basic_info', sa.String(length=50), nullable=True))
    op.add_column('users', sa.Column('status_address', sa.String(length=50), nullable=True))
    op.add_column('users', sa.Column('status_bank', sa.String(length=50), nullable=True))
    op.add_column('users', sa.Column('status_identity_proof', sa.String(length=50), nullable=True))

    # users_history table
    op.add_column('users_history', sa.Column('status_basic_info', sa.String(length=50), nullable=True))
    op.add_column('users_history', sa.Column('status_address', sa.String(length=50), nullable=True))
    op.add_column('users_history', sa.Column('status_bank', sa.String(length=50), nullable=True))
    op.add_column('users_history', sa.Column('status_identity_proof', sa.String(length=50), nullable=True))


def downgrade():

    op.drop_column('users', 'status_basic_info')
    op.drop_column('users', 'status_address')
    op.drop_column('users', 'status_bank')
    op.drop_column('users', 'status_identity_proof')

    op.drop_column('users_history', 'status_basic_info')
    op.drop_column('users_history', 'status_address')
    op.drop_column('users_history', 'status_bank')
    op.drop_column('users_history', 'status_identity_proof')