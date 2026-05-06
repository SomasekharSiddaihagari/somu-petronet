from datetime import datetime
from sqlalchemy import Column, Integer, String, Date, Time, DateTime, Boolean, Text, func
from sqlalchemy.ext.declarative import declarative_base
 
Base = declarative_base()
 
class DailySafetyChecklist(Base):
    __tablename__ = "daily_safety_checklist"
 
    dsc_id = Column(Integer, primary_key=True, autoincrement=True)
    doc_no = Column(String(50), nullable=True)
    shift = Column(String(10), nullable=True)
    start_time = Column(Time, nullable=True)
    station = Column(String(100), nullable=True)
    station_in_charge = Column(String(100), nullable=True)
    checklist_date = Column(Date, nullable=True)           # renamed from date to avoid conflict
    prepared_by_name = Column(String(100), nullable=True)
    reviewed_by_name = Column(String(100), nullable=True)
    ms_logbook_id = Column(Integer, nullable=True)
 
    # ─────────────────────────────────────────────────────────────
    # Section B - SECURITY GATE - FIRE SAFETY
    # ─────────────────────────────────────────────────────────────
    b1_water_level_satisfactory = Column(Boolean, nullable=True)
    b1_water_level_remarks = Column(Text, nullable=True)
    b1_water_tank_level_1 = Column(String(50), nullable=True)
    b1_water_tank_level_2 = Column(String(50), nullable=True)
    b1_water_tank_level_3 = Column(String(50), nullable=True)


    b2_hydrant_pressure_maintained = Column(Boolean, nullable=True)
    b2_hydrant_pressure_value = Column(Text, nullable=True)
 

    b3_fire_pump_diesel_batteries_good = Column(Boolean, nullable=True)
    b3_diesel_tank_level_1 = Column(String(50), nullable=True)
    b3_diesel_tank_level_2 = Column(String(50), nullable=True)
    b3_diesel_tank_level_3 = Column(String(50), nullable=True)
    b3_valves_fully_open = Column(String(250), nullable=True)
    b3_one_pump_start_pressure = Column(String(50), nullable=True)
    b3_auto_start_system_developed = Column(Boolean, nullable=True)
    b3_fire_water_pumps_egines_remarks = Column(Text, nullable=True)
 

    b4_fire_alarm_communication_working = Column(Boolean, nullable=True)
    b4_remarks = Column(Text, nullable=True)
 

    b5_clean_agent_system_cylinders_filled = Column(Boolean, nullable=True)
    b5_remarks = Column(Text, nullable=True)
 
    b6_any_unsafe_condition_fire_protection = Column(Boolean, nullable=True)
    b6_remarks = Column(Text, nullable=True)
 
    b7_regular_surprise_check_testing_done = Column(Boolean, nullable=True)
    b7_remarks = Column(Text, nullable=True)
 
    b8_wind_direction_displayed = Column(Boolean, nullable=True)
    b8_remarks = Column(Text, nullable=True)
 
    b9_caution_signs_displayed = Column(Boolean, nullable=True)
    b9_remarks = Column(Text, nullable=True)
 
    b10_fire_extinguishers_in_place_upto_date = Column(Boolean, nullable=True)
    b10_remarks = Column(Text, nullable=True)
 
    b11_cctv_functioning = Column(Boolean, nullable=True)
    b11_remarks = Column(Text, nullable=True)
 
    # ─────────────────────────────────────────────────────────────
    # Section B - SECURITY GATE - SECURITY CHECKS
    # ─────────────────────────────────────────────────────────────
    b_sec1_frisking_observation = Column(Text, nullable=True)
    b_sec1_frisking_remarks = Column(Text, nullable=True)
 
    b_sec2_boundary_wall_integrity_observation = Column(Text, nullable=True)
    b_sec2_remarks = Column(Text, nullable=True)
 
    b_sec3_emergency_gate_check_observation = Column(Text, nullable=True)
    b_sec3_remarks = Column(Text, nullable=True)
 
    b_sec4_ppe_usage_hazardous_area_observation = Column(Text, nullable=True)
    b_sec4_remarks = Column(Text, nullable=True)
 
    # ─────────────────────────────────────────────────────────────
    # Section C - EMERGENCY VEHICLE
    # ─────────────────────────────────────────────────────────────
    c1_emergency_response_vehicle_reg_no = Column(String(50), nullable=True)
    c1_emergency_maintenance_vehicle_reg_no = Column(String(50), nullable=True)
    c1_fire_tender_reg_no = Column(String(50), nullable=True)
    c1_gypsy_reg_no = Column(String(50), nullable=True)
    c1_observation = Column(Text, nullable=True)
    c1_remarks = Column(Text, nullable=True)
 
    c2_observation = Column(Text, nullable=True)
    c2_remarks = Column(Text, nullable=True)
 
    # ─────────────────────────────────────────────────────────────
    # Section D - ELECTRICAL AREA
    # ─────────────────────────────────────────────────────────────
    d1_transformer_yard_gate_closed_observation = Column(Text, nullable=True)
    d1_remarks = Column(Text, nullable=True)
 
    d2_authorized_entry_only_observation = Column(Text, nullable=True)
    d2_remarks = Column(Text, nullable=True)
 
    d3_any_oil_leak_observed = Column(Text, nullable=True)
    d3_remarks = Column(Text, nullable=True)
 
    d4_housekeeping_in_order = Column(Text, nullable=True)
    d4_remarks = Column(Text, nullable=True)
 
    d5_temporary_electrical_connection_exists = Column(Text, nullable=True)
    d5_remarks = Column(Text, nullable=True)
 
    d6_substation_housekeeping_in_order = Column(Text, nullable=True)
    d6_remarks = Column(Text, nullable=True)
 
    # ─────────────────────────────────────────────────────────────
    # Section E - PRODUCT PUMP HOUSE
    # ─────────────────────────────────────────────────────────────
    e1_electrical_connections_sound = Column(Boolean, nullable=True)
    e1_remarks = Column(Text, nullable=True)
 
    e2_earthing_proper = Column(Boolean, nullable=True)
    e2_remarks = Column(Text, nullable=True)
 
    e3_gauges_pumps_working = Column(Boolean, nullable=True)
    e3_remarks = Column(Text, nullable=True)
 
    e4_safety_guards_in_position = Column(Boolean, nullable=True)
    e4_remarks = Column(Text, nullable=True)
 
    e5_abnormal_vibration_noise = Column(Boolean, nullable=True)
    e5_remarks = Column(Text, nullable=True)
 
    e6_portable_extinguishers_in_position = Column(Boolean, nullable=True)
    e6_remarks = Column(Text, nullable=True)
 
    e7_any_product_leak_unsafe_condition = Column(Boolean, nullable=True)
    e7_remarks = Column(Text, nullable=True)
 
    e8_housekeeping_in_order = Column(Boolean, nullable=True)
    e8_remarks = Column(Text, nullable=True)
 
    e9_hydrocarbon_detection_system_working = Column(Boolean, nullable=True)
    e9_remarks = Column(Text, nullable=True)
 
    e10_last_fire_drill_done_on = Column(String(50), nullable=True)
    e10_remarks = Column(Text, nullable=True)
 
    e11_fire_water_monitors_hoses_good_condition = Column(Boolean, nullable=True)
    e11_remarks = Column(Text, nullable=True)
 
    # ─────────────────────────────────────────────────────────────
    # Section F - BASKET & METERING (I) / PIG RECEIVER (II) / TANK FARM (III)
    # Each item: Yes/No + Remarks — for all 3 areas
    # ─────────────────────────────────────────────────────────────
 
    # Area I ────────────────────────────────────────────────
    f_i_1_no_ignition_sources_visible = Column(Boolean, nullable=True)
    f_i_1_remarks = Column(Text, nullable=True)
 
    f_i_2_all_electrical_connections_safe = Column(Boolean, nullable=True)
    f_i_2_remarks = Column(Text, nullable=True)
 
    f_i_3_sprinkler_system_working = Column(Boolean, nullable=True)
    f_i_3_remarks = Column(Text, nullable=True)
 
    f_i_4_housekeeping_in_order = Column(Boolean, nullable=True)
    f_i_4_remarks = Column(Text, nullable=True)
 
    f_i_5_ows_tank_farm_functional = Column(Boolean, nullable=True)
    f_i_5_remarks = Column(Text, nullable=True)
 
    f_i_6_fire_extinguishers_accessible = Column(Boolean, nullable=True)
    f_i_6_remarks = Column(Text, nullable=True)
 
    f_i_7_any_product_leak_or_unsafe_condition = Column(Boolean, nullable=True)
    f_i_7_remarks = Column(Text, nullable=True)
 
    f_i_8_fire_water_monitors_hoses_good = Column(Boolean, nullable=True)
    f_i_8_remarks = Column(Text, nullable=True)
 
    f_i_9_rovs_on_remote_mode = Column(Boolean, nullable=True)
    f_i_9_remarks = Column(Text, nullable=True)
 
    f_i_10_pressure_temperature_transmitters_functional = Column(Boolean, nullable=True)
    f_i_10_remarks = Column(Text, nullable=True)
 
    f_i_11_bonding_across_flanges_visible_intact = Column(Boolean, nullable=True)
    f_i_11_remarks = Column(Text, nullable=True)
 
    f_i_12_last_fire_drill_done = Column(Boolean, nullable=True)
    f_i_12_remarks = Column(Text, nullable=True)
 
    f_i_13_hydrocarbon_detection_system_working = Column(Boolean, nullable=True)
    f_i_13_remarks = Column(Text, nullable=True)
 
    # Area II ────────────────────────────────────────────────
    f_ii_1_no_ignition_sources_visible = Column(Boolean, nullable=True)
    f_ii_1_remarks = Column(Text, nullable=True)
 
    f_ii_2_all_electrical_connections_safe = Column(Boolean, nullable=True)
    f_ii_2_remarks = Column(Text, nullable=True)
 
    f_ii_3_sprinkler_system_working = Column(Boolean, nullable=True)
    f_ii_3_remarks = Column(Text, nullable=True)
 
    f_ii_4_housekeeping_in_order = Column(Boolean, nullable=True)
    f_ii_4_remarks = Column(Text, nullable=True)
 
    f_ii_5_ows_tank_farm_functional = Column(Boolean, nullable=True)
    f_ii_5_remarks = Column(Text, nullable=True)
 
    f_ii_6_fire_extinguishers_accessible = Column(Boolean, nullable=True)
    f_ii_6_remarks = Column(Text, nullable=True)
 
    f_ii_7_any_product_leak_or_unsafe_condition = Column(Boolean, nullable=True)
    f_ii_7_remarks = Column(Text, nullable=True)
 
    f_ii_8_fire_water_monitors_hoses_good = Column(Boolean, nullable=True)
    f_ii_8_remarks = Column(Text, nullable=True)
 
    f_ii_9_rovs_on_remote_mode = Column(Boolean, nullable=True)
    f_ii_9_remarks = Column(Text, nullable=True)
 
    f_ii_10_pressure_temperature_transmitters_functional = Column(Boolean, nullable=True)
    f_ii_10_remarks = Column(Text, nullable=True)
 
    f_ii_11_bonding_across_flanges_visible_intact = Column(Boolean, nullable=True)
    f_ii_11_remarks = Column(Text, nullable=True)
 
    f_ii_12_last_fire_drill_done = Column(Boolean, nullable=True)
    f_ii_12_remarks = Column(Text, nullable=True)
 
    f_ii_13_hydrocarbon_detection_system_working = Column(Boolean, nullable=True)
    f_ii_13_remarks = Column(Text, nullable=True)
 
    # Area III ────────────────────────────────────────────────
    f_iii_1_no_ignition_sources_visible = Column(Boolean, nullable=True)
    f_iii_1_remarks = Column(Text, nullable=True)
 
    f_iii_2_all_electrical_connections_safe = Column(Boolean, nullable=True)
    f_iii_2_remarks = Column(Text, nullable=True)
 
    f_iii_3_sprinkler_system_working = Column(Boolean, nullable=True)
    f_iii_3_remarks = Column(Text, nullable=True)
 
    f_iii_4_housekeeping_in_order = Column(Boolean, nullable=True)
    f_iii_4_remarks = Column(Text, nullable=True)
 
    f_iii_5_ows_tank_farm_functional = Column(Boolean, nullable=True)
    f_iii_5_remarks = Column(Text, nullable=True)
 
    f_iii_6_fire_extinguishers_accessible = Column(Boolean, nullable=True)
    f_iii_6_remarks = Column(Text, nullable=True)
 
    f_iii_7_any_product_leak_or_unsafe_condition = Column(Boolean, nullable=True)
    f_iii_7_remarks = Column(Text, nullable=True)
 
    f_iii_8_fire_water_monitors_hoses_good = Column(Boolean, nullable=True)
    f_iii_8_remarks = Column(Text, nullable=True)
 
    f_iii_9_rovs_on_remote_mode = Column(Boolean, nullable=True)
    f_iii_9_remarks = Column(Text, nullable=True)
 
    f_iii_10_pressure_temperature_transmitters_functional = Column(Boolean, nullable=True)
    f_iii_10_remarks = Column(Text, nullable=True)
 
    f_iii_11_bonding_across_flanges_visible_intact = Column(Boolean, nullable=True)
    f_iii_11_remarks = Column(Text, nullable=True)
 
    f_iii_12_last_fire_drill_done = Column(Boolean, nullable=True)
    f_iii_12_remarks = Column(Text, nullable=True)
 
    f_iii_13_hydrocarbon_detection_system_working = Column(Boolean, nullable=True)
    f_iii_13_remarks = Column(Text, nullable=True)


     # ─────────────────────────────────────────────────────────────
    # Section G - STATION LIMITING VALVE (SLV)
    # ─────────────────────────────────────────────────────────────
    g1_product_leak_or_unsafe_condition = Column(Text, nullable=True)
    g1_remarks = Column(Text, nullable=True)

    g2_housekeeping_in_order = Column(Boolean, nullable=True)
    g2_remarks = Column(Text, nullable=True)

    acknowledge_id = Column(String(255), nullable=True)
    acknowledge_date = Column(DateTime, nullable=True)
    acknowledge_by = Column(Integer, nullable=True)




    created_at = Column(DateTime, server_default=func.now(), nullable=True)
    created_by = Column(Integer, nullable=True)
    updated_at = Column(DateTime,nullable=True)
    updated_by = Column(Integer, nullable=True)
 
 
 
 
 
 