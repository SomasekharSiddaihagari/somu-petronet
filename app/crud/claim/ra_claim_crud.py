from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy.sql import text
from app.schemas.claim.ra_claim_schema import (
    RAClaimCreate,
    RAClaimUpdate
)

# -------------------------------------------------
# Generate RA Claim Reference
# Example: RA/2025/000001
# -------------------------------------------------
def generate_ra_claim_ref(db: Session) -> str:
    year = datetime.now().year
    prefix = f"RA/{year}/"

    query = text("""
        SELECT ra_claim_ref_id
        FROM ra_claim
        WHERE ra_claim_ref_id LIKE :prefix
        ORDER BY ra_claim_id DESC
        LIMIT 1
    """)

    last = db.execute(query, {"prefix": f"{prefix}%"}).fetchone()

    next_no = 1
    if last and last[0]:
        next_no = int(last[0].split("/")[-1]) + 1

    return f"{prefix}{str(next_no).zfill(6)}"


# =================================================
# CREATE
# =================================================
def create_ra_claim(db: Session, data: RAClaimCreate):
    ra_claim_ref_id = generate_ra_claim_ref(db)

    payload = data.model_dump()
    payload["ra_claim_ref_id"] = ra_claim_ref_id

    query = text("""
        INSERT INTO ra_claim (
            ra_claim_ref_id,
            employee_name,
            employee_id,
            department,
            designation,
            station,
            grade,
            claim_module,
            category,
            status,
            remarks,
            created_by
        )
        VALUES (
            :ra_claim_ref_id,
            :employee_name,
            :employee_id,
            :department,
            :designation,
            :station,
            :grade,
            :claim_module,
            :category,
            :status,
            :remarks,
            :created_by
        )
        RETURNING ra_claim_id
    """)

    ra_claim_id = db.execute(query, payload).scalar()

    # insert_ra_claim_history(db, ra_claim_id)
    db.commit()

    return {
        "ra_claim_id": ra_claim_id,
        "ra_claim_ref_id": ra_claim_ref_id
    }


# =================================================
# UPDATE
# =================================================
def update_ra_claim(
    db: Session,
    ra_claim_id: int,
    data: RAClaimUpdate
):
    payload = data.model_dump(exclude_unset=True)

    if not payload:
        return False

    set_clause = ", ".join(f"{k} = :{k}" for k in payload)

    query = text(f"""
        UPDATE ra_claim
        SET {set_clause},
            updated_at = NOW()
        WHERE ra_claim_id = :ra_claim_id
    """)

    payload["ra_claim_id"] = ra_claim_id
    db.execute(query, payload)

    insert_ra_claim_history(db, ra_claim_id)
    db.commit()
    return True


# =================================================
# GET BY ID
# =================================================
def get_ra_claim(db: Session, ra_claim_id: int):
    query = text("""
        SELECT *
        FROM ra_claim
        WHERE ra_claim_id = :id
    """)

    return db.execute(query, {"id": ra_claim_id}).mappings().first()


# =================================================
# DELETE
# =================================================
def delete_ra_claim(db: Session, ra_claim_id: int):
    insert_ra_claim_history(db, ra_claim_id)

    db.execute(
        text("""
            DELETE FROM ra_claim
            WHERE ra_claim_id = :id
        """),
        {"id": ra_claim_id}
    )

    db.commit()
    return True


# =================================================
# HISTORY SNAPSHOT
# =================================================
def insert_ra_claim_history(db: Session, ra_claim_id: int):
    history_sql = text("""
        INSERT INTO ra_claim_history (
            ra_claim_id,
            ra_claim_ref_id,
            employee_name,
            employee_id,
            department,
            designation,
            station,
            grade,
            claim_module,
            category,
            status,
            remarks,
            updated_by_supervisor,
            updated_by_supervisor_name,
            updated_by_hr,
            updated_by_hr_name,
            updated_by_finance,
            updated_by_finance_name,
            created_by
        )
        SELECT
            ra_claim_id,
            ra_claim_ref_id,
            employee_name,
            employee_id,
            department,
            designation,
            station,
            grade,
            claim_module,
            category,
            status,
            remarks,
            updated_by_supervisor,
            updated_by_supervisor_name,
            updated_by_hr,
            updated_by_hr_name,
            updated_by_finance,
            updated_by_finance_name,
            created_by
        FROM ra_claim
        WHERE ra_claim_id = :id
    """)

    db.execute(history_sql, {"id": ra_claim_id})
