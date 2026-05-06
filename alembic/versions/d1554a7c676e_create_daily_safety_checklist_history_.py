"""create daily safety checklist history table

Revision ID: d1554a7c676e
Revises: f8e1b772480e
Create Date: 2026-01-19 21:29:25.549162

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd1554a7c676e'
down_revision: Union[str, Sequence[str], None] = 'f8e1b772480e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table(
        "daily_safety_checklist_history",
        sa.Column("history_id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("dsc_id", sa.Integer(), nullable=False),
        sa.Column("doc_no", sa.String(length=50)),
        sa.Column("shift", sa.String(length=10)),
        sa.Column("start_time", sa.Time()),
        sa.Column("station", sa.String(length=100)),
        sa.Column("station_in_charge", sa.String(length=100)),
        sa.Column("checklist_date", sa.Date()),
        sa.Column("prepared_by_name", sa.String(length=100)),
        sa.Column("reviewed_by_name", sa.String(length=100)),

        # ---------------- Section B – FIRE SAFETY ----------------
        sa.Column("b1_water_level_satisfactory", sa.Boolean()),
        sa.Column("b1_water_level_remarks", sa.Text()),
        sa.Column("b1_water_tank_level_1", sa.String(length=50)),
        sa.Column("b1_water_tank_level_2", sa.String(length=50)),
        sa.Column("b1_water_tank_level_3", sa.String(length=50)),

        sa.Column("b2_hydrant_pressure_maintained", sa.Boolean()),
        sa.Column("b2_hydrant_pressure_value", sa.Text()),

        sa.Column("b3_fire_pump_diesel_batteries_good", sa.Boolean()),
        sa.Column("b3_diesel_tank_level_1", sa.String(length=50)),
        sa.Column("b3_diesel_tank_level_2", sa.String(length=50)),
        sa.Column("b3_diesel_tank_level_3", sa.String(length=50)),
        sa.Column("b3_valves_fully_open", sa.String(length=250)),
        sa.Column("b3_one_pump_start_pressure", sa.String(length=50)),
        sa.Column("b3_auto_start_system_developed", sa.Boolean()),
        sa.Column("b3_fire_water_pumps_egines_remarks", sa.Text()),

        sa.Column("b4_fire_alarm_communication_working", sa.Boolean()),
        sa.Column("b4_remarks", sa.Text()),

        sa.Column("b5_clean_agent_system_cylinders_filled", sa.Boolean()),
        sa.Column("b5_remarks", sa.Text()),

        sa.Column("b6_any_unsafe_condition_fire_protection", sa.Boolean()),
        sa.Column("b6_remarks", sa.Text()),

        sa.Column("b7_regular_surprise_check_testing_done", sa.Boolean()),
        sa.Column("b7_remarks", sa.Text()),

        sa.Column("b8_wind_direction_displayed", sa.Boolean()),
        sa.Column("b8_remarks", sa.Text()),

        sa.Column("b9_caution_signs_displayed", sa.Boolean()),
        sa.Column("b9_remarks", sa.Text()),

        sa.Column("b10_fire_extinguishers_in_place_upto_date", sa.Boolean()),
        sa.Column("b10_remarks", sa.Text()),

        sa.Column("b11_cctv_functioning", sa.Boolean()),
        sa.Column("b11_remarks", sa.Text()),

        # ---------------- Section B – SECURITY ----------------
        sa.Column("b_sec1_frisking_observation", sa.Text()),
        sa.Column("b_sec1_frisking_remarks", sa.Text()),

        sa.Column("b_sec2_boundary_wall_integrity_observation", sa.Text()),
        sa.Column("b_sec2_remarks", sa.Text()),

        sa.Column("b_sec3_emergency_gate_check_observation", sa.Text()),
        sa.Column("b_sec3_remarks", sa.Text()),

        sa.Column("b_sec4_ppe_usage_hazardous_area_observation", sa.Text()),
        sa.Column("b_sec4_remarks", sa.Text()),

        # ---------------- Section C ----------------
        sa.Column("c1_emergency_response_vehicle_reg_no", sa.String(length=50)),
        sa.Column("c1_emergency_maintenance_vehicle_reg_no", sa.String(length=50)),
        sa.Column("c1_fire_tender_reg_no", sa.String(length=50)),
        sa.Column("c1_gypsy_reg_no", sa.String(length=50)),
        sa.Column("c1_remarks", sa.Text()),

        sa.Column("c2_observation", sa.Text()),
        sa.Column("c2_remarks", sa.Text()),

        # ---------------- Section D ----------------
        sa.Column("d1_transformer_yard_gate_closed_observation", sa.Text()),
        sa.Column("d1_remarks", sa.Text()),

        sa.Column("d2_authorized_entry_only_observation", sa.Text()),
        sa.Column("d2_remarks", sa.Text()),

        sa.Column("d3_any_oil_leak_observed", sa.Text()),
        sa.Column("d3_remarks", sa.Text()),

        sa.Column("d4_housekeeping_in_order", sa.Text()),
        sa.Column("d4_remarks", sa.Text()),

        sa.Column("d5_temporary_electrical_connection_exists", sa.Text()),
        sa.Column("d5_remarks", sa.Text()),

        sa.Column("d6_substation_housekeeping_in_order", sa.Text()),
        sa.Column("d6_remarks", sa.Text()),

        # ---------------- Section E ----------------
        sa.Column("e1_electrical_connections_sound", sa.Boolean()),
        sa.Column("e1_remarks", sa.Text()),
        sa.Column("e2_earthing_proper", sa.Boolean()),
        sa.Column("e2_remarks", sa.Text()),
        sa.Column("e3_gauges_pumps_working", sa.Boolean()),
        sa.Column("e3_remarks", sa.Text()),
        sa.Column("e4_safety_guards_in_position", sa.Boolean()),
        sa.Column("e4_remarks", sa.Text()),
        sa.Column("e5_abnormal_vibration_noise", sa.Boolean()),
        sa.Column("e5_remarks", sa.Text()),
        sa.Column("e6_portable_extinguishers_in_position", sa.Boolean()),
        sa.Column("e6_remarks", sa.Text()),
        sa.Column("e7_any_product_leak_unsafe_condition", sa.Boolean()),
        sa.Column("e7_remarks", sa.Text()),
        sa.Column("e8_housekeeping_in_order", sa.Boolean()),
        sa.Column("e8_remarks", sa.Text()),
        sa.Column("e9_hydrocarbon_detection_system_working", sa.Boolean()),
        sa.Column("e9_remarks", sa.Text()),
        sa.Column("e10_last_fire_drill_done_on", sa.String(length=50)),
        sa.Column("e10_remarks", sa.Text()),
        sa.Column("e11_fire_water_monitors_hoses_good_condition", sa.Boolean()),
        sa.Column("e11_remarks", sa.Text()),

        # ---------------- Section F – Area I / II / III (FULL) ----------------
        sa.Column("f_i_1_no_ignition_sources_visible", sa.Boolean()),
        sa.Column("f_i_1_remarks", sa.Text()),
        sa.Column("f_i_2_all_electrical_connections_safe", sa.Boolean()),
        sa.Column("f_i_2_remarks", sa.Text()),
        sa.Column("f_i_3_sprinkler_system_working", sa.Boolean()),
        sa.Column("f_i_3_remarks", sa.Text()),
        sa.Column("f_i_4_housekeeping_in_order", sa.Boolean()),
        sa.Column("f_i_4_remarks", sa.Text()),
        sa.Column("f_i_5_ows_tank_farm_functional", sa.Boolean()),
        sa.Column("f_i_5_remarks", sa.Text()),
        sa.Column("f_i_6_fire_extinguishers_accessible", sa.Boolean()),
        sa.Column("f_i_6_remarks", sa.Text()),
        sa.Column("f_i_7_any_product_leak_or_unsafe_condition", sa.Boolean()),
        sa.Column("f_i_7_remarks", sa.Text()),
        sa.Column("f_i_8_fire_water_monitors_hoses_good", sa.Boolean()),
        sa.Column("f_i_8_remarks", sa.Text()),
        sa.Column("f_i_9_rovs_on_remote_mode", sa.Boolean()),
        sa.Column("f_i_9_remarks", sa.Text()),
        sa.Column("f_i_10_pressure_temperature_transmitters_functional", sa.Boolean()),
        sa.Column("f_i_10_remarks", sa.Text()),
        sa.Column("f_i_11_bonding_across_flanges_visible_intact", sa.Boolean()),
        sa.Column("f_i_11_remarks", sa.Text()),
        sa.Column("f_i_12_last_fire_drill_done", sa.Boolean()),
        sa.Column("f_i_12_remarks", sa.Text()),
        sa.Column("f_i_13_hydrocarbon_detection_system_working", sa.Boolean()),
        sa.Column("f_i_13_remarks", sa.Text()),

        sa.Column("created_at", sa.DateTime(), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(), server_default=sa.func.now(), onupdate=sa.func.now()),
    )


def downgrade():
    op.drop_table("daily_safety_checklist_history")