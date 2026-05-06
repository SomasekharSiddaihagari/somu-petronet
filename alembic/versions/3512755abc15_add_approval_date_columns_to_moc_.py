"""add approval date columns to moc_requests

Revision ID: 3512755abc15
Revises: dc29906f8854
Create Date: 2025-11-06 18:15:08.884061

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '3512755abc15'
down_revision: Union[str, Sequence[str], None] = 'dc29906f8854'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column('moc_requests', sa.Column('submittion_date', sa.DateTime(), nullable=True))
    op.add_column('moc_requests', sa.Column('hira_approved_date', sa.DateTime(), nullable=True))
    op.add_column('moc_requests', sa.Column('sic_approved_date', sa.DateTime(), nullable=True))
    op.add_column('moc_requests', sa.Column('approved_date', sa.DateTime(), nullable=True))

def downgrade():
    op.drop_column('moc_requests', 'approved_date')
    op.drop_column('moc_requests', 'sic_approved_date')
    op.drop_column('moc_requests', 'hira_approved_date')
    op.drop_column('moc_requests', 'submittion_date')