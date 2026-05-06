from sqlalchemy.orm import Session
from sqlalchemy.sql import text

from app.schemas.hse.incident_cause_analysis_schema import (
    IncidentCauseAnalysisCreate,
    IncidentCauseAnalysisUpdate
)


# =========================
# CREATE
# =========================
def create_incident_cause_analysis(
    db: Session,
    data: IncidentCauseAnalysisCreate
):
    payload = data.model_dump()

    sql = text("""
        INSERT INTO incident_cause_analysis (
            incident_id,

            cause_deviation_from_procedure,
            cause_lack_of_job_knowledge,
            cause_lack_of_supervision,
            cause_improper_inspection,
            cause_improper_maintenance,
            cause_improper_material_handling,
            cause_negligent_driving,
            cause_not_using_ppe,
            cause_equipment_failure,
            cause_poor_design_layout,
            cause_inadequate_facility,
            cause_poor_house_keeping,
            cause_natural_calamity,
            cause_pilferage_sabotage,

            leak_weld_from_equipment_lines,
            leak_from_flange_gland,
            leak_from_rotary_equipment,
            leak_metallurgical_failure,
            leak_due_to_improper_operation,
            leak_due_to_improper_maintenance,
            leak_normal_operation_venting_draining,
            leak_any_other,
            leak_any_other_description,    

            ignition_near_to_hot_work,
            ignition_near_to_furnace_flare,
            ignition_auto_ignition,
            ignition_loose_electrical_connection,
            ignition_near_to_hot_surface,
            ignition_static_electricity,
            ignition_hammering_fall_of_object,
            ignition_heat_due_to_friction,
            ignition_lightning,
            ignition_any_other_pyrophoric,
            ignition_any_other_pyrophoric_description,    

            status,
            created_by
        )
        VALUES (
            :incident_id,

            :cause_deviation_from_procedure,
            :cause_lack_of_job_knowledge,
            :cause_lack_of_supervision,
            :cause_improper_inspection,
            :cause_improper_maintenance,
            :cause_improper_material_handling,
            :cause_negligent_driving,
            :cause_not_using_ppe,
            :cause_equipment_failure,
            :cause_poor_design_layout,
            :cause_inadequate_facility,
            :cause_poor_house_keeping,
            :cause_natural_calamity,
            :cause_pilferage_sabotage,

            :leak_weld_from_equipment_lines,
            :leak_from_flange_gland,
            :leak_from_rotary_equipment,
            :leak_metallurgical_failure,
            :leak_due_to_improper_operation,
            :leak_due_to_improper_maintenance,
            :leak_normal_operation_venting_draining,
            :leak_any_other,
            :leak_any_other_description,   

            :ignition_near_to_hot_work,
            :ignition_near_to_furnace_flare,
            :ignition_auto_ignition,
            :ignition_loose_electrical_connection,
            :ignition_near_to_hot_surface,
            :ignition_static_electricity,
            :ignition_hammering_fall_of_object,
            :ignition_heat_due_to_friction,
            :ignition_lightning,
            :ignition_any_other_pyrophoric,
            :ignition_any_other_pyrophoric_description,

            :status,
            :created_by
        )
        RETURNING cause_id
    """)

    result = db.execute(sql, payload)
    db.commit()

    return {"cause_id": result.scalar()}


# =========================
# UPDATE
# =========================
def update_incident_cause_analysis(
    db: Session,
    cause_id: int,
    data: IncidentCauseAnalysisUpdate
):
    payload = data.model_dump(exclude_unset=True)

    if not payload:
        return False

    set_clause = ", ".join([f"{k} = :{k}" for k in payload.keys()])

    sql = text(f"""
        UPDATE incident_cause_analysis
        SET {set_clause},
            updated_at = NOW()
        WHERE cause_id = :cause_id
    """)

    payload["cause_id"] = cause_id
    db.execute(sql, payload)
    db.commit()
    return True



# =========================
# GET ALL
# =========================
def get_all_incident_cause_analysis(db: Session):
    sql = text("""
        SELECT
            cause_id,
            incident_id,

            cause_deviation_from_procedure,
            cause_lack_of_job_knowledge,
            cause_lack_of_supervision,
            cause_improper_inspection,
            cause_improper_maintenance,
            cause_improper_material_handling,
            cause_negligent_driving,
            cause_not_using_ppe,
            cause_equipment_failure,
            cause_poor_design_layout,
            cause_inadequate_facility,
            cause_poor_house_keeping,
            cause_natural_calamity,
            cause_pilferage_sabotage,

            leak_weld_from_equipment_lines,
            leak_from_flange_gland,
            leak_from_rotary_equipment,
            leak_metallurgical_failure,
            leak_due_to_improper_operation,
            leak_due_to_improper_maintenance,
            leak_normal_operation_venting_draining,
            leak_any_other,
            leak_any_other_description,

            ignition_near_to_hot_work,
            ignition_near_to_furnace_flare,
            ignition_auto_ignition,
            ignition_loose_electrical_connection,
            ignition_near_to_hot_surface,
            ignition_static_electricity,
            ignition_hammering_fall_of_object,
            ignition_heat_due_to_friction,
            ignition_lightning,
            ignition_any_other_pyrophoric,
            ignition_any_other_pyrophoric_description,   

            status,
            created_by,
            updated_by,
            created_at,
            updated_at
        FROM incident_cause_analysis
        ORDER BY created_at DESC
    """)

    rows = db.execute(sql).mappings().all()

    return {
        "count": len(rows),
        "data": rows
    }



