from sqlalchemy.orm import Session
from sqlalchemy import text
from app.schemas.MOC.HIRASchema import HIRACreate, HIRAUpdate


def create_hira(db: Session, hira: HIRACreate):
    query = text("""
        INSERT INTO hira_entries (
            moc_request_id,
            risk,
            division_dept_name,
            project_requisition_no,
            job_description,
            activity,
            hazard,
            risk_level,
            consequence,
            control_measures,
            comments_initiator,
            hira_reviewer_id,
            status
        )
        VALUES (
            :moc_request_id,
            :risk,
            :division_dept_name,
            :project_requisition_no,
            :job_description,
            :activity,
            :hazard,
            :risk_level,
            :consequence,
            :control_measures,
            :comments_initiator,
            :hira_reviewer_id,
            :status
        )
        RETURNING hira_id
    """)

    result = db.execute(query, hira.dict())
    db.commit()

    return result.fetchone()[0]


def update_hira(db: Session, hira_id: int, hira: HIRAUpdate):
    fields = []
    values = {"hira_id": hira_id}

    for key, value in hira.dict(exclude_unset=True).items():
        fields.append(f"{key} = :{key}")
        values[key] = value

    if not fields:
        return 0

    query = text(f"""
        UPDATE hira_entries
        SET {", ".join(fields)}
        WHERE hira_id = :hira_id
    """)

    result = db.execute(query, values)
    db.commit()

    return result.rowcount
