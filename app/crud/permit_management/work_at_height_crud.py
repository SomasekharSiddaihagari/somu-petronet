from datetime import date
from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.sql import text

from app.schemas.permit_management.work_at_height_schema import (
    WorkAtHeightPermitCreate,
    WorkAtHeightPermitUpdate
)


# =================================================
# AUTO SERIAL NUMBER GENERATOR
# =================================================
def generate_serial_number(db: Session, user_id: int) -> str:

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

    today = date.today()
    if today.month >= 4:
        fy = f"{today.year}-{str(today.year + 1)[-2:]}"
    else:
        fy = f"{today.year - 1}-{str(today.year)[-2:]}"

    max_query = text("""
        SELECT MAX(
            CAST(
                SPLIT_PART(serial_number, '/', 4) AS INTEGER
            )
        ) AS max_seq
        FROM work_at_height_permit
        WHERE serial_number LIKE :pattern
          AND serial_number IS NOT NULL
    """)

    result = db.execute(max_query, {
        "pattern": f"WAH/{station_code}/{fy}/%"
    }).mappings().first()

    next_seq = (result["max_seq"] or 0) + 1
    sequence = str(next_seq).zfill(3)

    return f"WAH/{station_code}/{fy}/{sequence}"


# =================================================
# HISTORY SNAPSHOT INSERT
# =================================================
def insert_work_at_height_history(db: Session, whp_id: int):
    history_sql = text("""
        INSERT INTO work_at_height_permit_history (
            whp_id,
            serial_number,
            section_contractor_name,
            nature_of_work,
            work_from_time,
            work_from_date,
            work_to_time,
            work_to_date,
            location,
            jsa_id,

            sc1_equipment_work_area_inspected,
            sc2_surrounding_area_checked,
            sc3_sewers_manholes_covered,
            sc4_scaffolds_ladders_checked,
            sc5_materials_fall_protected,
            sc6_isi_marked_belts_helmets,
            sc7_contractor_fit_for_height,
            sc8_instructions_given,
            sc9_proper_illumination,
            sc10_adequate_platform_space,
            sc11_proper_exit_means,
            sc12_precautionary_tags_boards,
            sc13_portable_equipment_earthed,
            sc14_elcb_switches_provided,
            sc14_additional_safety_measures,
            sc15_standby_supervision_provided,
            sc16_workers_trained_safety_belts,
            sc17_operations_incharge_informed,
            sc18_area_cordoned_off,
            sc19_precautions_against_public_traffic,
            sc20_fire_extinguisher_provided,
            sc20_condition_fav_elevation_work,

            special_instructions,
            additional_remarks,

            issuer_designation,
            issuer_name,
            issuer_signature,

            requestor_name,
            requestor_designation,
            requestor_signature,

            receiver_role,
            receiver_name,
            receiver_designation,
            receiver_signature,

            electrical_isolation_required,
            electrical_energization_required,
            toolbox_talk_required,

            renewal_from_date,
            renewal_from_time,
            renewal_to_date,
            renewal_to_time,
            renewal_issuer_name,
            renewal_issuer_designation,
            renewal_issuer_signature,
            renewal_requestor_name,
            renewal_requestor_designation,
            renewal_requestor_signature,
            renewal_receiver_name,
            renewal_receiver_designation,
            renewal_receiver_signature,
            renewal_toolbox_talk,

            closure_issuer_designation,
            closure_issuer_name,
            closure_issuer_signature,
            closure_requestor_name,
            closure_requestor_designation,
            closure_requestor_signature,
            closure_receiver_role,
            closure_receiver_name,
            closure_receiver_signature,

            job_completion_time,
            job_completion_date,
            work_status,

            status,
            created_by,
            updated_by,
            created_at,
            updated_at
        )
        SELECT
            whp_id,
            serial_number,
            section_contractor_name,
            nature_of_work,
            work_from_time,
            work_from_date,
            work_to_time,
            work_to_date,
            location,
            jsa_id,

            sc1_equipment_work_area_inspected,
            sc2_surrounding_area_checked,
            sc3_sewers_manholes_covered,
            sc4_scaffolds_ladders_checked,
            sc5_materials_fall_protected,
            sc6_isi_marked_belts_helmets,
            sc7_contractor_fit_for_height,
            sc8_instructions_given,
            sc9_proper_illumination,
            sc10_adequate_platform_space,
            sc11_proper_exit_means,
            sc12_precautionary_tags_boards,
            sc13_portable_equipment_earthed,
            sc14_elcb_switches_provided,
            sc14_additional_safety_measures,
            sc15_standby_supervision_provided,
            sc16_workers_trained_safety_belts,
            sc17_operations_incharge_informed,
            sc18_area_cordoned_off,
            sc19_precautions_against_public_traffic,
            sc20_fire_extinguisher_provided,
            sc20_condition_fav_elevation_work,

            special_instructions,
            additional_remarks,

            issuer_designation,
            issuer_name,
            issuer_signature,

            requestor_name,
            requestor_designation,
            requestor_signature,

            receiver_role,
            receiver_name,
            receiver_designation,
            receiver_signature,

            electrical_isolation_required,
            electrical_energization_required,
            toolbox_talk_required,

            renewal_from_date,
            renewal_from_time,
            renewal_to_date,
            renewal_to_time,
            renewal_issuer_name,
            renewal_issuer_designation,
            renewal_issuer_signature,
            renewal_requestor_name,
            renewal_requestor_designation,
            renewal_requestor_signature,
            renewal_receiver_name,
            renewal_receiver_designation,
            renewal_receiver_signature,
            renewal_toolbox_talk,

            closure_issuer_designation,
            closure_issuer_name,
            closure_issuer_signature,
            closure_requestor_name,
            closure_requestor_designation,
            closure_requestor_signature,
            closure_receiver_role,
            closure_receiver_name,
            closure_receiver_signature,

            job_completion_time,
            job_completion_date,
            work_status,

            status,
            created_by,
            updated_by,
            created_at,
            NOW()
        FROM work_at_height_permit
        WHERE whp_id = :whp_id
    """)

    db.execute(history_sql, {"whp_id": whp_id})


# =================================================
# CREATE (MAIN + HISTORY)
# =================================================
def create_work_at_height(db: Session, data: WorkAtHeightPermitCreate):
    payload = data.model_dump()

    payload["serial_number"] = generate_serial_number(
        db,
        payload["created_by"]
    )

    insert_sql = text("""
        INSERT INTO work_at_height_permit (
            serial_number,
            section_contractor_name,
            nature_of_work,
            work_from_time,
            work_from_date,
            work_to_time,
            work_to_date,
            location,
            jsa_id,

            sc1_equipment_work_area_inspected,
            sc2_surrounding_area_checked,
            sc3_sewers_manholes_covered,
            sc4_scaffolds_ladders_checked,
            sc5_materials_fall_protected,
            sc6_isi_marked_belts_helmets,
            sc7_contractor_fit_for_height,
            sc8_instructions_given,
            sc9_proper_illumination,
            sc10_adequate_platform_space,
            sc11_proper_exit_means,
            sc12_precautionary_tags_boards,
            sc13_portable_equipment_earthed,
            sc14_elcb_switches_provided,
            sc14_additional_safety_measures,
            sc15_standby_supervision_provided,
            sc16_workers_trained_safety_belts,
            sc17_operations_incharge_informed,
            sc18_area_cordoned_off,
            sc19_precautions_against_public_traffic,
            sc20_fire_extinguisher_provided,
            sc20_condition_fav_elevation_work,

            special_instructions,
            additional_remarks,

            issuer_designation,
            issuer_name,
            issuer_signature,
            issuer_userid,

            requestor_name,
            requestor_designation,
            requestor_signature,

            receiver_role,
            receiver_name,
            receiver_designation,
            receiver_signature,
            receiver_userid,

            electrical_isolation_required,
            electrical_energization_required,
            toolbox_talk_required,

            renewal_from_date,
            renewal_from_time,
            renewal_to_date,
            renewal_to_time,

            renewal_issuer_name,
            renewal_issuer_designation,
            renewal_issuer_signature,

            renewal_requestor_name,
            renewal_requestor_designation,
            renewal_requestor_signature,

            renewal_receiver_name,
            renewal_receiver_designation,
            renewal_receiver_signature,

            renewal_toolbox_talk,

            closure_issuer_designation,
            closure_issuer_name,
            closure_issuer_signature,
            closure_issuer_userid,

            closure_requestor_name,
            closure_requestor_designation,
            closure_requestor_signature,
            closure_requestor_userid,

            closure_receiver_role,
            closure_receiver_name,
            closure_receiver_signature,
            closure_receiver_userid,

            job_completion_time,
            job_completion_date,
            work_status,

            status,
            created_by,
            updated_by
        )

        VALUES (
            :serial_number,
            :section_contractor_name,
            :nature_of_work,
            :work_from_time,
            :work_from_date,
            :work_to_time,
            :work_to_date,
            :location,
            :jsa_id,

            :sc1_equipment_work_area_inspected,
            :sc2_surrounding_area_checked,
            :sc3_sewers_manholes_covered,
            :sc4_scaffolds_ladders_checked,
            :sc5_materials_fall_protected,
            :sc6_isi_marked_belts_helmets,
            :sc7_contractor_fit_for_height,
            :sc8_instructions_given,
            :sc9_proper_illumination,
            :sc10_adequate_platform_space,
            :sc11_proper_exit_means,
            :sc12_precautionary_tags_boards,
            :sc13_portable_equipment_earthed,
            :sc14_elcb_switches_provided,
            :sc14_additional_safety_measures,
            :sc15_standby_supervision_provided,
            :sc16_workers_trained_safety_belts,
            :sc17_operations_incharge_informed,
            :sc18_area_cordoned_off,
            :sc19_precautions_against_public_traffic,
            :sc20_fire_extinguisher_provided,
            :sc20_condition_fav_elevation_work,

            :special_instructions,
            :additional_remarks,

            :issuer_designation,
            :issuer_name,
            :issuer_signature,
            :issuer_userid,

            :requestor_name,
            :requestor_designation,
            :requestor_signature,

            :receiver_role,
            :receiver_name,
            :receiver_designation,
            :receiver_signature,
            :receiver_userid,

            :electrical_isolation_required,
            :electrical_energization_required,
            :toolbox_talk_required,

            :renewal_from_date,
            :renewal_from_time,
            :renewal_to_date,
            :renewal_to_time,

            :renewal_issuer_name,
            :renewal_issuer_designation,
            :renewal_issuer_signature,

            :renewal_requestor_name,
            :renewal_requestor_designation,
            :renewal_requestor_signature,

            :renewal_receiver_name,
            :renewal_receiver_designation,
            :renewal_receiver_signature,

            :renewal_toolbox_talk,

            :closure_issuer_designation,
            :closure_issuer_name,
            :closure_issuer_signature,
            :closure_issuer_userid,

            :closure_requestor_name,
            :closure_requestor_designation,
            :closure_requestor_signature,
            :closure_requestor_userid,

            :closure_receiver_role,
            :closure_receiver_name,
            :closure_receiver_signature,
            :closure_receiver_userid,

            :job_completion_time,
            :job_completion_date,
            :work_status,

            :status,
            :created_by,
            :updated_by
        )
        RETURNING whp_id
    """)

    result = db.execute(insert_sql, payload)
    whp_id = result.scalar()

    db.commit()

    return {
        "message": "Work At Height Permit Created Successfully",
        "whp_id": whp_id,
        "serial_number": payload["serial_number"]
    }


# =================================================
# UPDATE (MAIN + HISTORY)
# =================================================
def update_work_at_height(db: Session, whp_id: int, data: WorkAtHeightPermitUpdate):
    payload = data.model_dump(exclude_unset=True)

    if not payload:
        return False

    set_clause = ", ".join([f"{k} = :{k}" for k in payload.keys()])

    update_sql = text(f"""
        UPDATE work_at_height_permit
        SET {set_clause},
            updated_at = NOW()
        WHERE whp_id = :whp_id
    """)

    payload["whp_id"] = whp_id
    db.execute(update_sql, payload)

    insert_work_at_height_history(db, whp_id)

    db.commit()
    return True