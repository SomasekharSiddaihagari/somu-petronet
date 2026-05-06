from pydantic import BaseModel, Field
from typing import Optional, Text
from datetime import date, time, datetime

# from sqlalchemy import Boolean, Text

class DailySafetyChecklistBase(BaseModel):

    doc_no: Optional[str] = None
    shift: Optional[str] = None
    start_time: Optional[time] = None
    station: Optional[str] = None
    station_in_charge: Optional[str] = None
    checklist_date: Optional[date] = None
    prepared_by_name: Optional[str] = None
    reviewed_by_name: Optional[str] = None
    ms_logbook_id: Optional[int] = None

    # ─── Section B - FIRE SAFETY ───────────────────────────────────────────────

    b1_water_level_satisfactory: Optional[bool] = None
    b1_water_level_remarks: Optional[str] = None
    b1_water_tank_level_1: Optional[str] = None
    b1_water_tank_level_2: Optional[str] = None
    b1_water_tank_level_3: Optional[str] = None

    b2_hydrant_pressure_maintained: Optional[bool] = None
    b2_hydrant_pressure_value: Optional[str] = None

    b3_fire_pump_diesel_batteries_good: Optional[bool] = None
    b3_diesel_tank_level_1: Optional[str] = None
    b3_diesel_tank_level_2: Optional[str] = None
    b3_diesel_tank_level_3: Optional[str] = None
    b3_valves_fully_open: Optional[str] = None
    b3_one_pump_start_pressure: Optional[str] = None
    b3_auto_start_system_developed: Optional[bool] = None
    b3_fire_water_pumps_egines_remarks: Optional[str] = None

    b4_fire_alarm_communication_working: Optional[bool] = None
    b4_remarks: Optional[str] = None

    b5_clean_agent_system_cylinders_filled: Optional[bool] = None
    b5_remarks: Optional[str] = None

    b6_any_unsafe_condition_fire_protection: Optional[bool] = None
    b6_remarks: Optional[str] = None

    b7_regular_surprise_check_testing_done: Optional[bool] = None
    b7_remarks: Optional[str] = None

    b8_wind_direction_displayed: Optional[bool] = None
    b8_remarks: Optional[str] = None

    b9_caution_signs_displayed: Optional[bool] = None
    b9_remarks: Optional[str] = None

    b10_fire_extinguishers_in_place_upto_date: Optional[bool] = None
    b10_remarks: Optional[str] = None

    b11_cctv_functioning: Optional[bool] = None
    b11_remarks: Optional[str] = None

    # ─── Section B - SECURITY CHECKS ──────────────────────────────────────────

    b_sec1_frisking_observation: Optional[str] = None
    b_sec1_frisking_remarks: Optional[str] = None

    b_sec2_boundary_wall_integrity_observation: Optional[str] = None
    b_sec2_remarks: Optional[str] = None

    b_sec3_emergency_gate_check_observation: Optional[str] = None
    b_sec3_remarks: Optional[str] = None

    b_sec4_ppe_usage_hazardous_area_observation: Optional[str] = None
    b_sec4_remarks: Optional[str] = None

    # ─── Section C - EMERGENCY VEHICLE ────────────────────────────────────────

    c1_emergency_response_vehicle_reg_no: Optional[str] = None
    c1_emergency_maintenance_vehicle_reg_no: Optional[str] = None
    c1_fire_tender_reg_no: Optional[str] = None
    c1_gypsy_reg_no: Optional[str] = None
    c1_remarks: Optional[str] = None

    c2_observation: Optional[str] = None
    c2_remarks: Optional[str] = None

    # ─── Section D - ELECTRICAL AREA ──────────────────────────────────────────

    d1_transformer_yard_gate_closed_observation: Optional[str] = None
    d1_remarks: Optional[str] = None

    d2_authorized_entry_only_observation: Optional[str] = None
    d2_remarks: Optional[str] = None

    d3_any_oil_leak_observed: Optional[str] = None
    d3_remarks: Optional[str] = None

    d4_housekeeping_in_order: Optional[str] = None
    d4_remarks: Optional[str] = None

    d5_temporary_electrical_connection_exists: Optional[str] = None
    d5_remarks: Optional[str] = None

    d6_substation_housekeeping_in_order: Optional[str] = None
    d6_remarks: Optional[str] = None

    # ─── Section E - PRODUCT PUMP HOUSE ───────────────────────────────────────

    e1_electrical_connections_sound: Optional[bool] = None
    e1_remarks: Optional[str] = None

    e2_earthing_proper: Optional[bool] = None
    e2_remarks: Optional[str] = None

    e3_gauges_pumps_working: Optional[bool] = None
    e3_remarks: Optional[str] = None

    e4_safety_guards_in_position: Optional[bool] = None
    e4_remarks: Optional[str] = None

    e5_abnormal_vibration_noise: Optional[bool] = None
    e5_remarks: Optional[str] = None

    e6_portable_extinguishers_in_position: Optional[bool] = None
    e6_remarks: Optional[str] = None

    e7_any_product_leak_unsafe_condition: Optional[bool] = None
    e7_remarks: Optional[str] = None

    e8_housekeeping_in_order: Optional[bool] = None
    e8_remarks: Optional[str] = None

    e9_hydrocarbon_detection_system_working: Optional[bool] = None
    e9_remarks: Optional[str] = None

    e10_last_fire_drill_done_on: Optional[str] = None
    e10_remarks: Optional[str] = None

    e11_fire_water_monitors_hoses_good_condition: Optional[bool] = None
    e11_remarks: Optional[str] = None

    # ─── Section F - Area I (BASKET & METERING) ───────────────────────────────

    f_i_1_no_ignition_sources_visible: Optional[bool] = None
    f_i_1_remarks: Optional[str] = None

    f_i_2_all_electrical_connections_safe: Optional[bool] = None
    f_i_2_remarks: Optional[str] = None

    f_i_3_sprinkler_system_working: Optional[bool] = None
    f_i_3_remarks: Optional[str] = None

    f_i_4_housekeeping_in_order: Optional[bool] = None
    f_i_4_remarks: Optional[str] = None

    f_i_5_ows_tank_farm_functional: Optional[bool] = None
    f_i_5_remarks: Optional[str] = None

    f_i_6_fire_extinguishers_accessible: Optional[bool] = None
    f_i_6_remarks: Optional[str] = None

    f_i_7_any_product_leak_or_unsafe_condition: Optional[bool] = None
    f_i_7_remarks: Optional[str] = None

    f_i_8_fire_water_monitors_hoses_good: Optional[bool] = None
    f_i_8_remarks: Optional[str] = None

    f_i_9_rovs_on_remote_mode: Optional[bool] = None
    f_i_9_remarks: Optional[str] = None

    f_i_10_pressure_temperature_transmitters_functional: Optional[bool] = None
    f_i_10_remarks: Optional[str] = None

    f_i_11_bonding_across_flanges_visible_intact: Optional[bool] = None
    f_i_11_remarks: Optional[str] = None

    f_i_12_last_fire_drill_done: Optional[bool] = None
    f_i_12_remarks: Optional[str] = None

    f_i_13_hydrocarbon_detection_system_working: Optional[bool] = None
    f_i_13_remarks: Optional[str] = None

    # ─── Section F - Area II (PIG RECEIVER) ───────────────────────────────────

    f_ii_1_no_ignition_sources_visible: Optional[bool] = None
    f_ii_1_remarks: Optional[str] = None

    f_ii_2_all_electrical_connections_safe: Optional[bool] = None
    f_ii_2_remarks: Optional[str] = None

    f_ii_3_sprinkler_system_working: Optional[bool] = None
    f_ii_3_remarks: Optional[str] = None

    f_ii_4_housekeeping_in_order: Optional[bool] = None
    f_ii_4_remarks: Optional[str] = None

    f_ii_5_ows_tank_farm_functional: Optional[bool] = None
    f_ii_5_remarks: Optional[str] = None

    f_ii_6_fire_extinguishers_accessible: Optional[bool] = None
    f_ii_6_remarks: Optional[str] = None

    f_ii_7_any_product_leak_or_unsafe_condition: Optional[bool] = None
    f_ii_7_remarks: Optional[str] = None

    f_ii_8_fire_water_monitors_hoses_good: Optional[bool] = None
    f_ii_8_remarks: Optional[str] = None

    f_ii_9_rovs_on_remote_mode: Optional[bool] = None
    f_ii_9_remarks: Optional[str] = None

    f_ii_10_pressure_temperature_transmitters_functional: Optional[bool] = None
    f_ii_10_remarks: Optional[str] = None

    f_ii_11_bonding_across_flanges_visible_intact: Optional[bool] = None
    f_ii_11_remarks: Optional[str] = None

    f_ii_12_last_fire_drill_done: Optional[bool] = None
    f_ii_12_remarks: Optional[str] = None

    f_ii_13_hydrocarbon_detection_system_working: Optional[bool] = None
    f_ii_13_remarks: Optional[str] = None

    # ─── Section F - Area III (TANK FARM) ─────────────────────────────────────

    f_iii_1_no_ignition_sources_visible: Optional[bool] = None
    f_iii_1_remarks: Optional[str] = None

    f_iii_2_all_electrical_connections_safe: Optional[bool] = None
    f_iii_2_remarks: Optional[str] = None

    f_iii_3_sprinkler_system_working: Optional[bool] = None
    f_iii_3_remarks: Optional[str] = None

    f_iii_4_housekeeping_in_order: Optional[bool] = None
    f_iii_4_remarks: Optional[str] = None

    f_iii_5_ows_tank_farm_functional: Optional[bool] = None
    f_iii_5_remarks: Optional[str] = None

    f_iii_6_fire_extinguishers_accessible: Optional[bool] = None
    f_iii_6_remarks: Optional[str] = None

    f_iii_7_any_product_leak_or_unsafe_condition: Optional[bool] = None
    f_iii_7_remarks: Optional[str] = None

    f_iii_8_fire_water_monitors_hoses_good: Optional[bool] = None
    f_iii_8_remarks: Optional[str] = None

    f_iii_9_rovs_on_remote_mode: Optional[bool] = None
    f_iii_9_remarks: Optional[str] = None

    f_iii_10_pressure_temperature_transmitters_functional: Optional[bool] = None
    f_iii_10_remarks: Optional[str] = None

    f_iii_11_bonding_across_flanges_visible_intact: Optional[bool] = None
    f_iii_11_remarks: Optional[str] = None

    f_iii_12_last_fire_drill_done: Optional[bool] = None
    f_iii_12_remarks: Optional[str] = None

    f_iii_13_hydrocarbon_detection_system_working: Optional[bool] = None
    f_iii_13_remarks: Optional[str] = None


    # ─── Section G - SAFETY OBSERVATIONS ─────────────────────────────────────

    g1_product_leak_or_unsafe_condition: Optional[str] = None
    g1_remarks: Optional[str] = None
    g2_housekeeping_in_order: Optional[bool] = None
    g2_remarks: Optional[str] = None


    # ─── Audit fields ──────────────────────────────────────────────────────────

    created_by: Optional[int] = None
    updated_by: Optional[int] = None


class DailySafetyChecklistCreate(DailySafetyChecklistBase):
    pass


class DailySafetyChecklistUpdate(DailySafetyChecklistBase):
    pass


class DailySafetyChecklistResponse(DailySafetyChecklistBase):

    dsc_id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True  # Pydantic v2 (use orm_mode = True for Pydantic v1)