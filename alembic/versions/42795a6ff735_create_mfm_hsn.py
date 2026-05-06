"""create mfm hsn

Revision ID: 42795a6ff735
Revises: 172e4a6f9091
Create Date: 2026-01-22 18:21:26.594280

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import func

# revision identifiers, used by Alembic.
revision: str = '42795a6ff735'
down_revision: Union[str, Sequence[str], None] = '172e4a6f9091'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # =====================================================
    # mfm_log_hsn_master
    # =====================================================
    op.create_table(
        "mfm_log_hsn_master",
        sa.Column("mfm_log_hsn_id", sa.Integer(), primary_key=True, autoincrement=True),

        sa.Column("station", sa.String(50)),
        sa.Column("station_in_charge", sa.String(100)),
        sa.Column("shift", sa.String(10)),
        sa.Column("start_time", sa.Time()),
        sa.Column("log_date", sa.Date()),
        sa.Column("document_no", sa.String(100)),

        sa.Column("left_initial_tank_no", sa.String(50)),
        sa.Column("left_initial_dip_in_cms", sa.Float()),
        sa.Column("left_tank_co_time", sa.Time()),

        sa.Column("left_final_tank_dip_in_cms", sa.Float()),
        sa.Column("left_new_tank_initial_dip_in_cm", sa.Float()),
        sa.Column("left_new_tank_no", sa.String(50)),

        sa.Column("left_co_fm_reading_gross", sa.Float()),
        sa.Column("left_co_fm_reading_nett", sa.Float()),
        sa.Column("left_co_fm_reading_mass", sa.Float()),

        sa.Column("left2_initial_tank_no", sa.String(50)),
        sa.Column("left2_initial_dip_in_cms", sa.Float()),
        sa.Column("left2_tank_co_time", sa.Time()),

        sa.Column("left2_final_tank_dip_in_cms", sa.Float()),
        sa.Column("left2_new_tank_initial_dip_in_cm", sa.Float()),
        sa.Column("left2_new_tank_no", sa.String(50)),

        sa.Column("left2_co_fm_reading_gross", sa.Float()),
        sa.Column("left2_co_fm_reading_nett", sa.Float()),
        sa.Column("left2_co_fm_reading_mass", sa.Float()),

        sa.Column("right_initial_tank_no", sa.String(50)),
        sa.Column("right_initial_dip_in_cms", sa.Float()),
        sa.Column("right_tank_co_time", sa.Time()),

        sa.Column("right_final_tank_dip_in_cms", sa.Float()),
        sa.Column("right_new_tank_initial_dip_in_cm", sa.Float()),
        sa.Column("right_new_tank_no", sa.String(50)),

        sa.Column("right_co_fm_reading_gross", sa.Float()),
        sa.Column("right_co_fm_reading_nett", sa.Float()),
        sa.Column("right_co_fm_reading_mass", sa.Float()),

        sa.Column("faq_changed_from", sa.String(50)),
        sa.Column("faq_changed_to", sa.String(50)),
        sa.Column("faq_changed_at", sa.Time()),

        sa.Column("initial_fmr_g", sa.Float()),
        sa.Column("initial_fmr_n", sa.Float()),
        sa.Column("initial_fmr_m", sa.Float()),

        sa.Column("final_fmr_g", sa.Float()),
        sa.Column("final_fmr_n", sa.Float()),
        sa.Column("final_fmr_m", sa.Float()),

        sa.Column("sic_name", sa.String(100)),

        sa.Column("b_left_initial_tank_no", sa.String(50)),
        sa.Column("b_left_initial_dip_in_cms", sa.Float()),
        sa.Column("b_left_tank_co_time", sa.Time()),

        sa.Column("b_left_final_tank_dip_in_cms", sa.Float()),
        sa.Column("b_left_new_tank_initial_dip_in_cm", sa.Float()),
        sa.Column("b_left_new_tank_no", sa.String(50)),

        sa.Column("b_left_co_fm_reading_gross", sa.Float()),
        sa.Column("b_left_co_fm_reading_nett", sa.Float()),
        sa.Column("b_left_co_fm_reading_mass", sa.Float()),

        sa.Column("b_left2_initial_tank_no", sa.String(50)),
        sa.Column("b_left2_initial_dip_in_cms", sa.Float()),
        sa.Column("b_left2_tank_co_time", sa.Time()),

        sa.Column("b_left2_final_tank_dip_in_cms", sa.Float()),
        sa.Column("b_left2_new_tank_initial_dip_in_cm", sa.Float()),
        sa.Column("b_left2_new_tank_no", sa.String(50)),

        sa.Column("b_left2_co_fm_reading_gross", sa.Float()),
        sa.Column("b_left2_co_fm_reading_nett", sa.Float()),
        sa.Column("b_left2_co_fm_reading_mass", sa.Float()),

        sa.Column("created_at", sa.DateTime(), server_default=func.now()),
    )

    # =====================================================
    # mfm_log_hsn_entry
    # =====================================================
    op.create_table(
        "mfm_log_hsn_entry",
        sa.Column("mfm_log_hsn_entry_id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column(
            "master_id",
            sa.Integer(),
            sa.ForeignKey("mfm_log_hsn_master.mfm_log_hsn_id", ondelete="CASCADE"),
        ),

        sa.Column("entry_date", sa.Date()),
        sa.Column("entry_time", sa.Time()),

        sa.Column("pt_1308_pressure", sa.Numeric(10, 3)),
        sa.Column("pt_1306_pressure", sa.Numeric(10, 3)),

        sa.Column("flow_rate_net", sa.Numeric(12, 3)),
        sa.Column("flow_rate_gross", sa.Numeric(12, 3)),

        sa.Column("hpcl_fcv_opening_1315", sa.Numeric(12, 3)),

        sa.Column("gross_vol_reading_fqy", sa.Numeric(12, 3)),
        sa.Column("gross_qty_delivered_kl", sa.Numeric(12, 3)),

        sa.Column("net_vol_reading_fqy", sa.Numeric(12, 3)),
        sa.Column("net_qty_delivered_kl", sa.Numeric(12, 3)),

        sa.Column("mass_reading_mt_fqy", sa.Numeric(12, 3)),
        sa.Column("mass_qty_delivered_mt_kl", sa.Numeric(12, 3)),

        sa.Column("product_density", sa.Numeric(10, 4)),
        sa.Column("product_temp", sa.Numeric(6, 2)),
        sa.Column("density_15deg", sa.Numeric(10, 4)),

        sa.Column("hpcl_line_no", sa.String(50)),
        sa.Column("tank_dip_during_plt_cm", sa.Numeric(10, 2)),
        sa.Column("qty_as_per_atg", sa.Numeric(12, 3)),

        sa.Column("diff_atg_fmr", sa.Numeric(12, 3)),
        sa.Column("sign_shift_ie", sa.String(100)),

        sa.Column("remarks", sa.Text()),
        sa.Column("created_at", sa.DateTime(), server_default=func.now()),
    )

    # =====================================================
    # mfm_log_hsn_entry_history
    # =====================================================
    op.create_table(
        "mfm_log_hsn_entry_history",
        sa.Column("history_id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("mfm_log_hsn_entry_id", sa.Integer()),
        sa.Column("master_id", sa.Integer()),

        sa.Column("entry_date", sa.Date()),
        sa.Column("entry_time", sa.Time()),

        sa.Column("pt_1308_pressure", sa.Numeric(10, 3)),
        sa.Column("pt_1306_pressure", sa.Numeric(10, 3)),

        sa.Column("flow_rate_net", sa.Numeric(12, 3)),
        sa.Column("flow_rate_gross", sa.Numeric(12, 3)),

        sa.Column("hpcl_fcv_opening_1315", sa.Numeric(12, 3)),

        sa.Column("gross_vol_reading_fqy", sa.Numeric(12, 3)),
        sa.Column("gross_qty_delivered_kl", sa.Numeric(12, 3)),

        sa.Column("net_vol_reading_fqy", sa.Numeric(12, 3)),
        sa.Column("net_qty_delivered_kl", sa.Numeric(12, 3)),

        sa.Column("mass_reading_mt_fqy", sa.Numeric(12, 3)),
        sa.Column("mass_qty_delivered_mt_kl", sa.Numeric(12, 3)),

        sa.Column("product_density", sa.Numeric(10, 4)),
        sa.Column("product_temp", sa.Numeric(6, 2)),
        sa.Column("density_15deg", sa.Numeric(10, 4)),

        sa.Column("hpcl_line_no", sa.String(50)),
        sa.Column("tank_dip_during_plt_cm", sa.Numeric(10, 2)),
        sa.Column("qty_as_per_atg", sa.Numeric(12, 3)),

        sa.Column("diff_atg_fmr", sa.Numeric(12, 3)),
        sa.Column("sign_shift_ie", sa.String(100)),

        sa.Column("remarks", sa.Text()),
        sa.Column("created_at", sa.DateTime(), server_default=func.now()),
    )

    # =====================================================
    # mfm_log_hsn_master_history
    # =====================================================
    op.create_table(
        "mfm_log_hsn_master_history",
        sa.Column("history_id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("mfm_log_hsn_id", sa.Integer()),

        sa.Column("document_no", sa.String(100)),
        sa.Column("station", sa.String(50)),
        sa.Column("station_in_charge", sa.String(100)),
        sa.Column("shift", sa.String(10)),
        sa.Column("start_time", sa.Time()),
        sa.Column("log_date", sa.Date()),

        sa.Column("shift_a_tank_takeover", sa.String(100)),
        sa.Column("shift_a_tank_handover", sa.String(100)),
        sa.Column("shift_b_tank_takeover", sa.String(100)),
        sa.Column("shift_b_tank_handover", sa.String(100)),
        sa.Column("shift_c_tank_takeover", sa.String(100)),
        sa.Column("shift_c_tank_handover", sa.String(100)),

        sa.Column("qty_pumped_mangalore_kl", sa.Numeric(12, 3)),
        sa.Column("receipt_hassan_kl", sa.Numeric(12, 3)),
        sa.Column("receipt_bangalore_kl", sa.Numeric(12, 3)),

        sa.Column("qty_available_tank101_kl", sa.Numeric(12, 3)),
        sa.Column("qty_available_tank102_kl", sa.Numeric(12, 3)),

        sa.Column("loss_gain_kl", sa.Numeric(12, 3)),

        sa.Column("qty_pumped_last_24hrs_kl", sa.Numeric(12, 3)),
        sa.Column("qty_pumped_plt_kl", sa.Numeric(12, 3)),
        sa.Column("qty_pumped_month_kl", sa.Numeric(12, 3)),
        sa.Column("qty_pumped_year_kl", sa.Numeric(12, 3)),

        sa.Column("diesel_dg_tank_ltrs", sa.Numeric(12, 3)),
        sa.Column("diesel_dg_set_tank_ltrs", sa.Numeric(12, 3)),
        sa.Column("diesel_ffdu3_ser_tank_ltrs", sa.Numeric(12, 3)),
        sa.Column("diesel_ffdu4_ser_tank_ltrs", sa.Numeric(12, 3)),
        sa.Column("diesel_ffdu5_ser_tank_ltrs", sa.Numeric(12, 3)),

        sa.Column("hrs_operation_last_24hrs", sa.Numeric(6, 2)),
        sa.Column("hrs_operation_month", sa.Numeric(6, 2)),
        sa.Column("hrs_operation_year", sa.Numeric(6, 2)),
        sa.Column("sump_tank_dip_0700_hrs", sa.Numeric(12, 3)),

        sa.Column("sic_signature", sa.String(100)),
        sa.Column("created_at", sa.DateTime(), server_default=func.now()),
    )

    # =====================================================
    # HSN2 MASTER
    # =====================================================
    op.create_table(
        "mfm_log_hsn2_master",
        sa.Column("mfm_hsn_two_id", sa.Integer(), primary_key=True, autoincrement=True),

        sa.Column("station", sa.String(50), nullable=False),
        sa.Column("station_in_charge", sa.String(100)),
        sa.Column("shift", sa.String(20)),
        sa.Column("start_time", sa.Time()),
        sa.Column("log_date", sa.Date()),

        sa.Column("fqy_changed_from", sa.String(50)),
        sa.Column("fqy_changed_to", sa.String(50)),
        sa.Column("fqy_changed_at", sa.Time()),

        sa.Column("initial_fmr_g", sa.String(20)),
        sa.Column("initial_fmr_n", sa.String(20)),
        sa.Column("initial_fmr_m", sa.String(20)),

        sa.Column("final_fmr_g", sa.String(20)),
        sa.Column("final_fmr_n", sa.String(20)),
        sa.Column("final_fmr_m", sa.String(20)),

        sa.Column("sic_name", sa.String(100)),
        sa.Column("created_at", sa.DateTime(), server_default=func.now()),
    )

    # =====================================================
    # HSN2 ENTRY
    # =====================================================
    op.create_table(
        "mfm_log_hsn2_entry",
        sa.Column("mfm_log_hsn2_entry_id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column(
            "master_id",
            sa.Integer(),
            sa.ForeignKey("mfm_log_hsn2_master.mfm_hsn_two_id"),
            nullable=False,
        ),

        sa.Column("entry_date", sa.Date()),
        sa.Column("entry_time", sa.Time()),

        sa.Column("pump_inlet_header_pr", sa.String(50)),
        sa.Column("pump_outlet_header_pr", sa.String(50)),
        sa.Column("digital_fcva_opening", sa.String(50)),

        sa.Column("flow_rate_net", sa.String(50)),
        sa.Column("flow_rate_gross", sa.String(50)),

        sa.Column("gross_vol_fqy", sa.String(50)),
        sa.Column("gross_qty_per_gross", sa.String(50)),

        sa.Column("nett_vol_fqy", sa.String(50)),
        sa.Column("nett_qty_per_gross", sa.String(50)),

        sa.Column("mass_vol_fqy", sa.String(50)),
        sa.Column("qty_delivered_mt", sa.String(50)),

        sa.Column("density", sa.String(50)),
        sa.Column("temperature", sa.String(50)),
        sa.Column("density_15_deg", sa.String(50)),

        sa.Column("tank_corr_during_cm", sa.Float()),
        sa.Column("ci_pump", sa.String(50)),
        sa.Column("ci_line_pr", sa.Float()),
        sa.Column("stroke_len", sa.Float()),
        sa.Column("ci_dosing_rate", sa.Float()),

        sa.Column("sign_of_shift_ie", sa.String(100)),
        sa.Column("remarks", sa.Text()),
        sa.Column("created_at", sa.DateTime(), server_default=func.now()),
    )

    # =====================================================
    # HSN2 ENTRY HISTORY
    # =====================================================
    op.create_table(
        "mfm_log_hsn2_entry_history",
        sa.Column("history_id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("mfm_log_hsn2_entry_id", sa.Integer()),
        sa.Column("master_id", sa.Integer(), nullable=False),

        sa.Column("entry_date", sa.Date()),
        sa.Column("entry_time", sa.Time()),

        sa.Column("pump_inlet_header_pr", sa.String(50)),
        sa.Column("pump_outlet_header_pr", sa.String(50)),
        sa.Column("digital_fcva_opening", sa.String(50)),

        sa.Column("flow_rate_net", sa.String(50)),
        sa.Column("flow_rate_gross", sa.String(50)),

        sa.Column("gross_vol_fqy", sa.String(50)),
        sa.Column("gross_qty_per_gross", sa.String(50)),

        sa.Column("nett_vol_fqy", sa.String(50)),
        sa.Column("nett_qty_per_gross", sa.String(50)),

        sa.Column("mass_vol_fqy", sa.String(50)),
        sa.Column("qty_delivered_mt", sa.String(50)),

        sa.Column("density", sa.String(50)),
        sa.Column("temperature", sa.String(50)),
        sa.Column("density_15_deg", sa.String(50)),

        sa.Column("tank_corr_during_cm", sa.Float()),
        sa.Column("ci_pump", sa.String(50)),
        sa.Column("ci_line_pr", sa.Float()),
        sa.Column("stroke_len", sa.Float()),
        sa.Column("ci_dosing_rate", sa.Float()),

        sa.Column("sign_of_shift_ie", sa.String(100)),
        sa.Column("remarks", sa.Text()),
        sa.Column("created_at", sa.DateTime(), server_default=func.now()),
    )

    # =====================================================
    # HSN2 MASTER HISTORY
    # =====================================================
    op.create_table(
        "mfm_log_hsn2_master_history",
        sa.Column("history_id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("mfm_hsn_two_id_id", sa.Integer()),

        sa.Column("station", sa.String(50), nullable=False),
        sa.Column("station_in_charge", sa.String(100)),
        sa.Column("shift", sa.String(20)),
        sa.Column("start_time", sa.Time()),
        sa.Column("log_date", sa.Date()),

        sa.Column("fqy_changed_from", sa.String(50)),
        sa.Column("fqy_changed_to", sa.String(50)),
        sa.Column("fqy_changed_at", sa.Time()),

        sa.Column("initial_fmr_g", sa.String(20)),
        sa.Column("initial_fmr_n", sa.String(20)),
        sa.Column("initial_fmr_m", sa.String(20)),

        sa.Column("final_fmr_g", sa.String(20)),
        sa.Column("final_fmr_n", sa.String(20)),
        sa.Column("final_fmr_m", sa.String(20)),

        sa.Column("sic_name", sa.String(100)),
        sa.Column("created_at", sa.DateTime(), server_default=func.now()),
    )


def downgrade():
    op.drop_table("mfm_log_hsn2_master_history")
    op.drop_table("mfm_log_hsn2_entry_history")
    op.drop_table("mfm_log_hsn2_entry")
    op.drop_table("mfm_log_hsn2_master")

    op.drop_table("mfm_log_hsn_master_history")
    op.drop_table("mfm_log_hsn_entry_history")
    op.drop_table("mfm_log_hsn_entry")
    op.drop_table("mfm_log_hsn_master")