"""create mfm dkn

Revision ID: 3d2d7b6b56d5
Revises: c52cfa610fa0
Create Date: 2026-01-22 15:05:09.227775

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3d2d7b6b56d5'
down_revision: Union[str, Sequence[str], None] = 'c52cfa610fa0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None



from alembic import op
import sqlalchemy as sa


def upgrade():

    # =========================
    # MFM LOG MASTER
    # =========================
    op.create_table(
        "mfm_log_master_dkn",
        sa.Column("mfm_log_dkn_id", sa.Integer, primary_key=True, autoincrement=True),

        sa.Column("station", sa.String(50)),
        sa.Column("station_in_charge", sa.String(100)),
        sa.Column("document_no", sa.String(100)),
        sa.Column("shift", sa.String(10)),
        sa.Column("start_time", sa.Time),
        sa.Column("log_date", sa.Date),
        sa.Column("status", sa.String(20)),

        sa.Column("shift_a_tank_taken_over", sa.String(100)),
        sa.Column("shift_a_tank_handed_over", sa.String(100)),
        sa.Column("shift_b_tank_taken_over", sa.String(100)),
        sa.Column("shift_b_tank_handed_over", sa.String(100)),
        sa.Column("shift_c_tank_taken_over", sa.String(100)),
        sa.Column("shift_c_tank_handed_over", sa.String(100)),

        sa.Column("qty_pumped_from_mangalore", sa.Float),
        sa.Column("receipt_at_hassan", sa.Float),
        sa.Column("receipt_at_bangalore", sa.Float),

        sa.Column("qty_available_interface_tank_101", sa.Float),
        sa.Column("qty_available_interface_tank_102", sa.Float),
        sa.Column("loss_gain_101", sa.Float),
        sa.Column("loss_gain_102", sa.Float),

        sa.Column("qty_pumped_last_24hrs", sa.Float),
        sa.Column("qty_pumped_pl_t", sa.Float),
        sa.Column("qty_pumped_month", sa.Float),
        sa.Column("qty_pumped_year", sa.Float),

        sa.Column("euro_hsd", sa.Float),
        sa.Column("bsv_hsd", sa.Float),
        sa.Column("sk_o", sa.Float),
        sa.Column("ms", sa.Float),
        sa.Column("total_product", sa.Float),

        sa.Column("hrs_operation_last_24hrs", sa.Float),
        sa.Column("hrs_operation_month", sa.Float),
        sa.Column("hrs_operation_year", sa.Float),

        sa.Column("sump_tank_dip_0700hrs", sa.Float),
        sa.Column("diesel_dg_tank", sa.Float),
        sa.Column("diesel_dg_set_tank", sa.Float),
        sa.Column("diesel_ffdu_3_ser_tank", sa.Float),
        sa.Column("diesel_ffdu_4_ser_tank", sa.Float),
        sa.Column("diesel_ffdu_5_ser_tank", sa.Float),

        sa.Column("remarks", sa.Text),
        sa.Column("created_at", sa.DateTime, server_default=sa.func.now()),
    )

    op.create_table(
        "mfm_log_master_dkn_history",
        sa.Column("history_id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("mfm_log_dkn_id", sa.Integer),

        sa.Column("station", sa.String(50)),
        sa.Column("station_in_charge", sa.String(100)),
        sa.Column("document_no", sa.String(100)),
        sa.Column("shift", sa.String(10)),
        sa.Column("start_time", sa.Time),
        sa.Column("log_date", sa.Date),
        sa.Column("status", sa.String(20)),

        sa.Column("shift_a_tank_taken_over", sa.String(100)),
        sa.Column("shift_a_tank_handed_over", sa.String(100)),
        sa.Column("shift_b_tank_taken_over", sa.String(100)),
        sa.Column("shift_b_tank_handed_over", sa.String(100)),
        sa.Column("shift_c_tank_taken_over", sa.String(100)),
        sa.Column("shift_c_tank_handed_over", sa.String(100)),

        sa.Column("qty_pumped_from_mangalore", sa.Float),
        sa.Column("receipt_at_hassan", sa.Float),
        sa.Column("receipt_at_bangalore", sa.Float),

        sa.Column("qty_available_interface_tank_101", sa.Float),
        sa.Column("qty_available_interface_tank_102", sa.Float),
        sa.Column("loss_gain_101", sa.Float),
        sa.Column("loss_gain_102", sa.Float),

        sa.Column("qty_pumped_last_24hrs", sa.Float),
        sa.Column("qty_pumped_pl_t", sa.Float),
        sa.Column("qty_pumped_month", sa.Float),
        sa.Column("qty_pumped_year", sa.Float),

        sa.Column("euro_hsd", sa.Float),
        sa.Column("bsv_hsd", sa.Float),
        sa.Column("sk_o", sa.Float),
        sa.Column("ms", sa.Float),
        sa.Column("total_product", sa.Float),

        sa.Column("hrs_operation_last_24hrs", sa.Float),
        sa.Column("hrs_operation_month", sa.Float),
        sa.Column("hrs_operation_year", sa.Float),

        sa.Column("sump_tank_dip_0700hrs", sa.Float),
        sa.Column("diesel_dg_tank", sa.Float),
        sa.Column("diesel_dg_set_tank", sa.Float),
        sa.Column("diesel_ffdu_3_ser_tank", sa.Float),
        sa.Column("diesel_ffdu_4_ser_tank", sa.Float),
        sa.Column("diesel_ffdu_5_ser_tank", sa.Float),

        sa.Column("remarks", sa.Text),
        sa.Column("created_at", sa.DateTime, server_default=sa.func.now()),
    )

    # =========================
    # MFM LOG ENTRY
    # =========================
    op.create_table(
        "mfm_log_entry_dkn",
        sa.Column("mfm_log_dsk_id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("master_id", sa.Integer, sa.ForeignKey("mfm_log_master_dkn.mfm_log_dkn_id")),

        sa.Column("entry_time", sa.Time),

        sa.Column("mainline_density", sa.Float),
        sa.Column("mainline_temp", sa.Float),
        sa.Column("sampling_density", sa.Float),
        sa.Column("sampling_temp", sa.Float),

        sa.Column("manifold_density", sa.Float),
        sa.Column("manifold_temp", sa.Float),
        sa.Column("corresponding_density", sa.Float),

        sa.Column("receiving_tank_no", sa.String(50)),
        sa.Column("tank_dip", sa.Float),
        sa.Column("tank_quantity", sa.Float),

        sa.Column("flow_gross", sa.Float),
        sa.Column("flow_net", sa.Float),
        sa.Column("flow_mass", sa.Float),

        sa.Column("delivered_fc_klhr", sa.Float),
        sa.Column("delivered_fc_cumu", sa.Float),
        sa.Column("delivered_qd_klhr", sa.Float),
        sa.Column("delivered_qd_cumu", sa.Float),

        sa.Column("delivered_tank_dip", sa.Float),

        sa.Column("remarks", sa.Text),
        sa.Column("created_at", sa.DateTime, server_default=sa.func.now()),
    )

    op.create_table(
        "mfm_log_entry_dkn_history",
        sa.Column("history_id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("mfm_log_dsk_id", sa.Integer),
        sa.Column("master_id", sa.Integer),

        sa.Column("entry_time", sa.Time),

        sa.Column("mainline_density", sa.Float),
        sa.Column("mainline_temp", sa.Float),
        sa.Column("sampling_density", sa.Float),
        sa.Column("sampling_temp", sa.Float),

        sa.Column("manifold_density", sa.Float),
        sa.Column("manifold_temp", sa.Float),
        sa.Column("corresponding_density", sa.Float),

        sa.Column("receiving_tank_no", sa.String(50)),
        sa.Column("tank_dip", sa.Float),
        sa.Column("tank_quantity", sa.Float),

        sa.Column("flow_gross", sa.Float),
        sa.Column("flow_net", sa.Float),
        sa.Column("flow_mass", sa.Float),

        sa.Column("delivered_fc_klhr", sa.Float),
        sa.Column("delivered_fc_cumu", sa.Float),
        sa.Column("delivered_qd_klhr", sa.Float),
        sa.Column("delivered_qd_cumu", sa.Float),

        sa.Column("delivered_tank_dip", sa.Float),

        sa.Column("remarks", sa.Text),
        sa.Column("created_at", sa.DateTime, server_default=sa.func.now()),
    )

    # =========================
    # MFM SHUTDOWN DETAIL
    # =========================
    op.create_table(
        "mfm_shutdown_detail_dkn",
        sa.Column("mfm_shutdown_id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("master_id", sa.Integer, sa.ForeignKey("mfm_log_master_dkn.mfm_log_dkn_id")),

        sa.Column("from_time", sa.Time),
        sa.Column("to_time", sa.Time),
        sa.Column("reason", sa.Text),

        sa.Column("kwh", sa.Float),
        sa.Column("kvah", sa.Float),
        sa.Column("pf", sa.Float),

        sa.Column("psd_time_from", sa.Time),
        sa.Column("psd_time_to", sa.Time),
        sa.Column("psd_cul_daily", sa.Float),
        sa.Column("psd_cul_monthly", sa.Float),

        sa.Column("dg_from", sa.Time),
        sa.Column("dg_to", sa.Time),

        sa.Column("engery_meter_reading", sa.Float),
        sa.Column("hours_meter", sa.Float),

        sa.Column("tank1", sa.Float),
        sa.Column("tank2", sa.Float),
        sa.Column("tank3", sa.Float),

        sa.Column("fw1", sa.Float),
        sa.Column("fw2", sa.Float),
        sa.Column("fw3", sa.Float),
        sa.Column("fw4", sa.Float),
        sa.Column("fw5", sa.Float),

        sa.Column("prevcumrunhour", sa.Integer),
        sa.Column("cummrunhour", sa.Integer),

        sa.Column("remarks", sa.Text),
        sa.Column("created_at", sa.DateTime, server_default=sa.func.now()),
    )

    op.create_table(
        "mfm_shutdown_detail_dkn_history",
        sa.Column("history_id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("mfm_shutdown_id", sa.Integer),
        sa.Column("master_id", sa.Integer),

        sa.Column("from_time", sa.Time),
        sa.Column("to_time", sa.Time),
        sa.Column("reason", sa.Text),

        sa.Column("kwh", sa.Float),
        sa.Column("kvah", sa.Float),
        sa.Column("pf", sa.Float),

        sa.Column("psd_time_from", sa.Time),
        sa.Column("psd_time_to", sa.Time),
        sa.Column("psd_cul_daily", sa.Float),
        sa.Column("psd_cul_monthly", sa.Float),

        sa.Column("dg_from", sa.Time),
        sa.Column("dg_to", sa.Time),

        sa.Column("engery_meter_reading", sa.Float),
        sa.Column("hours_meter", sa.Float),

        sa.Column("tank1", sa.Float),
        sa.Column("tank2", sa.Float),
        sa.Column("tank3", sa.Float),

        sa.Column("fw1", sa.Float),
        sa.Column("fw2", sa.Float),
        sa.Column("fw3", sa.Float),
        sa.Column("fw4", sa.Float),
        sa.Column("fw5", sa.Float),

        sa.Column("prevcumrunhour", sa.Integer),
        sa.Column("cummrunhour", sa.Integer),

        sa.Column("remarks", sa.Text),
        sa.Column("created_at", sa.DateTime, server_default=sa.func.now()),
    )

    # =========================
    # MFM PLT DETAIL
    # =========================
    op.create_table(
        "mfm_plt_detail_dkn",
        sa.Column("mfm_plt_dkn_id", sa.Integer, primary_key=True),
        sa.Column("master_id", sa.Integer, sa.ForeignKey("mfm_log_master_dkn.mfm_log_dkn_id")),

        sa.Column("plt_sd_start_time", sa.Time),
        sa.Column("plt_sd_end_time", sa.Time),

        sa.Column("omc_with_tank_no", sa.String(50)),
        sa.Column("start_time", sa.Time),
        sa.Column("stop_time", sa.Time),

        sa.Column("opening_dip", sa.Float),
        sa.Column("opening_qty", sa.Float),

        sa.Column("closing_dip", sa.Float),
        sa.Column("closing_qty", sa.Float),

        sa.Column("fmr_opening_net", sa.Float),
        sa.Column("fmr_opening_gross", sa.Float),
        sa.Column("fmr_opening_mass", sa.Float),

        sa.Column("fmr_closing_net", sa.Float),
        sa.Column("fmr_closing_gross", sa.Float),
        sa.Column("fmr_closing_mass", sa.Float),

        sa.Column("qty_as_per_dip", sa.Float),
        sa.Column("qty_as_per_fmr", sa.Float),

        sa.Column("remarks", sa.Text),
        sa.Column("created_at", sa.DateTime, server_default=sa.func.now()),
    )

    op.create_table(
        "mfm_plt_detail_dkn_history",
        sa.Column("history_id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("mfm_plt_dkn_id", sa.Integer),
        sa.Column("master_id", sa.Integer),

        sa.Column("plt_start_time", sa.Time),
        sa.Column("plt_end_time", sa.Time),

        sa.Column("omc_with_tank_no", sa.String(50)),
        sa.Column("start_time", sa.Time),
        sa.Column("stop_time", sa.Time),

        sa.Column("opening_dip", sa.Float),
        sa.Column("opening_qty", sa.Float),

        sa.Column("closing_dip", sa.Float),
        sa.Column("closing_qty", sa.Float),

        sa.Column("fmr_opening_net", sa.Float),
        sa.Column("fmr_opening_gross", sa.Float),
        sa.Column("fmr_opening_mass", sa.Float),

        sa.Column("fmr_closing_net", sa.Float),
        sa.Column("fmr_closing_gross", sa.Float),
        sa.Column("fmr_closing_mass", sa.Float),

        sa.Column("qty_as_per_dip", sa.Float),
        sa.Column("qty_as_per_fmr", sa.Float),

        sa.Column("remarks", sa.Text),
        sa.Column("created_at", sa.DateTime, server_default=sa.func.now()),
    )
