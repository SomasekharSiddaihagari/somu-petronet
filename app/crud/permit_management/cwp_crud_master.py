from datetime import date
from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.sql import text

from app.schemas.permit_management.cwp_schema_master import (
    CompositeWorkPermitCreate,
    CompositeWorkPermitUpdate,
)


# =================================================
# AUTO SERIAL NUMBER GENERATOR
# =================================================
def generate_cwp_serial_number(db: Session, user_id: int) -> str:
    # 1️⃣ Get station_code from user → station
    station_query = text("""
        SELECT s.station_code
        FROM users u
        JOIN station s ON s.station_id = u.station_id
        WHERE u.user_id = :user_id
          AND u.is_deleted = FALSE
    """)
    station = db.execute(station_query, {"user_id": user_id}).mappings().first()

    if not station:
        raise HTTPException(status_code=400, detail="Station not found for this user")

    station_code = station["station_code"]

    # 2️⃣ Calculate financial year
    today = date.today()
    if today.month >= 4:
        fy = f"{today.year}-{str(today.year + 1)[-2:]}"
    else:
        fy = f"{today.year - 1}-{str(today.year)[-2:]}"

    # 3️⃣ Extract MAX sequence from existing serial numbers for this station + FY
    max_query = text("""
        SELECT MAX(
            CAST(
                SPLIT_PART(serial_number, '/', 4) AS INTEGER
            )
        ) AS max_seq
        FROM composite_work_permit
        WHERE serial_number LIKE :pattern
          AND serial_number IS NOT NULL
    """)

    result = db.execute(max_query, {"pattern": f"CWP/{station_code}/{fy}/%"}).mappings().first()

    next_seq = (result["max_seq"] or 0) + 1
    sequence = str(next_seq).zfill(3)

    return f"CWP/{station_code}/{fy}/{sequence}"


# =================================================
# INSERT HISTORY SNAPSHOT
# =================================================
def insert_cwp_history(db: Session, cwp_id: int):
    history_sql = text("""
        INSERT INTO composite_work_permit_history (
            cwp_id, serial_number, location, issued_to, description_of_work,
            work_from_time, work_from_date, work_to_time, work_to_date,
            jsa_id, jsa_ref_no, job_type, cross_reference_permits, isolation_certificate_ref,
            a1_equipment_area_inspected, a1_sub_equipment, a1_sub_work_area,
            a2_surrounding_area_checked,
            a3_sewers_manholes_covered, a3_sub_sewers, a3_sub_manholes, a3_sub_cbd, a3_sub_hot_surface, a3_sub_other, a3_sub_other_text,
            a4_hazards_considered, a5_equipment_drained,
            a6_equipment_steamed_purged, a6_sub_steamed, a6_sub_purged,
            a7_equipment_blinded_isolated, a7_sub_blinded, a7_sub_disconnected, a7_sub_closed, a7_sub_isolated, a7_sub_wedge_opened,
            a8_equipment_water_flushed,
            a9_iron_sulphide_removed, a9_sub_sulphide_removed, a9_sub_kept_wet,
            a10_equipment_electrically_isolated,
            a11_gas_test, a11_val_hcs_percent, a11_val_toxic_gas_ppm, a11_val_o2_percent,
            a12_fire_extinguisher_provided, a12_sub_running_water_hose, a12_sub_fire_extinguisher, a12_sub_fire_water_system,
            a13_area_cordoned, a14_ventilation_lighting,
            b1_escape_provided,
            b2_standby_personnel, b2_sub_process, b2_sub_maint, b2_sub_contractor, b2_sub_fire_dept,
            b3_check_oil_gas_trapped, b4_shield_against_spark, b5_portable_equipment_grounded, b6_standby_for_confined_space,
            c1_peso_spark_elimination, c1_sub_mobile_equipment, c1_sub_vehicle_provided,
            d1_excavation_clearance_obtained, d1_sub_excavation, d1_sub_road_cutting, d1_sub_dyke_cutting,
            hazard_lack_of_o2, hazard_lack_of_h2s, hazard_toxic_gases, hazard_combustible_gases, hazard_pyrophoric_iron, hazard_corrosive_chemicals, hazard_steam_condensate, hazard_other, hazard_other_text,
            ppe_helmet, ppe_safety_shoes, ppe_hand_gloves, ppe_boiler_suit, ppe_cotton_coverall, ppe_face_shield, ppe_fresh_air_mask, ppe_dust_respirator, ppe_apron, ppe_goggles, ppe_earmuff, ppe_lifeline, ppe_safety_belt, ppe_airline, ppe_other, ppe_other_text,
            additional_requirements_precautions,
            requestor_name, requestor_designation, requestor_signature,
            issuer_name, issuer_designation, issuer_signature,
            receiver_name, receiver_designation, receiver_signature,
            electrical_isolation_required, electrical_energization_required,
            toolbox_talk_completed,
            gas_test_from_time, gas_test_to_time, gas_test_from_date, gas_test_to_date,
            gas_hcs_percent, gas_toxic_ppm, gas_o2_percent, gas_additional_precautions,
            gas_requestor_name, gas_requestor_designation, gas_requestor_signature,
            gas_issuer_name, gas_issuer_designation, gas_issuer_signature,
            gas_receiver_name, gas_receiver_designation, gas_receiver_signature,
            closure_requestor_name, closure_requestor_designation, closure_requestor_signature,
            closure_issuer_name, closure_issuer_designation, closure_issuer_signature,
            closure_receiver_name, closure_receiver_designation, closure_receiver_signature,
            status, created_by, updated_by, created_at, updated_at
        )
        SELECT
            cwp_id, serial_number, location, issued_to, description_of_work,
            work_from_time, work_from_date, work_to_time, work_to_date,
            jsa_id, jsa_ref_no, job_type, cross_reference_permits, isolation_certificate_ref,
            a1_equipment_area_inspected, a1_sub_equipment, a1_sub_work_area,
            a2_surrounding_area_checked,
            a3_sewers_manholes_covered, a3_sub_sewers, a3_sub_manholes, a3_sub_cbd, a3_sub_hot_surface, a3_sub_other, a3_sub_other_text,
            a4_hazards_considered, a5_equipment_drained,
            a6_equipment_steamed_purged, a6_sub_steamed, a6_sub_purged,
            a7_equipment_blinded_isolated, a7_sub_blinded, a7_sub_disconnected, a7_sub_closed, a7_sub_isolated, a7_sub_wedge_opened,
            a8_equipment_water_flushed,
            a9_iron_sulphide_removed, a9_sub_sulphide_removed, a9_sub_kept_wet,
            a10_equipment_electrically_isolated,
            a11_gas_test, a11_val_hcs_percent, a11_val_toxic_gas_ppm, a11_val_o2_percent,
            a12_fire_extinguisher_provided, a12_sub_running_water_hose, a12_sub_fire_extinguisher, a12_sub_fire_water_system,
            a13_area_cordoned, a14_ventilation_lighting,
            b1_escape_provided,
            b2_standby_personnel, b2_sub_process, b2_sub_maint, b2_sub_contractor, b2_sub_fire_dept,
            b3_check_oil_gas_trapped, b4_shield_against_spark, b5_portable_equipment_grounded, b6_standby_for_confined_space,
            c1_peso_spark_elimination, c1_sub_mobile_equipment, c1_sub_vehicle_provided,
            d1_excavation_clearance_obtained, d1_sub_excavation, d1_sub_road_cutting, d1_sub_dyke_cutting,
            hazard_lack_of_o2, hazard_lack_of_h2s, hazard_toxic_gases, hazard_combustible_gases, hazard_pyrophoric_iron, hazard_corrosive_chemicals, hazard_steam_condensate, hazard_other, hazard_other_text,
            ppe_helmet, ppe_safety_shoes, ppe_hand_gloves, ppe_boiler_suit, ppe_cotton_coverall, ppe_face_shield, ppe_fresh_air_mask, ppe_dust_respirator, ppe_apron, ppe_goggles, ppe_earmuff, ppe_lifeline, ppe_safety_belt, ppe_airline, ppe_other, ppe_other_text,
            additional_requirements_precautions,
            requestor_name, requestor_designation, requestor_signature,
            issuer_name, issuer_designation, issuer_signature,
            receiver_name, receiver_designation, receiver_signature,
            electrical_isolation_required, electrical_energization_required,
            toolbox_talk_completed,
            gas_test_from_time, gas_test_to_time, gas_test_from_date, gas_test_to_date,
            gas_hcs_percent, gas_toxic_ppm, gas_o2_percent, gas_additional_precautions,
            gas_requestor_name, gas_requestor_designation, gas_requestor_signature,
            gas_issuer_name, gas_issuer_designation, gas_issuer_signature,
            gas_receiver_name, gas_receiver_designation, gas_receiver_signature,
            closure_requestor_name, closure_requestor_designation, closure_requestor_signature,
            closure_issuer_name, closure_issuer_designation, closure_issuer_signature,
            closure_receiver_name, closure_receiver_designation, closure_receiver_signature,
            status, created_by, updated_by, created_at, NOW()
        FROM composite_work_permit
        WHERE cwp_id = :cwp_id
    """)

    db.execute(history_sql, {"cwp_id": cwp_id})


# =================================================
# CREATE (MAIN + HISTORY)
# =================================================
def create_cwp(db: Session, data: CompositeWorkPermitCreate):
    payload = data.model_dump()

    # default updated_by
    if not payload.get("updated_by"):
        payload["updated_by"] = payload["created_by"]

    # serial number
    payload["serial_number"] = generate_cwp_serial_number(
        db,
        int(payload["created_by"])
    )

    insert_sql = text("""
        INSERT INTO composite_work_permit (
            serial_number,
            location,
            issued_to,
            description_of_work,
            work_from_time,
            work_from_date,
            work_to_time,
            work_to_date,

            jsa_id,
            jsa_ref_no,
            job_type,
            cross_reference_permits,
            isolation_certificate_ref,

            a1_equipment_area_inspected,
            a1_sub_equipment,
            a1_sub_work_area,
            a2_surrounding_area_checked,

            a3_sewers_manholes_covered,
            a3_sub_sewers,
            a3_sub_manholes,
            a3_sub_cbd,
            a3_sub_hot_surface,
            a3_sub_other,
            a3_sub_other_text,

            a4_hazards_considered,
            a5_equipment_drained,

            a6_equipment_steamed_purged,
            a6_sub_steamed,
            a6_sub_purged,

            a7_equipment_blinded_isolated,
            a7_sub_blinded,
            a7_sub_disconnected,
            a7_sub_closed,
            a7_sub_isolated,
            a7_sub_wedge_opened,

            a8_equipment_water_flushed,

            a9_iron_sulphide_removed,
            a9_sub_sulphide_removed,
            a9_sub_kept_wet,

            a10_equipment_electrically_isolated,

            a11_gas_test,
            a11_val_hcs_percent,
            a11_val_toxic_gas_ppm,
            a11_val_o2_percent,

            a12_fire_extinguisher_provided,
            a12_sub_running_water_hose,
            a12_sub_fire_extinguisher,
            a12_sub_fire_water_system,

            a13_area_cordoned,
            a14_ventilation_lighting,

            b1_escape_provided,

            b2_standby_personnel,
            b2_sub_process,
            b2_sub_maint,
            b2_sub_contractor,
            b2_sub_fire_dept,

            b3_check_oil_gas_trapped,
            b4_shield_against_spark,
            b5_portable_equipment_grounded,
            b6_standby_for_confined_space,

            c1_peso_spark_elimination,
            c1_sub_mobile_equipment,
            c1_sub_vehicle_provided,

            d1_excavation_clearance_obtained,
            d1_sub_excavation,
            d1_sub_road_cutting,
            d1_sub_dyke_cutting,

            hazard_lack_of_o2,
            hazard_lack_of_h2s,
            hazard_toxic_gases,
            hazard_combustible_gases,
            hazard_pyrophoric_iron,
            hazard_corrosive_chemicals,
            hazard_steam_condensate,
            hazard_other,
            hazard_other_text,

            ppe_helmet,
            ppe_safety_shoes,
            ppe_hand_gloves,
            ppe_boiler_suit,
            ppe_cotton_coverall,
            ppe_face_shield,
            ppe_fresh_air_mask,
            ppe_dust_respirator,
            ppe_apron,
            ppe_goggles,
            ppe_earmuff,
            ppe_lifeline,
            ppe_safety_belt,
            ppe_airline,
            ppe_other,
            ppe_other_text,

            additional_requirements_precautions,

            requestor_name,
            requestor_designation,
            requestor_signature,

            issuer_name,
            issuer_designation,
            issuer_signature,
            issuer_userid,

            receiver_name,
            receiver_designation,
            receiver_signature,
            receiver_userid,

            electrical_isolation_required,
            electrical_energization_required,

            toolbox_talk_completed,

            gas_test_from_time,
            gas_test_to_time,
            gas_test_from_date,
            gas_test_to_date,
            gas_hcs_percent,
            gas_toxic_ppm,
            gas_o2_percent,
            gas_additional_precautions,

            gas_requestor_name,
            gas_requestor_designation,
            gas_requestor_signature,
            gas_requestor_userid,

            gas_issuer_name,
            gas_issuer_designation,
            gas_issuer_signature,
            gas_issuer_userid,

            gas_receiver_name,
            gas_receiver_designation,
            gas_receiver_signature,
            gas_receiver_userid,

            closure_requestor_name,
            closure_requestor_designation,
            closure_requestor_signature,
            closure_requestor_userid,

            closure_issuer_name,
            closure_issuer_designation,
            closure_issuer_signature,
            closure_issuer_userid,

            closure_receiver_name,
            closure_receiver_designation,
            closure_receiver_signature,
            closure_receiver_userid,

            status,
            created_by,
            updated_by
        )

        VALUES (
            :serial_number,
            :location,
            :issued_to,
            :description_of_work,
            :work_from_time,
            :work_from_date,
            :work_to_time,
            :work_to_date,

            :jsa_id,
            :jsa_ref_no,
            :job_type,
            :cross_reference_permits,
            :isolation_certificate_ref,

            :a1_equipment_area_inspected,
            :a1_sub_equipment,
            :a1_sub_work_area,
            :a2_surrounding_area_checked,

            :a3_sewers_manholes_covered,
            :a3_sub_sewers,
            :a3_sub_manholes,
            :a3_sub_cbd,
            :a3_sub_hot_surface,
            :a3_sub_other,
            :a3_sub_other_text,

            :a4_hazards_considered,
            :a5_equipment_drained,

            :a6_equipment_steamed_purged,
            :a6_sub_steamed,
            :a6_sub_purged,

            :a7_equipment_blinded_isolated,
            :a7_sub_blinded,
            :a7_sub_disconnected,
            :a7_sub_closed,
            :a7_sub_isolated,
            :a7_sub_wedge_opened,

            :a8_equipment_water_flushed,

            :a9_iron_sulphide_removed,
            :a9_sub_sulphide_removed,
            :a9_sub_kept_wet,

            :a10_equipment_electrically_isolated,

            :a11_gas_test,
            :a11_val_hcs_percent,
            :a11_val_toxic_gas_ppm,
            :a11_val_o2_percent,

            :a12_fire_extinguisher_provided,
            :a12_sub_running_water_hose,
            :a12_sub_fire_extinguisher,
            :a12_sub_fire_water_system,

            :a13_area_cordoned,
            :a14_ventilation_lighting,

            :b1_escape_provided,

            :b2_standby_personnel,
            :b2_sub_process,
            :b2_sub_maint,
            :b2_sub_contractor,
            :b2_sub_fire_dept,

            :b3_check_oil_gas_trapped,
            :b4_shield_against_spark,
            :b5_portable_equipment_grounded,
            :b6_standby_for_confined_space,

            :c1_peso_spark_elimination,
            :c1_sub_mobile_equipment,
            :c1_sub_vehicle_provided,

            :d1_excavation_clearance_obtained,
            :d1_sub_excavation,
            :d1_sub_road_cutting,
            :d1_sub_dyke_cutting,

            :hazard_lack_of_o2,
            :hazard_lack_of_h2s,
            :hazard_toxic_gases,
            :hazard_combustible_gases,
            :hazard_pyrophoric_iron,
            :hazard_corrosive_chemicals,
            :hazard_steam_condensate,
            :hazard_other,
            :hazard_other_text,

            :ppe_helmet,
            :ppe_safety_shoes,
            :ppe_hand_gloves,
            :ppe_boiler_suit,
            :ppe_cotton_coverall,
            :ppe_face_shield,
            :ppe_fresh_air_mask,
            :ppe_dust_respirator,
            :ppe_apron,
            :ppe_goggles,
            :ppe_earmuff,
            :ppe_lifeline,
            :ppe_safety_belt,
            :ppe_airline,
            :ppe_other,
            :ppe_other_text,

            :additional_requirements_precautions,

            :requestor_name,
            :requestor_designation,
            :requestor_signature,

            :issuer_name,
            :issuer_designation,
            :issuer_signature,
            :issuer_userid,

            :receiver_name,
            :receiver_designation,
            :receiver_signature,
            :receiver_userid,

            :electrical_isolation_required,
            :electrical_energization_required,

            :toolbox_talk_completed,

            :gas_test_from_time,
            :gas_test_to_time,
            :gas_test_from_date,
            :gas_test_to_date,
            :gas_hcs_percent,
            :gas_toxic_ppm,
            :gas_o2_percent,
            :gas_additional_precautions,

            :gas_requestor_name,
            :gas_requestor_designation,
            :gas_requestor_signature,
            :gas_requestor_userid,

            :gas_issuer_name,
            :gas_issuer_designation,
            :gas_issuer_signature,
            :gas_issuer_userid,

            :gas_receiver_name,
            :gas_receiver_designation,
            :gas_receiver_signature,
            :gas_receiver_userid,

            :closure_requestor_name,
            :closure_requestor_designation,
            :closure_requestor_signature,
            :closure_requestor_userid,

            :closure_issuer_name,
            :closure_issuer_designation,
            :closure_issuer_signature,
            :closure_issuer_userid,

            :closure_receiver_name,
            :closure_receiver_designation,
            :closure_receiver_signature,
            :closure_receiver_userid,

            :status,
            :created_by,
            :updated_by
        )
        RETURNING cwp_id
    """)

    result = db.execute(insert_sql, payload)
    cwp_id = result.scalar()

    insert_cwp_history(db, cwp_id)
    db.commit()

    return {
        "cwp_id": cwp_id,
        "serial_number": payload["serial_number"]
    }


# =================================================
# UPDATE (MAIN + HISTORY)
# =================================================
def update_cwp(db: Session, cwp_id: int, data: CompositeWorkPermitUpdate):
    payload = data.model_dump(exclude_unset=True)

    if not payload:
        return False

    set_clause = ", ".join([f"{k} = :{k}" for k in payload.keys()])

    update_sql = text(f"""
        UPDATE composite_work_permit
        SET {set_clause},
            updated_at = NOW()
        WHERE cwp_id = :cwp_id
    """)

    payload["cwp_id"] = cwp_id
    db.execute(update_sql, payload)

    insert_cwp_history(db, cwp_id)
    db.commit()

    return True
