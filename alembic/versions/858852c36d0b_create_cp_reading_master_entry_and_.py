"""create cp reading master entry and history tables

Revision ID: 858852c36d0b
Revises: 2148ed9d7070
Create Date: 2026-01-21 19:37:00.897121

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '858852c36d0b'
down_revision: Union[str, Sequence[str], None] = '2148ed9d7070'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade():

    # =========================================================
    # MLR MASTER
    # =========================================================
    op.create_table(
        "cp_reading_mlr_master",
        sa.Column("cp_mlr_id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("station", sa.String(50)),
        sa.Column("station_in_charge", sa.String(100)),
        sa.Column("shift", sa.String(20)),
        sa.Column("start_time", sa.Time),
        sa.Column("log_date", sa.Date),
        sa.Column("status", sa.String(20)),
        sa.Column("created_at", sa.DateTime, server_default=sa.func.now()),
    )

    op.create_table(
        "cp_reading_mlr_master_history",
        sa.Column("history_id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("cp_mlr_id", sa.Integer),
        sa.Column("station", sa.String(50)),
        sa.Column("station_in_charge", sa.String(100)),
        sa.Column("shift", sa.String(20)),
        sa.Column("start_time", sa.Time),
        sa.Column("log_date", sa.Date),
        sa.Column("status", sa.String(20)),
        sa.Column("created_at", sa.DateTime, server_default=sa.func.now()),
    )

    # =========================================================
    # MLR ENTRY
    # =========================================================
    op.create_table(
        "cp_reading_mlr_entry",
        sa.Column("cp_mlr_entry_id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column(
            "master_id",
            sa.Integer,
            sa.ForeignKey("cp_reading_mlr_master.cp_mlr_id", ondelete="CASCADE"),
        ),
        sa.Column("sr_no", sa.Integer),
        sa.Column("entry_date", sa.Date),
        sa.Column("entry_time", sa.Time),
        sa.Column("remarks", sa.String(255)),

        sa.Column("ner_ac_ip_v", sa.String(20)),
        sa.Column("ner_psp_ve", sa.String(20)),
        sa.Column("ner_ac_ip_amp", sa.String(20)),
        sa.Column("ner_op_dc_v", sa.String(20)),
        sa.Column("ner_op_dc_amp", sa.String(20)),

        sa.Column("sv3_ac_ip_v", sa.String(20)),
        sa.Column("sv3_psp_ve", sa.String(20)),
        sa.Column("sv3_ac_ip_amp", sa.String(20)),
        sa.Column("sv3_op_dc_v", sa.String(20)),
        sa.Column("sv3_op_dc_amp", sa.String(20)),

        sa.Column("sv4_ac_ip_v", sa.String(20)),
        sa.Column("sv4_psp_ve", sa.String(20)),
        sa.Column("sv4_ac_ip_amp", sa.String(20)),
        sa.Column("sv4_op_dc_v", sa.String(20)),
        sa.Column("sv4_op_dc_amp", sa.String(20)),

        sa.Column("created_at", sa.DateTime, server_default=sa.func.now()),
    )

    op.create_table(
        "cp_reading_mlr_entry_history",
        sa.Column("history_id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("cp_mlr_entry_id", sa.Integer),
        sa.Column("master_id", sa.Integer),
        sa.Column("sr_no", sa.Integer),
        sa.Column("entry_date", sa.Date),
        sa.Column("entry_time", sa.Time),
        sa.Column("remarks", sa.String(255)),

        sa.Column("ner_ac_ip_v", sa.String(20)),
        sa.Column("ner_psp_ve", sa.String(20)),
        sa.Column("ner_ac_ip_amp", sa.String(20)),
        sa.Column("ner_op_dc_v", sa.String(20)),
        sa.Column("ner_op_dc_amp", sa.String(20)),

        sa.Column("sv3_ac_ip_v", sa.String(20)),
        sa.Column("sv3_psp_ve", sa.String(20)),
        sa.Column("sv3_ac_ip_amp", sa.String(20)),
        sa.Column("sv3_op_dc_v", sa.String(20)),
        sa.Column("sv3_op_dc_amp", sa.String(20)),

        sa.Column("sv4_ac_ip_v", sa.String(20)),
        sa.Column("sv4_psp_ve", sa.String(20)),
        sa.Column("sv4_ac_ip_amp", sa.String(20)),
        sa.Column("sv4_op_dc_v", sa.String(20)),
        sa.Column("sv4_op_dc_amp", sa.String(20)),

        sa.Column("created_at", sa.DateTime, server_default=sa.func.now()),
    )

    # =========================================================
    # HSN MASTER / ENTRY
    # =========================================================
    op.create_table(
        "cp_reading_hsn_master",
        sa.Column("cp_hsn_id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("station", sa.String(50)),
        sa.Column("station_in_charge", sa.String(100)),
        sa.Column("shift", sa.String(20)),
        sa.Column("start_time", sa.Time),
        sa.Column("log_date", sa.Date),
        sa.Column("status", sa.String(20)),
        sa.Column("created_at", sa.DateTime, server_default=sa.func.now()),
    )

    op.create_table(
        "cp_reading_hsn_master_history",
        sa.Column("history_id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("cp_hsn_id", sa.Integer),
        sa.Column("station", sa.String(50)),
        sa.Column("station_in_charge", sa.String(100)),
        sa.Column("shift", sa.String(20)),
        sa.Column("start_time", sa.Time),
        sa.Column("log_date", sa.Date),
        sa.Column("status", sa.String(20)),
        sa.Column("created_at", sa.DateTime, server_default=sa.func.now()),
    )

    # =========================================================
    # DKN MASTER / ENTRY
    # =========================================================
    op.create_table(
        "cp_reading_dkn_master",
        sa.Column("cp_dkn_id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("station", sa.String(50)),
        sa.Column("station_in_charge", sa.String(100)),
        sa.Column("shift", sa.String(20)),
        sa.Column("start_time", sa.Time),
        sa.Column("log_date", sa.Date),
        sa.Column("status", sa.String(20)),
        sa.Column("created_at", sa.DateTime, server_default=sa.func.now()),
    )

    op.create_table(
        "cp_reading_dkn_master_history",
        sa.Column("history_id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("cp_dkn_id", sa.Integer),
        sa.Column("station", sa.String(50)),
        sa.Column("station_in_charge", sa.String(100)),
        sa.Column("shift", sa.String(20)),
        sa.Column("start_time", sa.Time),
        sa.Column("log_date", sa.Date),
        sa.Column("status", sa.String(20)),
        sa.Column("created_at", sa.DateTime, server_default=sa.func.now()),
    )

    # =========================================================
    # NER MASTER
    # =========================================================
    op.create_table(
        "cp_reading_ner_master",
        sa.Column("cp_ner_id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("document_number", sa.String(100)),
        sa.Column("station", sa.String(50)),
        sa.Column("station_in_charge", sa.String(100)),
        sa.Column("shift", sa.String(20)),
        sa.Column("start_time", sa.Time),
        sa.Column("log_date", sa.Date),
        sa.Column("status", sa.String(20)),
        sa.Column("created_at", sa.DateTime, server_default=sa.func.now()),
    )


def downgrade():
    op.drop_table("cp_reading_ner_master")
    op.drop_table("cp_reading_dkn_master_history")
    op.drop_table("cp_reading_dkn_master")
    op.drop_table("cp_reading_hsn_master_history")
    op.drop_table("cp_reading_hsn_master")
    op.drop_table("cp_reading_mlr_entry_history")
    op.drop_table("cp_reading_mlr_entry")
    op.drop_table("cp_reading_mlr_master_history")
    op.drop_table("cp_reading_mlr_master")