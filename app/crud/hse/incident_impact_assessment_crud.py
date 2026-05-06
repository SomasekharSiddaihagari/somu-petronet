from sqlalchemy.orm import Session
from sqlalchemy.sql import text

from app.schemas.hse.incident_impact_assessment_schema import (
    IncidentImpactAssessmentCreate,
    IncidentImpactAssessmentUpdate
)


# =========================
# CREATE
# =========================
def create_incident_impact_assessment(
    db: Session,
    data: IncidentImpactAssessmentCreate
):
    payload = data.model_dump()

    sql = text("""
        INSERT INTO incident_impact_assessment (
            incident_id,
            fatalities_employees,
            fatalities_contractor,
            fatalities_others,
            injuries_employees,
            injuries_contractor,
            injuries_others,
            man_hours_lost_employees,
            man_hours_lost_contractor,
            man_hours_lost_others,
            direct_loss_details,
            indirect_loss_details,
            facility_status,
            brief_incident_description,
            similar_incident_past,
            status,
            created_by
        )
        VALUES (
            :incident_id,
            :fatalities_employees,
            :fatalities_contractor,
            :fatalities_others,
            :injuries_employees,
            :injuries_contractor,
            :injuries_others,
            :man_hours_lost_employees,
            :man_hours_lost_contractor,
            :man_hours_lost_others,
            :direct_loss_details,
            :indirect_loss_details,
            :facility_status,
            :brief_incident_description,
            :similar_incident_past,
            :status,
            :created_by
        )
        RETURNING impact_id
    """)

    result = db.execute(sql, payload)
    db.commit()

    return {"impact_id": result.scalar()}


# =========================
# UPDATE
# =========================
def update_incident_impact_assessment(
    db: Session,
    impact_id: int,
    data: IncidentImpactAssessmentUpdate
):
    payload = data.model_dump(exclude_unset=True)

    if not payload:
        return False

    set_clause = ", ".join([f"{k} = :{k}" for k in payload.keys()])

    sql = text(f"""
        UPDATE incident_impact_assessment
        SET {set_clause},
            updated_at = NOW()
        WHERE impact_id = :impact_id
    """)

    payload["impact_id"] = impact_id
    db.execute(sql, payload)
    db.commit()
    return True


# =========================
# GET ALL
# =========================
def get_all_incident_impact_assessments(db: Session):
    sql = text("""
        SELECT
            impact_id,
            incident_id,

            fatalities_employees,
            fatalities_contractor,
            fatalities_others,

            injuries_employees,
            injuries_contractor,
            injuries_others,

            man_hours_lost_employees,
            man_hours_lost_contractor,
            man_hours_lost_others,

            direct_loss_details,
            indirect_loss_details,

            facility_status,
            brief_incident_description,
            similar_incident_past,

            status,
            created_by,
            updated_by,
            created_at,
            updated_at
        FROM incident_impact_assessment
        ORDER BY created_at DESC
    """)

    rows = db.execute(sql).mappings().all()

    return {
        "count": len(rows),
        "data": rows
    }

