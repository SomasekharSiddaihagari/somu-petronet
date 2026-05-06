from sqlalchemy.orm import Session
from sqlalchemy.sql import text
from app.schemas.claim.asset_claim_disbursement_schema import (
    AssetClaimDisbursementCreate,
    AssetClaimDisbursementUpdate
)

# -------------------------------------------------
# CREATE DISBURSEMENT (INSERT + HISTORY)
# -------------------------------------------------
def create_asset_claim_disbursement(
    db: Session,
    data: AssetClaimDisbursementCreate
):
    payload = data.model_dump()

    query = text("""
        INSERT INTO asset_claim_disbursement (
            asset_claim_submission_id,
            claim_amount,
            disbursed_amount,
            payment_mode,
            disbursement_date,
            transaction_reference_no,
            bank_name,
            account_number,
            remarks,
            status,
            created_by,
            sap_assets_no
        )
        VALUES (
            :asset_claim_submission_id,
            :claim_amount,
            :disbursed_amount,
            :payment_mode,
            :disbursement_date,
            :transaction_reference_no,
            :bank_name,
            :account_number,
            :remarks,
            :status,
            :created_by,
            :sap_assets_no
        )
        RETURNING asset_claim_disbursement_id
    """)

    result = db.execute(query, payload)
    disbursement_id = result.scalar()

    insert_asset_claim_disbursement_history(db, disbursement_id)

    db.commit()
    return disbursement_id


# -------------------------------------------------
# UPDATE DISBURSEMENT (DYNAMIC + HISTORY)
# -------------------------------------------------
def update_asset_claim_disbursement(
    db: Session,
    asset_claim_disbursement_id: int,
    data: AssetClaimDisbursementUpdate
):
    payload = data.model_dump(exclude_unset=True)

    if not payload:
        return False

    set_clause = ", ".join([f"{k} = :{k}" for k in payload.keys()])

    query = text(f"""
        UPDATE asset_claim_disbursement
        SET {set_clause},
            updated_at = NOW()
        WHERE asset_claim_disbursement_id = :asset_claim_disbursement_id
    """)

    payload["asset_claim_disbursement_id"] = asset_claim_disbursement_id
    db.execute(query, payload)

    insert_asset_claim_disbursement_history(db, asset_claim_disbursement_id)

    db.commit()
    return True


# -------------------------------------------------
# HISTORY SNAPSHOT
# -------------------------------------------------
def insert_asset_claim_disbursement_history(
    db: Session,
    asset_claim_disbursement_id: int
):
    history_sql = text("""
        INSERT INTO asset_claim_disbursement_history (
            asset_claim_disbursement_id,
            asset_claim_submission_id,
            claim_amount,
            disbursed_amount,
            payment_mode,
            disbursement_date,
            transaction_reference_no,
            bank_name,
            account_number,
            remarks,
            status,
            created_by,
            updated_by,
            updated_by_supervisor,
            updated_by_supervisor_name,
            updated_by_hr,
            updated_by_hr_name,
            updated_by_finance,
            updated_by_finance_name,
            updated_at
        )
        SELECT
            asset_claim_disbursement_id,
            asset_claim_submission_id,
            claim_amount,
            disbursed_amount,
            payment_mode,
            disbursement_date,
            transaction_reference_no,
            bank_name,
            account_number,
            remarks,
            status,
            created_by,
            updated_by,
            updated_by_supervisor,
            updated_by_supervisor_name,
            updated_by_hr,
            updated_by_hr_name,
            updated_by_finance,
            updated_by_finance_name,
            NOW()
        FROM asset_claim_disbursement
        WHERE asset_claim_disbursement_id = :asset_claim_disbursement_id
    """)

    db.execute(
        history_sql,
        {"asset_claim_disbursement_id": asset_claim_disbursement_id}
    )
