"""create mfm log ner tables

Revision ID: 172e4a6f9091
Revises: 3c6fd41d3ef5
Create Date: 2026-01-22 17:39:29.912685

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '172e4a6f9091'
down_revision: Union[str, Sequence[str], None] = '3c6fd41d3ef5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # ===============================
    # mfm_log_ner_master
    # ===============================
    op.create_table(
        "mfm_log_ner_master",
        sa.Column("mfm_log_ner_id", sa.Integer(), primary_key=True, autoincrement=True),

        sa.Column("station", sa.String(100)),
        sa.Column("station_in_charge", sa.String(100)),
        sa.Column("shift", sa.String(20)),
        sa.Column("start_time", sa.Time()),
        sa.Column("log_date", sa.Date()),

        sa.Column("psp", sa.Float()),
        sa.Column("dc_voltage_op", sa.Float()),
        sa.Column("dc_current_op", sa.Float()),

        sa.Column("cp_charger", sa.String(50)),
        sa.Column("cp_ac_ip_voltage", sa.Float()),
        sa.Column("cp_ac_ip_current", sa.Float()),
        sa.Column("cp_dc_op_voltage", sa.Float()),
        sa.Column("cp_dc_op_current", sa.Float()),
        sa.Column("cp_battery_cell_voltage", sa.Float()),
        sa.Column("cp_battery_earth_leak", sa.Float()),

        sa.Column("telecom_charger", sa.String(50)),
        sa.Column("ac_ip_voltage_telecom", sa.Float()),
        sa.Column("ac_ip_current_telecom", sa.Float()),
        sa.Column("telecom_charger_dc_op_voltage", sa.Float()),
        sa.Column("telecom_charger_dc_op_current", sa.Float()),
        sa.Column("telecom_charger_battery_cell_voltage", sa.Float()),
        sa.Column("telecom_charger_battery_earth_leak", sa.Float()),

        sa.Column("kva_dg", sa.Float()),
        sa.Column("dg_ltrs", sa.Float()),

        sa.Column("sv3_import", sa.Float()),
        sa.Column("sv3_export", sa.Float()),
        sa.Column("sv3_dg_ltrs", sa.Float()),
        sa.Column("sv3_neriya_station", sa.String(100)),
        sa.Column("sv3_kwh", sa.Float()),
        sa.Column("sv3_kvarh", sa.Float()),
        sa.Column("sv3_pf", sa.Float()),
        sa.Column("sv3_psp", sa.Float()),
        sa.Column("sv3_volt", sa.Float()),
        sa.Column("sv3_curr", sa.Float()),
        sa.Column("sv3_tc", sa.Float()),
        sa.Column("sv3_fwt_level", sa.Float()),
        sa.Column("sv3_fwt_1", sa.Float()),
        sa.Column("sv3_fwt_2", sa.Float()),
        sa.Column("sv3_dg_ltrs_2", sa.Float()),

        sa.Column("sv4_import", sa.Float()),
        sa.Column("sv4_export", sa.Float()),
        sa.Column("sv4_dg_ltrs", sa.Float()),
        sa.Column("sv4_neriya_station", sa.String(100)),
        sa.Column("sv4_kwh", sa.Float()),
        sa.Column("sv4_kvarh", sa.Float()),
        sa.Column("sv4_pf", sa.Float()),
        sa.Column("sv4_psp", sa.Float()),
        sa.Column("sv4_volt", sa.Float()),
        sa.Column("sv4_curr", sa.Float()),
        sa.Column("sv4_tc", sa.Float()),
        sa.Column("sv4_fwt_level", sa.Float()),
        sa.Column("sv4_fwt_1", sa.Float()),
        sa.Column("sv4_fwt_2", sa.Float()),
        sa.Column("sv4_dg_ltrs_2", sa.Float()),

        sa.Column("remarks", sa.Text()),
        sa.Column("status", sa.String(20)),
        sa.Column("created_by", sa.String(100)),
        sa.Column("created_at", sa.DateTime()),
        sa.Column("updated_at", sa.DateTime()),
    )

    # ===============================
    # mfm_log_ner_master_history
    # ===============================
    op.create_table(
        "mfm_log_ner_master_history",
        sa.Column("history_id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("mfm_log_ner_id", sa.Integer()),

        sa.Column("station", sa.String(100)),
        sa.Column("station_in_charge", sa.String(100)),
        sa.Column("shift", sa.String(20)),
        sa.Column("start_time", sa.Time()),
        sa.Column("log_date", sa.Date()),

        sa.Column("psp", sa.Float()),
        sa.Column("dc_voltage_op", sa.Float()),
        sa.Column("dc_current_op", sa.Float()),

        sa.Column("cp_charger", sa.String(50)),
        sa.Column("cp_ac_ip_voltage", sa.Float()),
        sa.Column("cp_ac_ip_current", sa.Float()),
        sa.Column("cp_dc_op_voltage", sa.Float()),
        sa.Column("cp_dc_op_current", sa.Float()),
        sa.Column("cp_battery_cell_voltage", sa.Float()),
        sa.Column("cp_battery_earth_leak", sa.Float()),

        sa.Column("telecom_charger", sa.String(50)),
        sa.Column("ac_ip_voltage_telecom", sa.Float()),
        sa.Column("ac_ip_current_telecom", sa.Float()),
        sa.Column("telecom_charger_dc_op_voltage", sa.Float()),
        sa.Column("telecom_charger_dc_op_current", sa.Float()),
        sa.Column("telecom_charger_battery_cell_voltage", sa.Float()),
        sa.Column("telecom_charger_battery_earth_leak", sa.Float()),

        sa.Column("kva_dg", sa.Float()),
        sa.Column("dg_ltrs", sa.Float()),

        sa.Column("remarks", sa.Text()),
        sa.Column("status", sa.String(20)),
        sa.Column("created_by", sa.String(100)),
        sa.Column("created_at", sa.DateTime()),
        sa.Column("updated_at", sa.DateTime()),
    )

    # ===============================
    # mfm_log_ner_entry
    # ===============================
    op.create_table(
        "mfm_log_ner_entry",
        sa.Column("mfm_log_ner_entry_id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("master_id", sa.Integer(), sa.ForeignKey("mfm_log_ner_master.mfm_log_ner_id")),

        sa.Column("entry_date", sa.Date()),
        sa.Column("entry_time", sa.Time()),
        sa.Column("entry_date_two", sa.Date()),
        sa.Column("entry_time_two", sa.Time()),

        sa.Column("product", sa.String(100)),
        sa.Column("batch", sa.String(100)),

        sa.Column("density", sa.Float()),
        sa.Column("temperature", sa.Float()),

        sa.Column("pump_abc", sa.String(50)),
        sa.Column("lube_oil_pressure", sa.Float()),
        sa.Column("diff_basket_filter_ab", sa.Float()),

        sa.Column("fmr_gross", sa.Float()),
        sa.Column("fmr_net", sa.Float()),
        sa.Column("fmr_mass", sa.Float()),

        sa.Column("flow_rate_net", sa.Float()),
        sa.Column("flow_rate_mass", sa.Float()),

        sa.Column("pcv_percent", sa.Float()),

        sa.Column("ic_voltage_1", sa.Float()),
        sa.Column("ic_voltage_2", sa.Float()),

        sa.Column("load_current_r", sa.Float()),
        sa.Column("load_current_y", sa.Float()),
        sa.Column("load_current_b", sa.Float()),

        sa.Column("frequency", sa.Float()),
        sa.Column("load_percent", sa.Float()),

        sa.Column("remarks", sa.Text()),
        sa.Column("created_at", sa.DateTime()),
    )

    # ===============================
    # mfm_log_ner_entry_history
    # ===============================
    op.create_table(
        "mfm_log_ner_entry_history",
        sa.Column("history_id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("mfm_log_ner_entry_id", sa.Integer()),
        sa.Column("master_id", sa.Integer()),

        sa.Column("entry_date", sa.Date()),
        sa.Column("entry_time", sa.Time()),
        sa.Column("entry_date_two", sa.Date()),
        sa.Column("entry_time_two", sa.Time()),

        sa.Column("product", sa.String(100)),
        sa.Column("batch", sa.String(100)),

        sa.Column("density", sa.Float()),
        sa.Column("temperature", sa.Float()),

        sa.Column("pump_abc", sa.String(50)),
        sa.Column("lube_oil_pressure", sa.Float()),
        sa.Column("diff_basket_filter_ab", sa.Float()),

        sa.Column("fmr_gross", sa.Float()),
        sa.Column("fmr_net", sa.Float()),
        sa.Column("fmr_mass", sa.Float()),

        sa.Column("flow_rate_net", sa.Float()),
        sa.Column("flow_rate_mass", sa.Float()),

        sa.Column("pcv_percent", sa.Float()),

        sa.Column("uc_voltage_1", sa.Float()),
        sa.Column("uc_voltage_2", sa.Float()),

        sa.Column("load_current_r", sa.Float()),
        sa.Column("load_current_y", sa.Float()),
        sa.Column("load_current_b", sa.Float()),

        sa.Column("frequency", sa.Float()),
        sa.Column("load_percent", sa.Float()),

        sa.Column("remarks", sa.Text()),

        sa.Column("action", sa.String(50)),
        sa.Column("action_by", sa.String(100)),
        sa.Column("action_at", sa.DateTime()),
    )

    # ===============================
    # mfm_log_ner_page2_master
    # ===============================
    op.create_table(
        "mfm_log_ner_page2_master",
        sa.Column("mfm_log_ner_paget_two_id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("master_log_id", sa.Integer(), sa.ForeignKey("mfm_log_ner_master.mfm_log_ner_id")),

        sa.Column("power_day", sa.Float()),
        sa.Column("power_month", sa.Float()),
        sa.Column("power_year", sa.Float()),

        sa.Column("pltd_day", sa.Float()),
        sa.Column("pltd_month", sa.Float()),
        sa.Column("pltd_year", sa.Float()),

        sa.Column("interface_details", sa.Text()),

        sa.Column("net_day", sa.Float()),
        sa.Column("net_month", sa.Float()),
        sa.Column("net_year", sa.Float()),

        sa.Column("gross_day", sa.Float()),
        sa.Column("gross_month", sa.Float()),
        sa.Column("gross_year", sa.Float()),

        sa.Column("created_at", sa.DateTime()),
    )

    # ===============================
    # mfm_log_ner_page2_master_history
    # ===============================
    op.create_table(
        "mfm_log_ner_page2_master_history",
        sa.Column("history_id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("master_log_id", sa.Integer()),
        sa.Column("mfm_log_ner_paget_two_id", sa.Integer()),

        sa.Column("power_day", sa.Float()),
        sa.Column("power_month", sa.Float()),
        sa.Column("power_year", sa.Float()),

        sa.Column("pltd_day", sa.Float()),
        sa.Column("pltd_month", sa.Float()),
        sa.Column("pltd_year", sa.Float()),

        sa.Column("interface_details", sa.Text()),

        sa.Column("net_day", sa.Float()),
        sa.Column("net_month", sa.Float()),
        sa.Column("net_year", sa.Float()),

        sa.Column("gross_day", sa.Float()),
        sa.Column("gross_month", sa.Float()),
        sa.Column("gross_year", sa.Float()),

        sa.Column("created_at", sa.DateTime()),
    )


def downgrade():
    op.drop_table("mfm_log_ner_page2_master_history")
    op.drop_table("mfm_log_ner_page2_master")
    op.drop_table("mfm_log_ner_entry_history")
    op.drop_table("mfm_log_ner_entry")
    op.drop_table("mfm_log_ner_master_history")
    op.drop_table("mfm_log_ner_master")