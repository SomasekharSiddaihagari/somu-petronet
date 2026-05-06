from sqlalchemy import Column, Integer, String, Date, Time, DateTime, Boolean, Text, Float, func
from app.database import Base
from datetime import datetime

class CompositeWorkPermit(Base):
    __tablename__ = "composite_work_permit_history"

    history_id = Column(Integer, primary_key=True, autoincrement=True)
    cwp_id = Column(Integer, nullable=True)
    jsa_id = Column(Integer, nullable=True)


    # =================================================
    # BASIC INFORMATION
    # =================================================
    serial_number = Column(String(100), nullable=True)
    location = Column(String(255), nullable=True)
    contractor_id = Column(Integer, nullable=True)
    engineer_id = Column(Integer, nullable=True)
    issued_to = Column(String(255), nullable=True)  # Dept/Section/Contractor
    description_of_work = Column(Text, nullable=True)

    work_from_time = Column(Time, nullable=True)
    work_from_date = Column(Date, nullable=True)
    work_to_time = Column(Time, nullable=True)
    work_to_date = Column(Date, nullable=True)
    job_type = Column(String(100), nullable=True)

    jsa_ref_no = Column(String(100), nullable=True)
    cross_reference_permits = Column(String(100), nullable=True)
    isolation_certificate_ref = Column(String(100), nullable=True)

    # =================================================
    # WORK CHECKLIST - A. General points for cold work
    # (Store as Done / Not Req / NULL)
    # =================================================
    a1_equipment_area_inspected = Column(String(20), nullable=True)
    a1_sub_equipment = Column(Boolean, default=False)
    a1_sub_work_area = Column(Boolean, default=False)

    a2_surrounding_area_checked = Column(String(20), nullable=True)

    a3_sewers_manholes_covered = Column(String(20), nullable=True)
    a3_sub_sewers = Column(Boolean, default=False)
    a3_sub_manholes = Column(Boolean, default=False)
    a3_sub_cbd = Column(Boolean, default=False)
    a3_sub_hot_surface = Column(Boolean, default=False)
    a3_sub_other = Column(Boolean, default=False)
    a3_sub_other_text = Column(String(255), nullable=True)

    a4_hazards_considered = Column(String(20), nullable=True)

    a5_equipment_drained = Column(String(20), nullable=True)

    a6_equipment_steamed_purged = Column(String(20), nullable=True)
    a6_sub_steamed = Column(Boolean, default=False)
    a6_sub_purged = Column(Boolean, default=False)

    a7_equipment_blinded_isolated = Column(String(20), nullable=True)
    a7_sub_blinded = Column(Boolean, default=False)
    a7_sub_disconnected = Column(Boolean, default=False)
    a7_sub_closed = Column(Boolean, default=False)
    a7_sub_isolated = Column(Boolean, default=False)
    a7_sub_wedge_opened = Column(Boolean, default=False)

    a8_equipment_water_flushed = Column(String(20), nullable=True)

    a9_iron_sulphide_removed = Column(String(20), nullable=True)
    a9_sub_sulphide_removed = Column(Boolean, default=False)
    a9_sub_kept_wet = Column(Boolean, default=False)

    a10_equipment_electrically_isolated = Column(String(20), nullable=True)

    a11_gas_test = Column(String(20), nullable=True)
    a11_val_hcs_percent = Column(String(50), nullable=True)
    a11_val_toxic_gas_ppm = Column(String(50), nullable=True)
    a11_val_o2_percent = Column(String(50), nullable=True)

    a12_fire_extinguisher_provided = Column(String(20), nullable=True)
    a12_sub_running_water_hose = Column(Boolean, default=False)
    a12_sub_fire_extinguisher = Column(Boolean, default=False)
    a12_sub_fire_water_system = Column(Boolean, default=False)

    a13_area_cordoned = Column(String(20), nullable=True)

    a14_ventilation_lighting = Column(String(20), nullable=True)

    # =================================================
    # B. For Hot work / Entry to confined space
    # =================================================
    b1_escape_provided = Column(String(20), nullable=True)

    b2_standby_personnel = Column(String(20), nullable=True)
    b2_sub_process = Column(Boolean, default=False)
    b2_sub_maint = Column(Boolean, default=False)
    b2_sub_contractor = Column(Boolean, default=False)
    b2_sub_fire_dept = Column(Boolean, default=False)

    b3_check_oil_gas_trapped = Column(String(20), nullable=True)

    b4_shield_against_spark = Column(String(20), nullable=True)

    b5_portable_equipment_grounded = Column(String(20), nullable=True)

    b6_standby_for_confined_space = Column(String(20), nullable=True)

    # =================================================
    # C. For Vehicle Entry
    # =================================================
    c1_peso_spark_elimination = Column(String(20), nullable=True)
    c1_sub_mobile_equipment = Column(Boolean, default=False)
    c1_sub_vehicle_provided = Column(Boolean, default=False)

    # =================================================
    # D. For Excavation works
    # =================================================
    d1_excavation_clearance_obtained = Column(String(20), nullable=True)
    d1_sub_excavation = Column(Boolean, default=False)
    d1_sub_road_cutting = Column(Boolean, default=False)
    d1_sub_dyke_cutting = Column(Boolean, default=False)

    # =================================================
    # RESIDUAL HAZARDS
    # =================================================
    hazard_lack_of_o2 = Column(Boolean, default=False)
    hazard_lack_of_h2s = Column(Boolean, default=False)
    hazard_toxic_gases = Column(Boolean, default=False)
    hazard_combustible_gases = Column(Boolean, default=False)
    hazard_pyrophoric_iron = Column(Boolean, default=False)
    hazard_corrosive_chemicals = Column(Boolean, default=False)
    hazard_steam_condensate = Column(Boolean, default=False)
    hazard_other = Column(Boolean, default=False)
    hazard_other_text = Column(String(255), nullable=True)

    # =================================================
    # PPES
    # =================================================
    ppe_helmet = Column(Boolean, default=False)
    ppe_safety_shoes = Column(Boolean, default=False)
    ppe_hand_gloves = Column(Boolean, default=False)
    ppe_boiler_suit = Column(Boolean, default=False)
    ppe_cotton_coverall = Column(Boolean, default=False)
    ppe_face_shield = Column(Boolean, default=False)
    ppe_fresh_air_mask = Column(Boolean, default=False)
    ppe_dust_respirator = Column(Boolean, default=False)
    ppe_apron = Column(Boolean, default=False)
    ppe_goggles = Column(Boolean, default=False)
    ppe_earmuff = Column(Boolean, default=False)
    ppe_lifeline = Column(Boolean, default=False)
    ppe_safety_belt = Column(Boolean, default=False)
    ppe_airline = Column(Boolean, default=False)
    ppe_other = Column(Boolean, default=False)
    ppe_other_text = Column(String(255), nullable=True)

    # =================================================
    # REMARKS / HAZARDS / PPE
    # =================================================

    additional_requirements_precautions = Column(Text, nullable=True)

    # =================================================
    # AUTHORIZATION SIGNATURES
    # =================================================
    requestor_name = Column(String(150), nullable=True)
    requestor_designation = Column(String(150), nullable=True)
    requestor_signature = Column(String(255), nullable=True)

    issuer_name = Column(String(150), nullable=True)
    issuer_designation = Column(String(150), nullable=True)
    issuer_signature = Column(String(255), nullable=True)

    receiver_name = Column(String(150), nullable=True)
    receiver_designation = Column(String(150), nullable=True)
    receiver_signature = Column(String(255), nullable=True)

    # =================================================
    # ELECTRICAL PERMITS
    # =================================================
    electrical_isolation_required = Column(Boolean, nullable=True)
    electrical_energization_required = Column(Boolean, nullable=True)

    # =================================================
    # GAS TEST & ADDITIONAL PRECAUTIONS (SUMMARY FIELDS)
    # (Full grid can be normalized later if needed)
    # =================================================
    gas_test_from_time = Column(Time, nullable=True)
    gas_test_to_time = Column(Time, nullable=True)
    gas_test_from_date = Column(Date, nullable=True)
    gas_test_to_date = Column(Date, nullable=True)

    gas_hcs_percent = Column(String(50), nullable=True)
    gas_toxic_ppm = Column(String(50), nullable=True)
    gas_o2_percent = Column(String(50), nullable=True)

    gas_additional_precautions = Column(Text, nullable=True)

    gas_requestor_name = Column(String(150), nullable=True)
    gas_requestor_designation = Column(String(150), nullable=True)
    gas_requestor_signature = Column(String(255), nullable=True)

    gas_issuer_name = Column(String(150), nullable=True)
    gas_issuer_designation = Column(String(150), nullable=True)
    gas_issuer_signature = Column(String(255), nullable=True)

    gas_receiver_name = Column(String(150), nullable=True)
    gas_receiver_designation = Column(String(150), nullable=True)
    gas_receiver_signature = Column(String(255), nullable=True)

    # =================================================
    # TOOLBOX TALK
    # =================================================
    toolbox_talk_completed = Column(Boolean, nullable=True)

    # =================================================
    # CLOSURE SIGNATURES
    # =================================================
    closure_requestor_name = Column(String(150), nullable=True)
    closure_requestor_designation = Column(String(150), nullable=True)
    closure_requestor_signature = Column(String(255), nullable=True)

    closure_issuer_name = Column(String(150), nullable=True)
    closure_issuer_designation = Column(String(150), nullable=True)
    closure_issuer_signature = Column(String(255), nullable=True)

    closure_receiver_name = Column(String(150), nullable=True)
    closure_receiver_designation = Column(String(150), nullable=True)
    closure_receiver_signature = Column(String(255), nullable=True)

    # =================================================
    # SYSTEM
    # =================================================
    status = Column(String(50), nullable=True)  # Draft / Submitted / Approved / Closed
    created_by = Column(String(100), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=True)
    updated_by = Column(String(100), nullable=True)
    updated_at = Column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=True
    )
