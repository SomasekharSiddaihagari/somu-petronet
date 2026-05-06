"""add ms_logbook_id to kptcl tables

Revision ID: 516db58a3996
Revises: abed2f413369
Create Date: 2026-03-12 11:37:44.588891

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '516db58a3996'
down_revision: Union[str, Sequence[str], None] = 'abed2f413369'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column('kptcl_dkn_master', sa.Column('ms_logbook_id', sa.Integer(), nullable=True))
    op.add_column('kptcl_dkn_master_history', sa.Column('ms_logbook_id', sa.Integer(), nullable=True))

    op.add_column('kptcl_hsn_master', sa.Column('ms_logbook_id', sa.Integer(), nullable=True))
    op.add_column('kptcl_hsn_master_history', sa.Column('ms_logbook_id', sa.Integer(), nullable=True))

    op.add_column('kptcl_ner_master', sa.Column('ms_logbook_id', sa.Integer(), nullable=True))
    op.add_column('kptcl_ner_master_history', sa.Column('ms_logbook_id', sa.Integer(), nullable=True))


def downgrade():
    op.drop_column('kptcl_dkn_master', 'ms_logbook_id')
    op.drop_column('kptcl_dkn_master_history', 'ms_logbook_id')

    op.drop_column('kptcl_hsn_master', 'ms_logbook_id')
    op.drop_column('kptcl_hsn_master_history', 'ms_logbook_id')

    op.drop_column('kptcl_ner_master', 'ms_logbook_id')
    op.drop_column('kptcl_ner_master_history', 'ms_logbook_id')