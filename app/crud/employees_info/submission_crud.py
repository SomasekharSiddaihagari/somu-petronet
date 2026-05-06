from sqlalchemy import text
from sqlalchemy.orm import Session
from typing import Optional
from app.schemas.employees_info.submission_schema import (
    FamilySubmissionCreate,
    FamilySubmissionUpdate
)


# =========================
# CREATE SUBMISSION (POST)
# =========================
def create_submission(db: Session, payload: FamilySubmissionCreate):
    query = text("""
        INSERT INTO submission 
        (user_id, status, hr_comment, reviewed_by, reviewed_at)
        VALUES 
        (:user_id, :status, :hr_comment, :reviewed_by, :reviewed_at)
        RETURNING submission_id
    """)

    result = db.execute(query, {
        "user_id": payload.user_id,
        "status": payload.status,
        "hr_comment": payload.hr_comment,
        "reviewed_by": payload.reviewed_by,
        "reviewed_at": payload.reviewed_at
    })

    db.commit()
    return result.fetchone()[0]


# =========================
# UPDATE SUBMISSION (PUT)
# =========================
def update_submission(
    db: Session,
    submission_id: int,
    payload: FamilySubmissionUpdate
):

    fields = []
    values = {"submission_id": submission_id}

    if payload.status is not None:
        fields.append("status = :status")
        values["status"] = payload.status

    if payload.hr_comment is not None:
        fields.append("hr_comment = :hr_comment")
        values["hr_comment"] = payload.hr_comment

    if payload.reviewed_by is not None:
        fields.append("reviewed_by = :reviewed_by")
        values["reviewed_by"] = payload.reviewed_by

    if payload.reviewed_at is not None:
        fields.append("reviewed_at = :reviewed_at")
        values["reviewed_at"] = payload.reviewed_at

    if not fields:
        return "Nothing to update"

    query = text(f"""
        UPDATE submission
        SET {", ".join(fields)}
        WHERE submission_id = :submission_id
    """)

    db.execute(query, values)
    db.commit()

    return "Updated successfully"
