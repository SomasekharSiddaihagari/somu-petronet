"""add hop fields to out_of_pocket_claim tables

Revision ID: d9846044767e
Revises: 0da98dff8e6f
Create Date: 2026-03-02 12:35:04.265844

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd9846044767e'
down_revision: Union[str, Sequence[str], None] = '0da98dff8e6f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # Add columns to out_of_pocket_claim
    op.add_column(
        'out_of_pocket_claim',
        sa.Column('updated_by_hop', sa.Date(), nullable=True)
    )
    op.add_column(
        'out_of_pocket_claim',
        sa.Column('updated_by_hop_name', sa.String(length=150), nullable=True)
    )
    op.add_column(
        'out_of_pocket_claim',
        sa.Column('hop_comment', sa.Text(), nullable=True)
    )

    # Add columns to out_of_pocket_claim_history
    op.add_column(
        'out_of_pocket_claim_history',
        sa.Column('updated_by_hop', sa.Date(), nullable=True)
    )
    op.add_column(
        'out_of_pocket_claim_history',
        sa.Column('updated_by_hop_name', sa.String(length=150), nullable=True)
    )
    op.add_column(
        'out_of_pocket_claim_history',
        sa.Column('hop_comment', sa.Text(), nullable=True)
    )


def downgrade():
    # Remove columns from out_of_pocket_claim
    op.drop_column('out_of_pocket_claim', 'hop_comment')
    op.drop_column('out_of_pocket_claim', 'updated_by_hop_name')
    op.drop_column('out_of_pocket_claim', 'updated_by_hop')

    # Remove columns from out_of_pocket_claim_history
    op.drop_column('out_of_pocket_claim_history', 'hop_comment')
    op.drop_column('out_of_pocket_claim_history', 'updated_by_hop_name')
    op.drop_column('out_of_pocket_claim_history', 'updated_by_hop')