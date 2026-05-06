"""create user education tables

Revision ID: 4b3dad94f8fa
Revises: ffcdc4cca8ef
Create Date: 2025-11-26 16:22:38.817270

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4b3dad94f8fa'
down_revision: Union[str, Sequence[str], None] = 'ffcdc4cca8ef'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade():
    op.create_table(
        'user_education',
        sa.Column('education_id', sa.Integer, primary_key=True),
        sa.Column('user_id', sa.Integer, sa.ForeignKey('users.user_id', ondelete='CASCADE'), nullable=False),
 
        sa.Column('qualification', sa.String(), nullable=True),
        sa.Column('year_of_completion', sa.Integer(), nullable=True),
      
        sa.Column('education_document', sa.String(), nullable=True),
 
        sa.Column('created_at', sa.DateTime(), nullable=True),
    )
 
    op.create_table(
        'user_education_history',
        sa.Column('history_id', sa.Integer, primary_key=True),
        sa.Column('education_id', sa.Integer),
        sa.Column('user_id', sa.Integer),
 
        sa.Column('qualification', sa.String(), nullable=True),
        sa.Column('year_of_completion', sa.Integer(), nullable=True),
      
        sa.Column('education_document', sa.String(), nullable=True),
 
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('history_created_at', sa.DateTime(), nullable=True),
    )
 
 
def downgrade():
    op.drop_table('user_education_history')
    op.drop_table('user_education')