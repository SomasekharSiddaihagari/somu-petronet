"""create cp reading ner entry and history tables

Revision ID: 7c36572b8e25
Revises: 858852c36d0b
Create Date: 2026-01-21 19:49:21.603126

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7c36572b8e25'
down_revision: Union[str, Sequence[str], None] = '858852c36d0b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade():

    # =====================================================
    # cp_reading_ner_entry
    # =====================================================
    op.create_table(
        "cp_reading_ner_entry",
        sa.Column("cp_ner_entry_id", sa.Integer, primary_key=True, autoincrement=True),

        sa.Column(
            "master_id",
            sa.Integer,
            sa.ForeignKey(
                "cp_reading_ner_master.cp_ner_id",
                ondelete="CASCADE"
            ),
        ),

        sa.Column("sr_no", sa.Integer),
        sa.Column("entry_date", sa.Date),
        sa.Column("entry_time", sa.Time),
        sa.Column("remarks", sa.String(255)),

        # -------- DKN --------
        sa.Column("dkn_ac_ip_v", sa.String(20)),
        sa.Column("dkn_psp_ve", sa.String(20)),
        sa.Column("dkn_ac_ip_amp", sa.String(20)),
        sa.Column("dkn_op_dc_v", sa.String(20)),
        sa.Column("dkn_op_dc_amp", sa.String(20)),

        # -------- SVS --------
        sa.Column("svs_ac_ip_v", sa.String(20)),
        sa.Column("svs_psp_ve", sa.String(20)),
        sa.Column("svs_ac_ip_amp", sa.String(20)),
        sa.Column("svs_op_dc_v", sa.String(20)),
        sa.Column("svs_op_dc_amp", sa.String(20)),

        # -------- IP STN --------
        sa.Column("ip_stn_ac_ip_v", sa.String(20)),
        sa.Column("ip_stn_psp_ve", sa.String(20)),
        sa.Column("ip_stn_ac_ip_amp", sa.String(20)),
        sa.Column("ip_stn_op_dc_v", sa.String(20)),
        sa.Column("ip_stn_op_dc_amp", sa.String(20)),

        # -------- SV-9 --------
        sa.Column("sv9_ac_ip_v", sa.String(20)),
        sa.Column("sv9_psp_ve", sa.String(20)),
        sa.Column("sv9_ac_ip_amp", sa.String(20)),
        sa.Column("sv9_op_dc_v", sa.String(20)),
        sa.Column("sv9_op_dc_amp", sa.String(20)),

        # -------- SV-10 --------
        sa.Column("sv10_ac_ip_v", sa.String(20)),
        sa.Column("sv10_psp_ve", sa.String(20)),
        sa.Column("sv10_ac_ip_amp", sa.String(20)),
        sa.Column("sv10_op_dc_v", sa.String(20)),
        sa.Column("sv10_op_dc_amp", sa.String(20)),

        sa.Column("created_at", sa.DateTime, server_default=sa.func.now()),
    )

    # =====================================================
    # cp_reading_ner_entry_history
    # =====================================================
    op.create_table(
        "cp_reading_ner_entry_history",
        sa.Column("history_id", sa.Integer, primary_key=True, autoincrement=True),

        sa.Column("cp_ner_entry_id", sa.Integer),
        sa.Column("master_id", sa.Integer),
        sa.Column("sr_no", sa.Integer),

        sa.Column("entry_date", sa.Date),
        sa.Column("entry_time", sa.Time),
        sa.Column("remarks", sa.String(255)),

        sa.Column("dkn_ac_ip_v", sa.String(20)),
        sa.Column("dkn_psp_ve", sa.String(20)),
        sa.Column("dkn_ac_ip_amp", sa.String(20)),
        sa.Column("dkn_op_dc_v", sa.String(20)),
        sa.Column("dkn_op_dc_amp", sa.String(20)),

        sa.Column("svs_ac_ip_v", sa.String(20)),
        sa.Column("svs_psp_ve", sa.String(20)),
        sa.Column("svs_ac_ip_amp", sa.String(20)),
        sa.Column("svs_op_dc_v", sa.String(20)),
        sa.Column("svs_op_dc_amp", sa.String(20)),

        sa.Column("ip_stn_ac_ip_v", sa.String(20)),
        sa.Column("ip_stn_psp_ve", sa.String(20)),
        sa.Column("ip_stn_ac_ip_amp", sa.String(20)),
        sa.Column("ip_stn_op_dc_v", sa.String(20)),
        sa.Column("ip_stn_op_dc_amp", sa.String(20)),

        sa.Column("sv9_ac_ip_v", sa.String(20)),
        sa.Column("sv9_psp_ve", sa.String(20)),
        sa.Column("sv9_ac_ip_amp", sa.String(20)),
        sa.Column("sv9_op_dc_v", sa.String(20)),
        sa.Column("sv9_op_dc_amp", sa.String(20)),

        sa.Column("sv10_ac_ip_v", sa.String(20)),
        sa.Column("sv10_psp_ve", sa.String(20)),
        sa.Column("sv10_ac_ip_amp", sa.String(20)),
        sa.Column("sv10_op_dc_v", sa.String(20)),
        sa.Column("sv10_op_dc_amp", sa.String(20)),

        sa.Column("created_at", sa.DateTime, server_default=sa.func.now()),
    )


def downgrade():
    op.drop_table("cp_reading_ner_entry_history")
    op.drop_table("cp_reading_ner_entry")