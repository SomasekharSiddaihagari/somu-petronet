from sqlalchemy.orm import Session
from sqlalchemy.sql import text
from app.schemas.claim.mobile_bill_reimbursement_schema import (
    MobileBillReimbursementCreate,
    MobileBillReimbursementUpdate
)

# =================================================
# CREATE
# =================================================
def create_mobile_bill_reimbursement(
    db: Session,
    data: MobileBillReimbursementCreate
):
    # 🚨 DO NOT exclude None for INSERT
    payload = data.model_dump()

    query = text("""
        INSERT INTO mobile_bill_reimbursement (
            ra_claim_id,
            bill_month_year,

            mobile_number_1,
            bill_amount_1,
            mobile_number_2,
            bill_amount_2,

            total_claimed_amount,
            monthly_limit,
            document_names,

            remarks,
            declaration_accepted,
            status,

            updated_by_supervisor,
            updated_by_supervisor_name,
            supervisor_comment,

            updated_by_hr,
            updated_by_hr_name,
            hr_comment,

            updated_by_finance,
            updated_by_finance_name,
            finance_comment,

            created_by
        )
        VALUES (
            :ra_claim_id,
            :bill_month_year,

            :mobile_number_1,
            :bill_amount_1,
            :mobile_number_2,
            :bill_amount_2,

            :total_claimed_amount,
            :monthly_limit,
            :document_names,

            :remarks,
            :declaration_accepted,
            :status,

            :updated_by_supervisor,
            :updated_by_supervisor_name,
            :supervisor_comment,

            :updated_by_hr,
            :updated_by_hr_name,
            :hr_comment,

            :updated_by_finance,
            :updated_by_finance_name,
            :finance_comment,

            :created_by
        )
        RETURNING mobile_bill_reimbursement_id
    """)

    result = db.execute(query, payload)
    db.commit()

    return result.scalar()


# =================================================
# UPDATE
# =================================================
def update_mobile_bill_reimbursement(
    db: Session,
    mobile_bill_reimbursement_id: int,
    data: MobileBillReimbursementUpdate
):
    # ✅ exclude_none IS CORRECT for UPDATE
    payload = data.model_dump(exclude_none=True)

    if not payload:
        return

    set_clause = ", ".join(
        f"{key} = :{key}" for key in payload.keys()
    )

    payload["mobile_bill_reimbursement_id"] = mobile_bill_reimbursement_id

    query = text(f"""
        UPDATE mobile_bill_reimbursement
        SET {set_clause},
            updated_at = NOW()
        WHERE mobile_bill_reimbursement_id = :mobile_bill_reimbursement_id
    """)

    db.execute(query, payload)
    db.commit()


# =================================================
# GET BY ID
# =================================================
def get_mobile_bill_reimbursement(
    db: Session,
    mobile_bill_reimbursement_id: int
):
    query = text("""
        SELECT *
        FROM mobile_bill_reimbursement
        WHERE mobile_bill_reimbursement_id = :id
    """)

    return db.execute(
        query,
        {"id": mobile_bill_reimbursement_id}
    ).mappings().first()


# =================================================
# DELETE
# =================================================
def delete_mobile_bill_reimbursement(
    db: Session,
    mobile_bill_reimbursement_id: int
):
    insert_mobile_bill_reimbursement_history(db, mobile_bill_reimbursement_id)

    db.execute(
        text("""
            DELETE FROM mobile_bill_reimbursement
            WHERE mobile_bill_reimbursement_id = :id
        """),
        {"id": mobile_bill_reimbursement_id}
    )

    db.commit()
    return True


# =================================================
# HISTORY SNAPSHOT
# =================================================
def insert_mobile_bill_reimbursement_history(
    db: Session,
    mobile_bill_reimbursement_id: int
):
    history_sql = text("""
        INSERT INTO mobile_bill_reimbursement_history (
            mobile_bill_reimbursement_id,
            ra_claim_id,
            bill_month_year,
            mobile_number_1,
            bill_amount_1,
            mobile_number_2,
            bill_amount_2,
            total_claimed_amount,
            monthly_limit,
            document_names,
            remarks,
            declaration_accepted,
            status,
            updated_by_supervisor,
            updated_by_supervisor_name,
            supervisor_comment,
            updated_by_hr,
            updated_by_hr_name,
            hr_comment,
            updated_by_finance,
            updated_by_finance_name,
            finance_comment,
            created_by
        )
        SELECT
            mobile_bill_reimbursement_id,
            ra_claim_id,
            bill_month_year,
            mobile_number_1,
            bill_amount_1,
            mobile_number_2,
            bill_amount_2,
            total_claimed_amount,
            monthly_limit,
            document_names,
            remarks,
            declaration_accepted,
            status,
            updated_by_supervisor,
            updated_by_supervisor_name,
            supervisor_comment,
            updated_by_hr,
            updated_by_hr_name,
            hr_comment,
            updated_by_finance,
            updated_by_finance_name,
            finance_comment,
            created_by
        FROM mobile_bill_reimbursement
        WHERE mobile_bill_reimbursement_id = :id
    """)

    db.execute(history_sql, {"id": mobile_bill_reimbursement_id})
