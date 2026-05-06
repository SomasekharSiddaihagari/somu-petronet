"""add ms_logbook_id column

Revision ID: c8f05c8be613
Revises: d9846044767e
Create Date: 2026-03-06 10:59:35.393632

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c8f05c8be613'
down_revision: Union[str, Sequence[str], None] = 'd9846044767e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():

    op.add_column(
        'mfm_log_master_dkn',
        sa.Column('ms_logbook_id', sa.Integer(), nullable=True)
    )

    op.add_column(
        'mfm_log_master_dkn_history',
        sa.Column('ms_logbook_id', sa.Integer(), nullable=True)
    )

    op.add_column(
        'tank_dip_memo',
        sa.Column('ms_logbook_id', sa.Integer(), nullable=True)
    )

    op.add_column(
        'tank_dip_memo_history',
        sa.Column('ms_logbook_id', sa.Integer(), nullable=True)
    )


def downgrade():

    op.drop_column('mfm_log_master_dkn', 'ms_logbook_id')
    op.drop_column('mfm_log_master_dkn_history', 'ms_logbook_id')
    op.drop_column('tank_dip_memo', 'ms_logbook_id')
    op.drop_column('tank_dip_memo_history', 'ms_logbook_id')
