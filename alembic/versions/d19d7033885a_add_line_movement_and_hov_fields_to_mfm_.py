"""add line movement and hov fields to mfm accounting tables

Revision ID: d19d7033885a
Revises: 0a286c4c2194
Create Date: 2026-03-24 10:29:52.912067

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd19d7033885a'
down_revision: Union[str, Sequence[str], None] = '0a286c4c2194'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade():
    tables = ["mfm_accounting_dkn", "mfm_accounting_dkn_history"]

    for table in tables:
        op.add_column(table, sa.Column("hpcl_hsd_line_mov_seal", sa.String(), nullable=True))
        op.add_column(table, sa.Column("hpcl_hsd_line_mov_status", sa.String(), nullable=True))
        op.add_column(table, sa.Column("bpcl_hsd_line_mov_seal", sa.String(), nullable=True))
        op.add_column(table, sa.Column("bpcl_hsd_line_mov_status", sa.String(), nullable=True))
        op.add_column(table, sa.Column("iocl_hsd_line_mov_seal", sa.String(), nullable=True))
        op.add_column(table, sa.Column("iocl_hsd_line_mov_status", sa.String(), nullable=True))

        op.add_column(table, sa.Column("hpcl_hsd_line_hov_seal", sa.String(), nullable=True))
        op.add_column(table, sa.Column("hpcl_hsd_line_hov_status", sa.String(), nullable=True))
        op.add_column(table, sa.Column("bpcl_hsd_line_hov_seal", sa.String(), nullable=True))
        op.add_column(table, sa.Column("bpcl_hsd_line_hov_status", sa.String(), nullable=True))
        op.add_column(table, sa.Column("iocl_hsd_line_hov_seal", sa.String(), nullable=True))
        op.add_column(table, sa.Column("iocl_hsd_line_hov_status", sa.String(), nullable=True))

        op.add_column(table, sa.Column("mrpl_hsd_line_mov_seal", sa.String(), nullable=True))
        op.add_column(table, sa.Column("mrpl_hsd_line_mov_status", sa.String(), nullable=True))

        op.add_column(table, sa.Column("if_tank_101_mov_seal", sa.String(), nullable=True))
        op.add_column(table, sa.Column("if_tank_101_mov_status", sa.String(), nullable=True))
        op.add_column(table, sa.Column("if_tank_102_mov_seal", sa.String(), nullable=True))
        op.add_column(table, sa.Column("if_tank_102_mov_status", sa.String(), nullable=True))

        op.add_column(table, sa.Column("ms_header_line_mov_1415_seal", sa.String(), nullable=True))
        op.add_column(table, sa.Column("ms_header_line_mov_1415_status", sa.String(), nullable=True))
        op.add_column(table, sa.Column("ms_header_line_mov_1416_seal", sa.String(), nullable=True))
        op.add_column(table, sa.Column("ms_header_line_mov_1416_status", sa.String(), nullable=True))

        op.add_column(table, sa.Column("mrpl_hsd_dbvb_mov_seal", sa.String(), nullable=True))
        op.add_column(table, sa.Column("mrpl_hsd_dbvb_mov_status", sa.String(), nullable=True))


def downgrade():
    tables = ["mfm_accounting_dkn", "mfm_accounting_dkn_history"]

    for table in tables:
        op.drop_column(table, "hpcl_hsd_line_mov_seal")
        op.drop_column(table, "hpcl_hsd_line_mov_status")
        op.drop_column(table, "bpcl_hsd_line_mov_seal")
        op.drop_column(table, "bpcl_hsd_line_mov_status")
        op.drop_column(table, "iocl_hsd_line_mov_seal")
        op.drop_column(table, "iocl_hsd_line_mov_status")

        op.drop_column(table, "hpcl_hsd_line_hov_seal")
        op.drop_column(table, "hpcl_hsd_line_hov_status")
        op.drop_column(table, "bpcl_hsd_line_hov_seal")
        op.drop_column(table, "bpcl_hsd_line_hov_status")
        op.drop_column(table, "iocl_hsd_line_hov_seal")
        op.drop_column(table, "iocl_hsd_line_hov_status")

        op.drop_column(table, "mrpl_hsd_line_mov_seal")
        op.drop_column(table, "mrpl_hsd_line_mov_status")

        op.drop_column(table, "if_tank_101_mov_seal")
        op.drop_column(table, "if_tank_101_mov_status")
        op.drop_column(table, "if_tank_102_mov_seal")
        op.drop_column(table, "if_tank_102_mov_status")

        op.drop_column(table, "ms_header_line_mov_1415_seal")
        op.drop_column(table, "ms_header_line_mov_1415_status")
        op.drop_column(table, "ms_header_line_mov_1416_seal")
        op.drop_column(table, "ms_header_line_mov_1416_status")

        op.drop_column(table, "mrpl_hsd_dbvb_mov_seal")
        op.drop_column(table, "mrpl_hsd_dbvb_mov_status")