from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy.sql import text

from app.database import get_db
from app.schemas.claim.asset_claim_validation_sheema import (
    AssetClaimValidateRequest,
    AssetClaimValidateResponse
)
from app.services.claim.saervice_validation_asset import POLICY
from datetime import date, timedelta

router = APIRouter(prefix="/asset-claim", tags=["Asset Claim"])


# =================================================
# HELPERS
# =================================================
def calculate_next_date(invoice_date: date, years: int) -> date:
    return invoice_date + timedelta(days=365 * years)


def success_response(amount, ceiling, message):
    if ceiling and amount > ceiling:
        excess = amount - ceiling
        return AssetClaimValidateResponse(
            eligible=True,
            eligible_amount=ceiling,
            ceiling=ceiling,
            next_eligible_date=None,
            message=f"Eligible up to ₹{ceiling}. ₹{excess} to be paid by employee."
        )

    return AssetClaimValidateResponse(
        eligible=True,
        eligible_amount=amount,
        ceiling=ceiling,
        next_eligible_date=None,
        message=message
    )


# =================================================
# MAIN VALIDATION API
# =================================================
@router.post("/validate", response_model=AssetClaimValidateResponse)
def validate_asset_claim(
    payload: AssetClaimValidateRequest,
    db: Session = Depends(get_db)
):

    # =================================================
    # 1. Permanent employee check (GLOBAL)
    # =================================================
    if payload.employee_type != "Permanent":
        return AssetClaimValidateResponse(
            eligible=False,
            eligible_amount=None,
            ceiling=None,
            next_eligible_date=None,
            message="Only permanent employees are eligible"
        )

    # =================================================
    # 2. MOBILE HANDSET
    # =================================================
    if payload.category == "Mobile Handset":

        policy = POLICY["Mobile Handset"]
        ceiling = policy["grades"].get(payload.grade)

        if not ceiling:
            return AssetClaimValidateResponse(
                eligible=False,
                eligible_amount=None,
                ceiling=None,
                next_eligible_date=None,
                message="Invalid grade for Mobile Handset"
            )

        row = db.execute(
            text("""
                SELECT acs.invoice_date
                FROM asset_claim ac
                JOIN asset_claim_submission acs
                ON ac.asset_claim_id = acs.asset_claim_id
                WHERE ac.employee_id = :employee_id
                  AND ac.category = 'Mobile Handset'
                  AND ac.status = 'Approved'
                ORDER BY acs.invoice_date DESC
                LIMIT 1
            """),
            {"employee_id": payload.employee_id}
        ).fetchone()

        if row:
            next_date = calculate_next_date(row.invoice_date, policy["frequency_years"])
            if payload.invoice_date < next_date:
                return AssetClaimValidateResponse(
                    eligible=False,
                    eligible_amount=None,
                    ceiling=ceiling,
                    next_eligible_date=next_date,
                    message="Mobile Handset can be claimed once every 2 years"
                )

        return success_response(payload.claim_amount, ceiling, "Eligible for Mobile Handset")


    # =================================================
    # 3. LAPTOP / DESKTOP
    # =================================================
    if payload.category == "Laptop / Desktop":

        policy = POLICY["Laptop / Desktop"]
        ceiling = policy["grades"].get(payload.grade)

        if not ceiling:
            return AssetClaimValidateResponse(
                eligible=False,
                eligible_amount=None,
                ceiling=None,
                next_eligible_date=None,
                message="Invalid grade for Laptop/Desktop"
            )

        row = db.execute(
            text("""
                SELECT acs.invoice_date
                FROM asset_claim ac
                JOIN asset_claim_submission acs
                ON ac.asset_claim_id = acs.asset_claim_id
                WHERE ac.employee_id = :employee_id
                  AND ac.category = 'Laptop / Desktop'
                  AND ac.status = 'Approved'
                ORDER BY acs.invoice_date DESC
                LIMIT 1
            """),
            {"employee_id": payload.employee_id}
        ).fetchone()

        if row:
            next_date = calculate_next_date(row.invoice_date, policy["frequency_years"])
            if payload.invoice_date < next_date:
                return AssetClaimValidateResponse(
                    eligible=False,
                    eligible_amount=None,
                    ceiling=ceiling,
                    next_eligible_date=next_date,
                    message="Laptop/Desktop can be claimed once every 3 years"
                )

        # 1% upfront deduction
        net_amount = payload.claim_amount * 0.99

        return success_response(net_amount, ceiling, "Eligible for Laptop/Desktop")


    # =================================================
    # 4. DATA CARD PURCHASE
    # =================================================
    if payload.category == "Data Card":

        policy = POLICY["Data Card"]

        laptop_exists = db.execute(
            text("""
                SELECT 1 FROM asset_claim
                WHERE employee_id = :employee_id
                  AND category = 'Laptop/Desktop'
                  AND status = 'Approved'
                LIMIT 1
            """),
            {"employee_id": payload.employee_id}
        ).fetchone()

        row = db.execute(
            text("""
                SELECT acs.invoice_date
                FROM asset_claim ac
                JOIN asset_claim_submission acs
                ON ac.asset_claim_id = acs.asset_claim_id
                WHERE ac.employee_id = :employee_id
                  AND ac.category = 'Data Card'
                  AND ac.status = 'Approved'
                ORDER BY acs.invoice_date DESC
                LIMIT 1
            """),
            {"employee_id": payload.employee_id}
        ).fetchone()

        if row:
            next_date = calculate_next_date(row.invoice_date, policy["frequency_years"])
            if payload.invoice_date < next_date:
                return AssetClaimValidateResponse(
                    eligible=False,
                    eligible_amount=None,
                    ceiling=policy["ceiling"],
                    next_eligible_date=next_date,
                    message="Data Card can be claimed once every 3 years"
                )

        return success_response(payload.claim_amount, policy["ceiling"], "Eligible for Data Card")


    # =================================================
    # 5. FURNITURE (FULLY IMPLEMENTED)
    # =================================================
    if payload.category == "Furniture":

        if not payload.sub_category:
            return AssetClaimValidateResponse(
                eligible=False,
                eligible_amount=None,
                ceiling=None,
                next_eligible_date=None,
                message="Furniture sub-category is required"
            )

        furniture_policy = POLICY["Furniture"].get(payload.sub_category)
        if not furniture_policy:
            return AssetClaimValidateResponse(
                eligible=False,
                eligible_amount=None,
                ceiling=None,
                next_eligible_date=None,
                message="Invalid Furniture sub-category"
            )

        # Min item value
        if payload.claim_amount < furniture_policy["min_item_value"]:
            return AssetClaimValidateResponse(
                eligible=False,
                eligible_amount=None,
                ceiling=None,
                next_eligible_date=None,
                message="Minimum item value must be ₹5,000"
            )

        # Buyback cycle check (per sub-category)
        row = db.execute(
            text("""
                SELECT acs.invoice_date
                FROM asset_claim ac
                JOIN asset_claim_submission acs
                ON ac.asset_claim_id = acs.asset_claim_id
                WHERE ac.employee_id = :employee_id
                  AND ac.category = 'Furniture'
                  AND ac.sub_category = :sub_category
                  AND ac.status = 'Approved'
                ORDER BY acs.invoice_date DESC
                LIMIT 1
            """),
            {
                "employee_id": payload.employee_id,
                "sub_category": payload.sub_category
            }
        ).fetchone()

        if row:
            next_date = calculate_next_date(row.invoice_date, furniture_policy["buyback_years"])
            if payload.invoice_date < next_date:
                return AssetClaimValidateResponse(
                    eligible=False,
                    eligible_amount=None,
                    ceiling=None,
                    next_eligible_date=next_date,
                    message="Furniture buyback cycle not completed"
                )

        ceiling = None
        if "grades" in furniture_policy:
            ceiling = furniture_policy["grades"].get(payload.grade)
            if not ceiling:
                return AssetClaimValidateResponse(
                    eligible=False,
                    eligible_amount=None,
                    ceiling=None,
                    next_eligible_date=None,
                    message="Invalid grade for Furniture Electronics"
                )

        # 1% upfront deduction
        net_amount = payload.claim_amount * 0.99

        return success_response(net_amount, ceiling, "Eligible for Furniture claim")


    # =================================================
    # FALLBACK
    # =================================================
    return AssetClaimValidateResponse(
        eligible=False,
        eligible_amount=None,
        ceiling=None,
        next_eligible_date=None,
        message="Invalid category"
    )





