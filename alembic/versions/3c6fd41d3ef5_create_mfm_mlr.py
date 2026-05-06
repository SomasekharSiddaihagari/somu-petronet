"""create mfm mlr

Revision ID: 3c6fd41d3ef5
Revises: 3d2d7b6b56d5
Create Date: 2026-01-22 15:43:38.857973

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3c6fd41d3ef5'
down_revision: Union[str, Sequence[str], None] = '3d2d7b6b56d5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

from alembic import op
import sqlalchemy as sa


def upgrade():

    # =========================
    # ERV MLR MASTER TWO
    # =========================
    op.create_table(
        "mfm_log_mlr_master_two",
        sa.Column("mfm_log_mlr_two_id", sa.Integer, primary_key=True, autoincrement=True),

        sa.Column("station", sa.String(50), nullable=False),
        sa.Column("station_in_charge", sa.String(100)),
        sa.Column("shift", sa.String(20)),
        sa.Column("start_time", sa.Time),
        sa.Column("log_date", sa.Date),

        sa.Column("mrpl_qc_den_15c", sa.String(50)),
        sa.Column("flash_point_fbp", sa.String(50)),
        sa.Column("kv", sa.String(50)),

        sa.Column("ci", sa.String(50)),
        sa.Column("ron_no", sa.String(50)),
        sa.Column("cn", sa.String(50)),

        sa.Column("mainline_pump_no", sa.String(50)),
        sa.Column("booster_pump", sa.String(50)),

        sa.Column("total_sulphur", sa.String(50)),

        sa.Column("created_at", sa.DateTime, server_default=sa.func.now()),
    )

    op.create_table(
        "mfm_log_mlr_master_two_history",
        sa.Column("history_id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("mfm_log_mlr_two_id", sa.Integer, nullable=False),

        sa.Column("station", sa.String(50), nullable=False),
        sa.Column("station_in_charge", sa.String(100)),
        sa.Column("shift", sa.String(20)),
        sa.Column("start_time", sa.Time),
        sa.Column("log_date", sa.Date),

        sa.Column("mrpl_qc_den_15c", sa.String(50)),
        sa.Column("flash_point_fbp", sa.String(50)),
        sa.Column("kv", sa.String(50)),

        sa.Column("ci", sa.String(50)),
        sa.Column("ron_no", sa.String(50)),
        sa.Column("cn", sa.String(50)),

        sa.Column("mainline_pump_no", sa.String(50)),
        sa.Column("booster_pump", sa.String(50)),

        sa.Column("total_sulphur", sa.String(50)),

        sa.Column("created_at", sa.DateTime, server_default=sa.func.now()),
    )

    # =========================
    # ERV MLR ENTRY TWO
    # =========================
    op.create_table(
        "mfm_log_mlr_two_entry",
        sa.Column("mfm_log_mlr_two_entry_id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column(
            "master_id",
            sa.Integer,
            sa.ForeignKey("mfm_log_mlr_master_two.mfm_log_mlr_two_id"),
            nullable=False
        ),

        sa.Column("entry_date", sa.Date),
        sa.Column("entry_time", sa.Time),

        sa.Column("pump_disch_hdr_press_1108", sa.String(50)),
        sa.Column("pump_inlet_press_1104", sa.String(50)),
        sa.Column("press_after_pcv_1110", sa.String(50)),
        sa.Column("pcv_open_percent", sa.String(50)),

        sa.Column("water_temp", sa.String(50)),

        sa.Column("mtr_de_nde_casing_temp_1", sa.String(50)),
        sa.Column("pump_de_nde_vibration_1", sa.String(50)),
        sa.Column("thrust_brg_xy", sa.String(50)),

        sa.Column("water_temp_2", sa.String(50)),

        sa.Column("mtr_de_nde_casing_temp_2", sa.String(50)),
        sa.Column("pump_de_vibration_xy", sa.String(50)),

        sa.Column("created_at", sa.DateTime, server_default=sa.func.now()),
    )

    op.create_table(
        "mfm_log_mlr_entry_two_history",
        sa.Column("history_id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("mfm_log_mlr_two_entry_id", sa.Integer),
        sa.Column("master_id", sa.Integer, nullable=False),

        sa.Column("entry_date", sa.Date),
        sa.Column("entry_time", sa.Time),

        sa.Column("pump_disch_hdr_press_1108", sa.String(50)),
        sa.Column("pump_inlet_press_1104", sa.String(50)),
        sa.Column("press_after_pcv_1110", sa.String(50)),
        sa.Column("pcv_open_percent", sa.String(50)),

        sa.Column("water_temp", sa.String(50)),

        sa.Column("mtr_de_nde_casing_temp_1", sa.String(50)),
        sa.Column("pump_de_nde_vibration_1", sa.String(50)),
        sa.Column("thrust_brg_xy", sa.String(50)),

        sa.Column("water_temp_2", sa.String(50)),

        sa.Column("mtr_de_nde_casing_temp_2", sa.String(50)),
        sa.Column("pump_de_vibration_xy", sa.String(50)),

        sa.Column("created_at", sa.DateTime, server_default=sa.func.now()),
    )

    # =========================
    # MFM MLR MASTER
    # =========================
    op.create_table(
        "mfm_log_mlr_master",
        sa.Column("mfm_log_mlr_id", sa.Integer, primary_key=True, autoincrement=True),

        sa.Column("station", sa.String(50), nullable=False),
        sa.Column("station_in_charge", sa.String(100)),
        sa.Column("shift", sa.String(20)),
        sa.Column("start_time", sa.Time),
        sa.Column("log_date", sa.Date),

        sa.Column("tank_no", sa.String(50)),
        sa.Column("hpcl_batch_no", sa.String(50)),
        sa.Column("mrpl_batch_no", sa.String(50)),
        sa.Column("pmhbl_batch_no", sa.String(50)),

        sa.Column("product_name", sa.String(100)),
        sa.Column("cycle_no", sa.String(50)),
        sa.Column("tank_temp", sa.String(50)),
        sa.Column("tank_factor", sa.String(50)),

        sa.Column("flow_meter", sa.String(50)),

        sa.Column("created_at", sa.DateTime, server_default=sa.func.now()),
    )

    op.create_table(
        "mfm_log_mlr_master_history",
        sa.Column("history_id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("mfm_log_mlr_id", sa.Integer),

        sa.Column("station", sa.String(50), nullable=False),
        sa.Column("station_in_charge", sa.String(100)),
        sa.Column("shift", sa.String(20)),
        sa.Column("start_time", sa.Time),
        sa.Column("log_date", sa.Date),

        sa.Column("tank_no", sa.String(50)),
        sa.Column("hpcl_batch_no", sa.String(50)),
        sa.Column("mrpl_batch_no", sa.String(50)),
        sa.Column("pmhbl_batch_no", sa.String(50)),

        sa.Column("product_name", sa.String(100)),
        sa.Column("cycle_no", sa.String(50)),
        sa.Column("tank_temp", sa.String(50)),
        sa.Column("tank_factor", sa.String(50)),

        sa.Column("flow_meter", sa.String(50)),

        sa.Column("created_at", sa.DateTime, server_default=sa.func.now()),
    )

    # =========================
    # MFM MLR ENTRY
    # =========================
    op.create_table(
        "mfm_log_mlr_entry",
        sa.Column("mfm_log_mlr_entry_id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column(
            "master_id",
            sa.Integer,
            sa.ForeignKey("mfm_log_mlr_master.mfm_log_mlr_id"),
            nullable=False
        ),

        sa.Column("entry_date", sa.Date),
        sa.Column("entry_time", sa.Time),

        sa.Column("mrpl_dip", sa.String(50)),

        sa.Column("gross", sa.String(50)),
        sa.Column("net", sa.String(50)),
        sa.Column("mt", sa.String(50)),
        sa.Column("den_at_nat", sa.String(50)),
        sa.Column("temperature", sa.String(50)),
        sa.Column("den_at_15_deg", sa.String(50)),

        sa.Column("mrpl_atg", sa.String(50)),
        sa.Column("mrpl_mfm", sa.String(50)),

        sa.Column("mrpl_atg_flow", sa.String(50)),
        sa.Column("mrpl_mfm_flow", sa.String(50)),

        sa.Column("diff_in_percent", sa.String(50)),

        sa.Column("created_at", sa.DateTime, server_default=sa.func.now()),
    )

    op.create_table(
        "mfm_log_mlr_entry_history",
        sa.Column("history_id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("mfm_log_mlr_entry_id", sa.Integer),
        sa.Column("master_id", sa.Integer, nullable=False),

        sa.Column("entry_date", sa.Date),
        sa.Column("entry_time", sa.Time),

        sa.Column("mrpl_dip", sa.String(50)),

        sa.Column("gross", sa.String(50)),
        sa.Column("net", sa.String(50)),
        sa.Column("mt", sa.String(50)),
        sa.Column("den_at_nat", sa.String(50)),
        sa.Column("temperature", sa.String(50)),
        sa.Column("den_at_15_deg", sa.String(50)),

        sa.Column("mrpl_atg", sa.String(50)),
        sa.Column("mrpl_mfm", sa.String(50)),

        sa.Column("mrpl_atg_flow", sa.String(50)),
        sa.Column("mrpl_mfm_flow", sa.String(50)),

        sa.Column("diff_in_percent", sa.String(50)),

        sa.Column("created_at", sa.DateTime, server_default=sa.func.now()),
    )
