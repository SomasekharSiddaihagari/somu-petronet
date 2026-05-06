"""create safety committee discussions and history tables

Revision ID: d9def7668b89
Revises: 807a1736a2cf
Create Date: 2026-02-24 20:34:25.256812

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd9def7668b89'
down_revision: Union[str, Sequence[str], None] = '807a1736a2cf'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # ---------------------------------------------------
    # safety_committee_minutes_discussions
    # ---------------------------------------------------
    op.create_table(
        'safety_committee_minutes_discussions',

        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column(
            'scmm_id',
            sa.Integer(),
            sa.ForeignKey('safety_committee_minutes.scmm_id', ondelete="CASCADE"),
            nullable=True
        ),

        sa.Column('row_no', sa.Integer(), nullable=False),

        sa.Column('description_of_discussion', sa.Text(), nullable=True),
        sa.Column('issues_discussed', sa.Text(), nullable=True),
        sa.Column('action_taken', sa.Text(), nullable=True),
        sa.Column('completed_on', sa.Date(), nullable=True),
        sa.Column('action_by', sa.String(length=255), nullable=True),
        sa.Column('target_date', sa.Date(), nullable=True),
    )

    # ---------------------------------------------------
    # safety_committee_minutes_discussions_history
    # ---------------------------------------------------
    op.create_table(
        'safety_committee_minutes_discussions_history',

        sa.Column('history_id', sa.Integer(), primary_key=True, autoincrement=True),

        # original discussion id reference
        sa.Column('id', sa.Integer(), nullable=True),

        sa.Column(
            'scmm_id',
            sa.Integer(),
            sa.ForeignKey('safety_committee_minutes.scmm_id', ondelete="CASCADE"),
            nullable=True
        ),

        sa.Column('row_no', sa.Integer(), nullable=False),

        sa.Column('description_of_discussion', sa.Text(), nullable=True),
        sa.Column('issues_discussed', sa.Text(), nullable=True),
        sa.Column('action_taken', sa.Text(), nullable=True),
        sa.Column('completed_on', sa.Date(), nullable=True),
        sa.Column('action_by', sa.String(length=255), nullable=True),
        sa.Column('target_date', sa.Date(), nullable=True),
    )


def downgrade():
    op.drop_table('safety_committee_minutes_discussions_history')
    op.drop_table('safety_committee_minutes_discussions')