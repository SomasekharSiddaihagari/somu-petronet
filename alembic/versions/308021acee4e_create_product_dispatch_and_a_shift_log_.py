"""create product dispatch and a shift log tables

Revision ID: 308021acee4e
Revises: 42795a6ff735
Create Date: 2026-01-22 19:18:23.752007

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '308021acee4e'
down_revision: Union[str, Sequence[str], None] = '42795a6ff735'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # =====================================================
    # product_dispatch_category_master
    # =====================================================
    op.create_table(
        "product_dispatch_category_master",
        sa.Column("p_dispatch_id", sa.Integer(), primary_key=True, autoincrement=True),

        sa.Column("station", sa.String(100)),
        sa.Column("station_in_charge", sa.String(100)),
        sa.Column("shift", sa.String(50)),
        sa.Column("start_time", sa.Time()),
        sa.Column("logbook_date", sa.Date()),

        sa.Column("created_by", sa.String(100)),
        sa.Column("updated_by", sa.String(100)),
        sa.Column("created_at", sa.DateTime()),
        sa.Column("updated_at", sa.DateTime()),
    )

    # =====================================================
    # product_dispatch_category_master_history
    # =====================================================
    op.create_table(
        "product_dispatch_category_master_history",
        sa.Column("history_id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("p_dispatch_id", sa.Integer()),

        sa.Column("station", sa.String(100)),
        sa.Column("station_in_charge", sa.String(100)),
        sa.Column("shift", sa.String(50)),
        sa.Column("start_time", sa.Time()),
        sa.Column("logbook_date", sa.Date()),

        sa.Column("created_by", sa.String(100)),
        sa.Column("updated_by", sa.String(100)),
        sa.Column("created_at", sa.DateTime()),
        sa.Column("updated_at", sa.DateTime()),
    )

    # =====================================================
    # product_dispatch_hourly_log
    # =====================================================
    op.create_table(
        "product_dispatch_hourly_log",
        sa.Column("p_dispatch_hour_id", sa.Integer(), primary_key=True, autoincrement=True),

        sa.Column(
            "category_master_id",
            sa.Integer(),
            sa.ForeignKey("product_dispatch_category_master.p_dispatch_id"),
        ),

        sa.Column("log_date", sa.Date()),
        sa.Column("log_time", sa.Time()),

        sa.Column("mangalore_pres", sa.Float()),
        sa.Column("mangalore_tnk", sa.Float()),
        sa.Column("mangalore_suc", sa.Float()),
        sa.Column("mangalore_vol", sa.Float()),
        sa.Column("mangalore_cur", sa.Float()),
        sa.Column("mangalore_den", sa.Float()),
        sa.Column("mangalore_tmp", sa.Float()),
        sa.Column("mangalore_flw", sa.Float()),

        sa.Column("nadiya_pres", sa.Float()),
        sa.Column("nadiya_vlv", sa.Float()),
        sa.Column("nadiya_mat", sa.Float()),
        sa.Column("nadiya_flw", sa.Float()),

        sa.Column("hassan_pres", sa.Float()),
        sa.Column("hassan_bat", sa.Float()),
        sa.Column("hassan_mat", sa.Float()),
        sa.Column("hassan_qty", sa.Float()),
        sa.Column("hassan_den", sa.Float()),
        sa.Column("hassan_frm", sa.Float()),
        sa.Column("hassan_flw", sa.Float()),

        sa.Column("bangalore_pres", sa.Float()),
        sa.Column("bangalore_bat", sa.Float()),
        sa.Column("bangalore_mat", sa.Float()),
        sa.Column("bangalore_frm", sa.Float()),
        sa.Column("bangalore_to", sa.Float()),
        sa.Column("bangalore_flw", sa.Float()),
        sa.Column("bangalore_tnk", sa.Float()),

        sa.Column("created_by", sa.String(100)),
        sa.Column("created_at", sa.DateTime()),
    )

    # =====================================================
    # product_dispatch_hourly_log_history
    # =====================================================
    op.create_table(
        "product_dispatch_hourly_log_history",
        sa.Column("history_id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("p_dispatch_hour_id", sa.Integer()),
        sa.Column("category_master_id", sa.Integer()),

        sa.Column("log_date", sa.Date()),
        sa.Column("log_time", sa.Time()),

        sa.Column("mangalore_pres", sa.Float()),
        sa.Column("mangalore_tnk", sa.Float()),
        sa.Column("mangalore_suc", sa.Float()),
        sa.Column("mangalore_vol", sa.Float()),
        sa.Column("mangalore_cur", sa.Float()),
        sa.Column("mangalore_den", sa.Float()),
        sa.Column("mangalore_tmp", sa.Float()),
        sa.Column("mangalore_flw", sa.Float()),

        sa.Column("nadiya_pres", sa.Float()),
        sa.Column("nadiya_vlv", sa.Float()),
        sa.Column("nadiya_mat", sa.Float()),
        sa.Column("nadiya_flw", sa.Float()),

        sa.Column("hassan_pres", sa.Float()),
        sa.Column("hassan_bat", sa.Float()),
        sa.Column("hassan_mat", sa.Float()),
        sa.Column("hassan_qty", sa.Float()),
        sa.Column("hassan_den", sa.Float()),
        sa.Column("hassan_frm", sa.Float()),
        sa.Column("hassan_flw", sa.Float()),

        sa.Column("bangalore_pres", sa.Float()),
        sa.Column("bangalore_bat", sa.Float()),
        sa.Column("bangalore_mat", sa.Float()),
        sa.Column("bangalore_frm", sa.Float()),
        sa.Column("bangalore_to", sa.Float()),
        sa.Column("bangalore_flw", sa.Float()),
        sa.Column("bangalore_tnk", sa.Float()),

        sa.Column("created_by", sa.String(100)),
        sa.Column("created_at", sa.DateTime()),
    )

    # =====================================================
    # a_shift_log
    # =====================================================
    op.create_table(
        "a_shift_log",
        sa.Column("a_shift_log_id", sa.Integer(), primary_key=True, autoincrement=True),

        sa.Column(
            "category_master_id",
            sa.Integer(),
            sa.ForeignKey("product_dispatch_category_master.p_dispatch_id"),
        ),

        sa.Column("log_date", sa.Date()),
        sa.Column("shift_name", sa.String(20)),
        sa.Column("shift_start_time", sa.Time()),
        sa.Column("lpe_frl_at", sa.String(50)),

        sa.Column("suction_line", sa.String(100)),
        sa.Column("mlr", sa.String(100)),

        sa.Column("fire_pump_auto", sa.Boolean()),
        sa.Column("fire_pump_manual", sa.Boolean()),
        sa.Column("availability_auto", sa.Boolean()),
        sa.Column("availability_manual", sa.Boolean()),

        sa.Column("sko", sa.Float()),
        sa.Column("hsd", sa.Float()),
        sa.Column("ms", sa.Float()),
        sa.Column("dkn", sa.Float()),

        sa.Column("batch", sa.String(50)),
        sa.Column("qty", sa.Float()),

        sa.Column("sump_level_percent", sa.Float()),
        sa.Column("ci_pumped_percent", sa.Float()),

        sa.Column("net_qty_of_shift", sa.Float()),
        sa.Column("gross_qty_of_shift", sa.Float()),
        sa.Column("atg_qty_of_shift", sa.Float()),

        sa.Column("bp_101a_previous_hrs", sa.Float()),
        sa.Column("bp_101a_current_hrs", sa.Float()),
        sa.Column("bp_101a_cumulative_hrs", sa.Float()),
        sa.Column("bp_101a_availability", sa.String(50)),
        sa.Column("bp_101a_product", sa.String(50)),

        sa.Column("bp_101b_previous_hrs", sa.Float()),
        sa.Column("bp_101b_current_hrs", sa.Float()),
        sa.Column("bp_101b_cumulative_hrs", sa.Float()),
        sa.Column("bp_101b_availability", sa.String(50)),
        sa.Column("bp_101b_product", sa.String(50)),

        sa.Column("bp_102a_previous_hrs", sa.Float()),
        sa.Column("bp_102a_current_hrs", sa.Float()),
        sa.Column("bp_102a_cumulative_hrs", sa.Float()),
        sa.Column("bp_102a_availability", sa.String(50)),
        sa.Column("bp_102a_product", sa.String(50)),

        sa.Column("bp_102b_previous_hrs", sa.Float()),
        sa.Column("bp_102b_current_hrs", sa.Float()),
        sa.Column("bp_102b_cumulative_hrs", sa.Float()),
        sa.Column("bp_102b_availability", sa.String(50)),
        sa.Column("bp_102b_product", sa.String(50)),

        sa.Column("bp_102c_previous_hrs", sa.Float()),
        sa.Column("bp_102c_current_hrs", sa.Float()),
        sa.Column("bp_102c_cumulative_hrs", sa.Float()),
        sa.Column("bp_102c_availability", sa.String(50)),
        sa.Column("bp_102c_product", sa.String(50)),

        sa.Column("sump_pump_previous_hrs", sa.Float()),
        sa.Column("sump_pump_current_hrs", sa.Float()),
        sa.Column("sump_pump_cumulative_hrs", sa.Float()),
        sa.Column("sump_pump_availability", sa.String(50)),
        sa.Column("sump_pump_product", sa.String(50)),

        sa.Column("ci_pump_101a_previous_hrs", sa.Float()),
        sa.Column("ci_pump_101a_current_hrs", sa.Float()),
        sa.Column("ci_pump_101a_cumulative_hrs", sa.Float()),
        sa.Column("ci_pump_101a_availability", sa.String(50)),
        sa.Column("ci_pump_101a_product", sa.String(50)),

        sa.Column("ci_pump_101b_previous_hrs", sa.Float()),
        sa.Column("ci_pump_101b_current_hrs", sa.Float()),
        sa.Column("ci_pump_101b_cumulative_hrs", sa.Float()),
        sa.Column("ci_pump_101b_availability", sa.String(50)),
        sa.Column("ci_pump_101b_product", sa.String(50)),

        sa.Column("maintenance_details", sa.Text()),
        sa.Column("shift_engineer_name", sa.String(100)),
        sa.Column("signature", sa.String(255)),

        sa.Column("created_by", sa.String(100)),
        sa.Column("created_at", sa.DateTime()),
    )

    # =====================================================
    # a_shift_log_history
    # =====================================================
    op.create_table(
        "a_shift_log_history",
        sa.Column("history_id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("a_shift_log_id", sa.Integer()),
        sa.Column("category_master_id", sa.Integer()),

        sa.Column("log_date", sa.Date()),
        sa.Column("shift_name", sa.String(20)),
        sa.Column("shift_start_time", sa.Time()),
        sa.Column("lpe_frl_at", sa.String(50)),

        sa.Column("suction_line", sa.String(100)),
        sa.Column("mlr", sa.String(100)),

        sa.Column("fire_pump_auto", sa.Boolean()),
        sa.Column("fire_pump_manual", sa.Boolean()),
        sa.Column("availability_auto", sa.Boolean()),
        sa.Column("availability_manual", sa.Boolean()),

        sa.Column("sko", sa.Float()),
        sa.Column("hsd", sa.Float()),
        sa.Column("ms", sa.Float()),
        sa.Column("dkn", sa.Float()),

        sa.Column("batch", sa.String(50)),
        sa.Column("qty", sa.Float()),

        sa.Column("sump_level_percent", sa.Float()),
        sa.Column("ci_pumped_percent", sa.Float()),

        sa.Column("net_qty_of_shift", sa.Float()),
        sa.Column("gross_qty_of_shift", sa.Float()),
        sa.Column("atg_qty_of_shift", sa.Float()),

        sa.Column("bp_101a_previous_hrs", sa.Float()),
        sa.Column("bp_101a_current_hrs", sa.Float()),
        sa.Column("bp_101a_cumulative_hrs", sa.Float()),
        sa.Column("bp_101a_availability", sa.String(50)),
        sa.Column("bp_101a_product", sa.String(50)),

        sa.Column("bp_101b_previous_hrs", sa.Float()),
        sa.Column("bp_101b_current_hrs", sa.Float()),
        sa.Column("bp_101b_cumulative_hrs", sa.Float()),
        sa.Column("bp_101b_availability", sa.String(50)),
        sa.Column("bp_101b_product", sa.String(50)),

        sa.Column("bp_102a_previous_hrs", sa.Float()),
        sa.Column("bp_102a_current_hrs", sa.Float()),
        sa.Column("bp_102a_cumulative_hrs", sa.Float()),
        sa.Column("bp_102a_availability", sa.String(50)),
        sa.Column("bp_102a_product", sa.String(50)),

        sa.Column("bp_102b_previous_hrs", sa.Float()),
        sa.Column("bp_102b_current_hrs", sa.Float()),
        sa.Column("bp_102b_cumulative_hrs", sa.Float()),
        sa.Column("bp_102b_availability", sa.String(50)),
        sa.Column("bp_102b_product", sa.String(50)),

        sa.Column("bp_102c_previous_hrs", sa.Float()),
        sa.Column("bp_102c_current_hrs", sa.Float()),
        sa.Column("bp_102c_cumulative_hrs", sa.Float()),
        sa.Column("bp_102c_availability", sa.String(50)),
        sa.Column("bp_102c_product", sa.String(50)),

        sa.Column("sump_pump_previous_hrs", sa.Float()),
        sa.Column("sump_pump_current_hrs", sa.Float()),
        sa.Column("sump_pump_cumulative_hrs", sa.Float()),
        sa.Column("sump_pump_availability", sa.String(50)),
        sa.Column("sump_pump_product", sa.String(50)),

        sa.Column("ci_pump_101a_previous_hrs", sa.Float()),
        sa.Column("ci_pump_101a_current_hrs", sa.Float()),
        sa.Column("ci_pump_101a_cumulative_hrs", sa.Float()),
        sa.Column("ci_pump_101a_availability", sa.String(50)),
        sa.Column("ci_pump_101a_product", sa.String(50)),

        sa.Column("ci_pump_101b_previous_hrs", sa.Float()),
        sa.Column("ci_pump_101b_current_hrs", sa.Float()),
        sa.Column("ci_pump_101b_cumulative_hrs", sa.Float()),
        sa.Column("ci_pump_101b_availability", sa.String(50)),
        sa.Column("ci_pump_101b_product", sa.String(50)),

        sa.Column("maintenance_details", sa.Text()),
        sa.Column("shift_engineer_name", sa.String(100)),
        sa.Column("signature", sa.String(255)),

        sa.Column("created_by", sa.String(100)),
        sa.Column("created_at", sa.DateTime()),
    )


def downgrade():
    op.drop_table("a_shift_log_history")
    op.drop_table("a_shift_log")
    op.drop_table("product_dispatch_hourly_log_history")
    op.drop_table("product_dispatch_hourly_log")
    op.drop_table("product_dispatch_category_master_history")
    op.drop_table("product_dispatch_category_master")