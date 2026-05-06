from pydoc import text
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.claim.ra_claim_schema import (
    RAClaimCreate,
    RAClaimUpdate
)
from sqlalchemy.sql import text as sql_text

from app.crud.claim.ra_claim_crud import (
    create_ra_claim,
    update_ra_claim,
    get_ra_claim,
    delete_ra_claim
)

router = APIRouter(
    prefix="/ra-claim",
    tags=["RA Claim"]
)

@router.get("/claim-by-user/{user_id}")
def get_asset_claims_by_user(
    user_id: int,
    category: str | None = None,
    db: Session = Depends(get_db)
):
    result = db.execute(
        sql_text("""
            SELECT
                ac.*,
                COALESCE(
                    json_agg(
                        jsonb_build_object(
                            'asset_claim_submission_id', acs.asset_claim_submission_id,
                            'item_type', acs.item_type,
                            'item_name', acs.item_name,
                            'claim_amount', acs.claim_amount,
                            'owned_by', acs.owned_by,
                            'vendor_name', acs.vendor_name,
                            'vendor_gstin', acs.vendor_gstin,
                            'vendor_address', acs.vendor_address,
                            'vendor_contact_no', acs.vendor_contact_no,
                            'invoice_date', acs.invoice_date,
                            'invoice_no', acs.invoice_no,
                            'document_names', acs.document_names,
                            'status', acs.status,
                            'created_at', acs.created_at,
                            'residual_value_percent', acs.residual_value_percent,
                            'residual_value_amount', acs.residual_value_amount,
                            'amount_to_be_disbursed', acs.amount_to_be_disbursed,
                            'hr_comment', acs.hr_comment,
                            'finance_comment', acs.finance_comment,
                            'supervisor_comment', acs.supervisor_comment
                        )
                    ) FILTER (WHERE acs.asset_claim_submission_id IS NOT NULL),
                    '[]'
                ) AS submissions
            FROM asset_claim ac
            LEFT JOIN asset_claim_submission acs
              ON ac.asset_claim_id = acs.asset_claim_id
            WHERE ac.created_by = :user_id
              AND (ac.bought_back = false OR ac.bought_back IS NULL)
              AND (
                    :category IS NULL
                    OR ac.category ILIKE :category
                  )
            GROUP BY ac.asset_claim_id
            ORDER BY created_at DESC NULLS LAST
        """),
        {
            "user_id": user_id,
            "category": category
        }
    )

    rows = result.mappings().all()

    return {
        "success": True,
        "count": len(rows),
        "data": rows
    }



@router.post("/create")
def create_claim(
    data: RAClaimCreate,
    db: Session = Depends(get_db)
):
    return create_ra_claim(db, data)


@router.put("/update/{ra_claim_id}")
def update_claim(
    ra_claim_id: int,
    data: RAClaimUpdate,
    db: Session = Depends(get_db)
):
    update_ra_claim(db, ra_claim_id, data)
    return {
        "status": "success",
        "message": "RA claim updated successfully"
    }








# @router.get("/{ra_claim_id}")
# def get_claim(
#     ra_claim_id: int,
#     db: Session = Depends(get_db)
# ):
#     return get_ra_claim(db, ra_claim_id)


# @router.delete("/{ra_claim_id}")
# def delete_claim(
#     ra_claim_id: int,
#     db: Session = Depends(get_db)
# ):
#     delete_ra_claim(db, ra_claim_id)
#     return {
#         "status": "success",
#         "message": "RA claim deleted successfully"
#     }
#

# @router.get("/cards")
# def get_ra_claim_cards(
#     user_id: int = Query(...),
#     db: Session = Depends(get_db)
# ):
#     # -------------------------------------------------
#     # 1️⃣ USER VALIDATION
#     # -------------------------------------------------
#     exists = db.execute(
#         sql_text("SELECT 1 FROM users WHERE user_id = :id"),
#         {"id": user_id}
#     ).fetchone()

#     if not exists:
#         raise HTTPException(status_code=404, detail="User not found")

#     # -------------------------------------------------
#     # 2️⃣ TOTAL CLAIM COUNT (RA + ALLOWANCE, SELF ONLY)
#     # -------------------------------------------------
#     total_claims = db.execute(
#         sql_text("""
#             SELECT
#                 (
#                     SELECT COUNT(*)
#                     FROM ra_claim
#                     WHERE created_by = :id
#                 )
#                 +
#                 (
#                     SELECT COUNT(*)
#                     FROM allowance_claim
#                     WHERE created_by = :id
#                 ) AS total_claims
#         """),
#         {"id": user_id}
#     ).scalar()

#     # -------------------------------------------------
#     # 3️⃣ RA STATUS COUNTS (ROBUST STATUS HANDLING)
#     # -------------------------------------------------
#     status_counts = db.execute(
#         sql_text("""
#             SELECT
#                 COUNT(*) FILTER (
#                     WHERE status ILIKE '%approved%'
#                 ) AS approved,

#                 COUNT(*) FILTER (
#                     WHERE status ILIKE '%pending%'
#                 ) AS pending
#             FROM ra_claim
#             WHERE created_by = :id
#         """),
#         {"id": user_id}
#     ).mappings().one()

#     # -------------------------------------------------
#     # 4️⃣ TOTAL CLAIMED AMOUNT (ALL MODULES, SELF ONLY)
#     # -------------------------------------------------
#     total_claimed = db.execute(
#         sql_text("""
#             SELECT COALESCE(SUM(amount), 0)
#             FROM (
#                 SELECT total_claimed_amount AS amount
#                 FROM mobile_bill_reimbursement
#                 WHERE created_by = :id

#                 UNION ALL
#                 SELECT amount_claimed
#                 FROM laptop_maintenance_reimbursement
#                 WHERE created_by = :id

#                 UNION ALL
#                 SELECT bill_amount
#                 FROM data_card_reimbursement
#                 WHERE created_by = :id

#                 UNION ALL
#                 SELECT amount_claimed
#                 FROM furniture_rm_reimbursement
#                 WHERE created_by = :id

#                 UNION ALL
#                 SELECT fuel_claim_amount + maintenance_claim_amount
#                 FROM vehicle_cm_reimbursement
#                 WHERE created_by = :id

#                 UNION ALL
#                 SELECT total_amount
#                 FROM out_of_pocket_claim
#                 WHERE created_by = :id

#                 UNION ALL
#                 SELECT grand_total
#                 FROM allowance_claim
#                 WHERE created_by = :id
#             ) t
#         """),
#         {"id": user_id}
#     ).scalar()

#     # -------------------------------------------------
#     # 5️⃣ FINAL RESPONSE
#     # -------------------------------------------------
#     return {
#         "success": True,
#         "data": {
#             "total_claims": total_claims,
#             "approved": status_counts["approved"],
#             "pending": status_counts["pending"],
#             "total_claimed": float(total_claimed)
#         }
#     }


