"""add logbook shift nullable columns

Revision ID: 038bdccd59fe
Revises: 0297ce46c8d4
Create Date: 2026-01-28 16:24:34.299701

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '038bdccd59fe'
down_revision: Union[str, Sequence[str], None] = '0297ce46c8d4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    tables = [
        "logbook_shift_master",
        "logbook_shift_master_history"
    ]

    for table in tables:
        op.add_column(table, sa.Column('tank_ffe_id', sa.Integer(), nullable=True))

        op.add_column(table, sa.Column('cp_dkn_id', sa.Integer(), nullable=True))
        op.add_column(table, sa.Column('cp_hsn_id', sa.Integer(), nullable=True))
        op.add_column(table, sa.Column('cp_mlr_id', sa.Integer(), nullable=True))
        op.add_column(table, sa.Column('cp_ner_id', sa.Integer(), nullable=True))

        op.add_column(table, sa.Column('dsc_id', sa.Integer(), nullable=True))
        op.add_column(table, sa.Column('sampling_id', sa.Integer(), nullable=True))
        op.add_column(table, sa.Column('dg_id', sa.Integer(), nullable=True))
        op.add_column(table, sa.Column('erv_id', sa.Integer(), nullable=True))
        op.add_column(table, sa.Column('fire_id', sa.Integer(), nullable=True))

        op.add_column(table, sa.Column('kptcl_dkn_id', sa.Integer(), nullable=True))
        op.add_column(table, sa.Column('kptcl_hsn_id', sa.Integer(), nullable=True))
        op.add_column(table, sa.Column('kptcl_ner_id', sa.Integer(), nullable=True))

        op.add_column(table, sa.Column('vtmn_id', sa.Integer(), nullable=True))
        op.add_column(table, sa.Column('vtm_id', sa.Integer(), nullable=True))

        op.add_column(table, sa.Column('tank_id', sa.Integer(), nullable=True))

        op.add_column(table, sa.Column('pressure_id', sa.Integer(), nullable=True))
        op.add_column(table, sa.Column('npt_id', sa.Integer(), nullable=True))

        op.add_column(table, sa.Column('mfm_log_dkn_id', sa.Integer(), nullable=True))
        op.add_column(table, sa.Column('mfm_log_ner_id', sa.Integer(), nullable=True))

        op.add_column(table, sa.Column('mfm_acc_hsn_id', sa.Integer(), nullable=True))
        op.add_column(table, sa.Column('mfm_acc_dkn_id', sa.Integer(), nullable=True))

        op.add_column(table, sa.Column('security_guard_id', sa.Integer(), nullable=True))


def downgrade():
    tables = [
        "logbook_shift_master",
        "logbook_shift_master_history"
    ]

    for table in tables:
        op.drop_column(table, 'security_guard_id')

        op.drop_column(table, 'mfm_acc_dkn_id')
        op.drop_column(table, 'mfm_acc_hsn_id')

        op.drop_column(table, 'mfm_log_ner_id')
        op.drop_column(table, 'mfm_log_dkn_id')

        op.drop_column(table, 'npt_id')
        op.drop_column(table, 'pressure_id')

        op.drop_column(table, 'tank_id')

        op.drop_column(table, 'vtm_id')
        op.drop_column(table, 'vtmn_id')

        op.drop_column(table, 'kptcl_ner_id')
        op.drop_column(table, 'kptcl_hsn_id')
        op.drop_column(table, 'kptcl_dkn_id')

        op.drop_column(table, 'fire_id')
        op.drop_column(table, 'erv_id')
        op.drop_column(table, 'dg_id')
        op.drop_column(table, 'sampling_id')
        op.drop_column(table, 'dsc_id')

        op.drop_column(table, 'cp_ner_id')
        op.drop_column(table, 'cp_mlr_id')
        op.drop_column(table, 'cp_hsn_id')
        op.drop_column(table, 'cp_dkn_id')

        op.drop_column(table, 'tank_ffe_id')