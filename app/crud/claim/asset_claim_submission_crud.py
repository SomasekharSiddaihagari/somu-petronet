from sqlalchemy.orm import Session
from sqlalchemy.sql import text

from app.schemas.claim.asset_claim_submission_schema import (
    AssetClaimSubmissionCreate,
    AssetClaimSubmissionUpdate
)

# -------------------------------------------------
# CREATE SUBMISSION (MAIN + HISTORY)
# -------------------------------------------------
def create_asset_claim_submission(
    db: Session,
    data: AssetClaimSubmissionCreate
):
    payload = data.model_dump()

    query = text("""
        INSERT INTO asset_claim_submission (
            asset_claim_id,
            item_type,
            item_name,
            claim_amount,
            vendor_name,
            vendor_gstin,
            vendor_address,
            vendor_contact_no,
            invoice_date,
            invoice_no,
            document_names,
            owned_by,
            declaration_accepted,
            status,
            created_by
        )
        VALUES (
            :asset_claim_id,
            :item_type,
            :item_name,
            :claim_amount,
            :vendor_name,
            :vendor_gstin,
            :vendor_address,
            :vendor_contact_no,
            :invoice_date,
            :invoice_no,
            :document_names,
            :owned_by,
            :declaration_accepted,
            :status,
            :created_by
        )
        RETURNING asset_claim_submission_id
    """)

    result = db.execute(query, payload)
    submission_id = result.scalar()

    insert_asset_claim_submission_history(db, submission_id)

    db.commit()
    return submission_id


# -------------------------------------------------
# UPDATE SUBMISSION (NOW INCLUDES 3 FIELDS)
# -------------------------------------------------
def update_asset_claim_submission(
    db: Session,
    asset_claim_submission_id: int,
    data: AssetClaimSubmissionUpdate
    ):
    payload = data.model_dump(exclude_unset=True)

    if not payload:
        return False

    set_clause = ", ".join([f"{k} = :{k}" for k in payload.keys()])

    query = text(f"""
        UPDATE asset_claim_submission
        SET {set_clause},
            updated_at = NOW()
        WHERE asset_claim_submission_id = :asset_claim_submission_id
    """)

    payload["asset_claim_submission_id"] = asset_claim_submission_id
    db.execute(query, payload)

    # ✅ ALWAYS INSERT HISTORY SNAPSHOT
    insert_asset_claim_submission_history(db, asset_claim_submission_id)

    db.commit()
    return True


# -------------------------------------------------
# HISTORY SNAPSHOT (NO CHANGE REQUIRED)
# -------------------------------------------------
def insert_asset_claim_submission_history(
    db: Session,
    asset_claim_submission_id: int
):
    history_sql = text("""
        INSERT INTO asset_claim_submission_history (
            asset_claim_submission_id,
            asset_claim_id,
            item_type,
            item_name,
            claim_amount,
            vendor_name,
            vendor_gstin,
            vendor_address,
            vendor_contact_no,
            invoice_date,
            invoice_no,
            document_names,
            owned_by,
            declaration_accepted,
            status,
            created_by,
            updated_by,
            residual_value_percent,
            residual_value_amount,
            amount_to_be_disbursed,
            hr_comment,
            finance_comment,
            supervisor_comment,
            updated_by_supervisor,
            updated_by_supervisor_name,
            updated_by_hr,
            updated_by_hr_name,
            updated_by_finance,
            updated_by_finance_name,
            updated_at
        )
        SELECT
            asset_claim_submission_id,
            asset_claim_id,
            item_type,
            item_name,
            claim_amount,
            vendor_name,
            vendor_gstin,
            vendor_address,
            vendor_contact_no,
            invoice_date,
            invoice_no,
            document_names,
            owned_by,
            declaration_accepted,
            status,
            created_by,
            updated_by,
            residual_value_percent,
            residual_value_amount,
            amount_to_be_disbursed,
            hr_comment,
            finance_comment,
            supervisor_comment,
            updated_by_supervisor,
            updated_by_supervisor_name,
            updated_by_hr,
            updated_by_hr_name,
            updated_by_finance,
            updated_by_finance_name,
            NOW()
        FROM asset_claim_submission
        WHERE asset_claim_submission_id = :asset_claim_submission_id
    """)

    db.execute(
        history_sql,
        {"asset_claim_submission_id": asset_claim_submission_id}
    )
