"""Add colsure_date, sic_comments, colsure_comments to moc_requests

Revision ID: e286525c91b3
Revises: 3512755abc15
Create Date: 2025-11-07 13:18:57.885015

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'e286525c91b3'
down_revision: Union[str, Sequence[str], None] = '3512755abc15'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column('moc_requests', sa.Column('colsure_date', sa.DateTime(), nullable=True))
    op.add_column('moc_requests', sa.Column('sic_comments', sa.Text(), nullable=True))
    op.add_column('moc_requests', sa.Column('colsure_comments', sa.Text(), nullable=True))


def downgrade():
    op.drop_column('moc_requests', 'colsure_comments')
    op.drop_column('moc_requests', 'sic_comments')
    op.drop_column('moc_requests', 'colsure_date')