from sqlalchemy.orm import Session, load_only
from sqlalchemy import func
from datetime import date, timedelta
from decimal import Decimal

from app.models.claim.asset_claim import AssetClaim
from app.models.claim.asset_claim_submission import AssetClaimSubmission
from app.models.UserModel import User


# =================================================
# HELPER: REJECTION CHECK (GLOBAL & SAFE)
# =================================================
def is_rejected(column):
    """
    Returns SQLAlchemy condition:
    TRUE if column contains 'rejected' (case-insensitive)
    """
    return func.lower(column).like("%rejected%")


# -------------------------------------------------
# Common rejection response
# -------------------------------------------------
def rejection_response(category, item_type, message):
    return {
        "category": category,
        "item_type": item_type,
        "total_entitlement_limit": Decimal(0),
        "amount_utilized": Decimal(0),
        "balance_available": Decimal(0),
        "eligibility": "",
        "can_apply": False,
        "last_claim_date": None,
        "next_eligible_date": None,
        "policy_message": message,
    }


# -------------------------------------------------
# Main entitlement function
# -------------------------------------------------
def get_asset_entitlement(
    db: Session,
    user_id: int,
    category: str,
    item_type: str,
    sub_category: str | None = None,
):
    # =================================================
    # USER VALIDATION
    # =================================================
    user = (
        db.query(User)
        .filter(User.user_id == user_id, User.is_deleted == False)
        .first()
    )

    if not user:
        raise ValueError("User not found")

    if user.employment_type != "Permanent":
        return rejection_response(
            category, item_type, "Only permanent employees are eligible"
        )

    today = date.today()

    # =================================================
    # MOBILE HANDSET
    # =================================================
    if category == "Mobile Handset":
        entitlement = Decimal(40000 if user.grade in ("E6", "E7") else 30000)
        eligibility_text = "Once in 2 years"
        cooling_days = 730

        last_claim = (
            db.query(AssetClaim)
            .join(
                AssetClaimSubmission,
                AssetClaimSubmission.asset_claim_id == AssetClaim.asset_claim_id,
            )
            .options(load_only(AssetClaim.asset_claim_id, AssetClaim.claim_date))
            .filter(
                AssetClaim.created_by == user_id,
                AssetClaim.category == category,
                ~is_rejected(AssetClaimSubmission.status),
            )
            .order_by(AssetClaim.claim_date.desc())
            .first()
        )

        if not last_claim:
            return {
                "category": category,
                "item_type": item_type,
                "total_entitlement_limit": entitlement,
                "amount_utilized": Decimal(0),
                "balance_available": entitlement,
                "eligibility": eligibility_text,
                "can_apply": True,
                "last_claim_date": None,
                "next_eligible_date": None,
                "policy_message": "Eligible for claim",
            }

        utilized = (
            db.query(func.coalesce(func.sum(AssetClaimSubmission.claim_amount), 0))
            .filter(
                AssetClaimSubmission.asset_claim_id == last_claim.asset_claim_id,
                ~is_rejected(AssetClaimSubmission.status),
            )
            .scalar()
        )

        utilized = Decimal(utilized)
        next_eligible_date = last_claim.claim_date + timedelta(days=cooling_days)

        if today < next_eligible_date:
            return {
                "category": category,
                "item_type": item_type,
                "total_entitlement_limit": entitlement,
                "amount_utilized": utilized,
                "balance_available": Decimal(0),
                "eligibility": eligibility_text,
                "can_apply": False,
                "last_claim_date": last_claim.claim_date,
                "next_eligible_date": next_eligible_date,
                "policy_message": "Eligible after completion of 2 years from last claim",
            }

        return {
            "category": category,
            "item_type": item_type,
            "total_entitlement_limit": entitlement,
            "amount_utilized": Decimal(0),
            "balance_available": entitlement,
            "eligibility": eligibility_text,
            "can_apply": True,
            "last_claim_date": last_claim.claim_date,
            "next_eligible_date": None,
            "policy_message": "Eligible for claim",
        }



    elif category == "Laptop / Desktop":
        entitlement = Decimal(60000 if user.grade in ("E6", "E7") else 50000)
        eligibility_text = "Once in 3 years"
        cooling_days = 1095
        today = date.today()

        # --------------------------------------------------
        # 1. LAST LAPTOP/DESKTOP CLAIM (NON-REJECTED)
        # ALSO FETCH SUBMISSION STATUS
        # --------------------------------------------------
        result = (
            db.query(AssetClaim, AssetClaimSubmission.status)
            .join(
                AssetClaimSubmission,
                AssetClaimSubmission.asset_claim_id == AssetClaim.asset_claim_id,
            )
            .options(
                load_only(
                    AssetClaim.asset_claim_id,
                    AssetClaim.claim_date,
                    AssetClaim.bought_back,
                )
            )
            .filter(
                AssetClaim.created_by == user_id,
                AssetClaim.category == category,
                ~is_rejected(AssetClaimSubmission.status),
            )
            .order_by(
                    AssetClaim.claim_date.desc(),
                    AssetClaimSubmission.created_at.desc()
                )

            .first()
        )

        if result:
            asset_claim, submission_status = result
        else:
            asset_claim = None
            submission_status = None

        # --------------------------------------------------
        # 2. NO PREVIOUS CLAIM → FULL ELIGIBILITY
        # --------------------------------------------------
        if not asset_claim:
            return {
                "category": category,
                "item_type": item_type,
                "total_entitlement_limit": entitlement,
                "amount_utilized": Decimal(0),
                "balance_available": entitlement,
                "eligibility": eligibility_text,
                "can_apply": True,
                "last_claim_date": None,
                "next_eligible_date": None,
                "policy_message": "Eligible for claim",
            }

        # --------------------------------------------------
        # 3. TOTAL UTILIZED (ALL NON-REJECTED LAPTOP CLAIMS)
        # --------------------------------------------------
        total_utilized = (
            db.query(func.coalesce(func.sum(AssetClaimSubmission.claim_amount), 0))
            .join(
                AssetClaim,
                AssetClaim.asset_claim_id == AssetClaimSubmission.asset_claim_id,
            )
            .filter(
                AssetClaimSubmission.created_by == user_id,
                AssetClaim.category == category,
                ~is_rejected(AssetClaimSubmission.status),
            )
            .scalar()
        )

        total_utilized = Decimal(total_utilized)

        # --------------------------------------------------
        # 4. BOUGHT-BACK AMOUNT (REMOVE FROM UTILIZED)
        # --------------------------------------------------
        bought_back_amount = (
            db.query(func.coalesce(func.sum(AssetClaimSubmission.claim_amount), 0))
            .join(
                AssetClaim,
                AssetClaim.asset_claim_id == AssetClaimSubmission.asset_claim_id,
            )
            .filter(
                AssetClaimSubmission.created_by == user_id,
                AssetClaim.category == category,
                AssetClaim.bought_back.is_(True)
,
            )
            .scalar()
        )

        bought_back_amount = Decimal(bought_back_amount)

        # --------------------------------------------------
        # 5. EFFECTIVE UTILIZATION & BALANCE
        # --------------------------------------------------
        effective_utilized = total_utilized - bought_back_amount

        if effective_utilized < 0:
            effective_utilized = Decimal(0)

        balance = entitlement - effective_utilized

        if balance > entitlement:
            balance = entitlement

        # --------------------------------------------------
        # 6. BUYBACK CHECK (FINANCE APPROVED)
        # BUYBACK OVERRIDES COOLING
        # --------------------------------------------------
        if asset_claim.bought_back and submission_status == "Asset Buyback Approved":
            return {
                "category": category,
                "item_type": item_type,
                "total_entitlement_limit": entitlement,
                "amount_utilized": Decimal(0),
                "balance_available": entitlement,
                "eligibility": eligibility_text,
                "can_apply": True,
                "last_claim_date": asset_claim.claim_date,
                "next_eligible_date": None,
                "policy_message": "Eligible for claim (Previous asset bought back)",
            }

        # --------------------------------------------------
        # 7. COOLING PERIOD CHECK
        # --------------------------------------------------
        next_eligible_date = asset_claim.claim_date + timedelta(days=cooling_days)

        if today < next_eligible_date:
            return {
                "category": category,
                "item_type": item_type,
                "total_entitlement_limit": entitlement,
                "amount_utilized": effective_utilized,
                "balance_available": Decimal(0),
                "eligibility": eligibility_text,
                "can_apply": False,
                "last_claim_date": asset_claim.claim_date,
                "next_eligible_date": next_eligible_date,
                "policy_message": "Eligible after completion of 3 years from last claim",
            }

        # --------------------------------------------------
        # 8. BUYBACK MANDATORY CHECK
        # --------------------------------------------------
        if not asset_claim.bought_back:
            return {
                "category": category,
                "item_type": item_type,
                "total_entitlement_limit": entitlement,
                "amount_utilized": effective_utilized,
                "balance_available": Decimal(0),
                "eligibility": eligibility_text,
                "can_apply": False,
                "last_claim_date": asset_claim.claim_date,
                "next_eligible_date": next_eligible_date,
                "policy_message": "Buyback must be completed before next claim",
            }

        # --------------------------------------------------
        # 9. FINAL ELIGIBLE RESPONSE
        # --------------------------------------------------
        return {
            "category": category,
            "item_type": item_type,
            "total_entitlement_limit": entitlement,
            "amount_utilized": effective_utilized,
            "balance_available": balance,
            "eligibility": eligibility_text,
            "can_apply": True,
            "last_claim_date": asset_claim.claim_date,
            "next_eligible_date": None,
            "policy_message": "Eligible for claim",
        }


    # =================================================
    # DATA CARD (FIXED JOIN)
    # =================================================
    elif category == "Data Card":
        entitlement = Decimal(1000)
        cooling_days = 1095
        eligibility_text = "Once in 3 years (Laptop mandatory)"
        today = date.today()

        # --------------------------------------------------
        # 1. CHECK LAPTOP CLAIM EXISTS (NON-REJECTED)
        # --------------------------------------------------
        laptop_claim = (
            db.query(AssetClaim)
            .select_from(AssetClaim)   # 👈 IMPORTANT FIX
            .join(
                AssetClaimSubmission,
                AssetClaimSubmission.asset_claim_id == AssetClaim.asset_claim_id,
            )
            .filter(
                AssetClaim.created_by == user_id,
                AssetClaim.category == "Laptop / Desktop",
                ~is_rejected(AssetClaimSubmission.status),
            )
            .first()
        )

        if not laptop_claim:
            return {
                "category": category,
                "item_type": item_type,
                "total_entitlement_limit": entitlement,
                "amount_utilized": Decimal(0),
                "balance_available": entitlement,
                "eligibility": eligibility_text,
                "can_apply": False,
                "last_claim_date": None,
                "next_eligible_date": None,
                "policy_message": "Laptop/Desktop must be claimed before Data Card",
            }

        # --------------------------------------------------
        # 2. LAST DATA CARD CLAIM
        # --------------------------------------------------
        data_card_claim = (
            db.query(AssetClaim)
            .select_from(AssetClaim)   # 👈 IMPORTANT FIX
            .join(
                AssetClaimSubmission,
                AssetClaimSubmission.asset_claim_id == AssetClaim.asset_claim_id,
            )
            .options(load_only(AssetClaim.asset_claim_id, AssetClaim.claim_date))
            .filter(
                AssetClaim.created_by == user_id,
                AssetClaim.category == "Data Card",
                ~is_rejected(AssetClaimSubmission.status),
            )
            .order_by(AssetClaim.claim_date.desc())
            .first()
        )

        if not data_card_claim:
            return {
                "category": category,
                "item_type": item_type,
                "total_entitlement_limit": entitlement,
                "amount_utilized": Decimal(0),
                "balance_available": entitlement,
                "eligibility": eligibility_text,
                "can_apply": True,
                "last_claim_date": None,
                "next_eligible_date": None,
                "policy_message": "Eligible for claim",
            }

        # --------------------------------------------------
        # 3. UTILIZED AMOUNT
        # --------------------------------------------------
        utilized = (
            db.query(func.coalesce(func.sum(AssetClaimSubmission.claim_amount), 0))
            .filter(
                AssetClaimSubmission.asset_claim_id == data_card_claim.asset_claim_id,
                ~is_rejected(AssetClaimSubmission.status),
            )
            .scalar()
        )

        utilized = Decimal(utilized)
        next_eligible_date = data_card_claim.claim_date + timedelta(days=cooling_days)

        if today < next_eligible_date:
            return {
                "category": category,
                "item_type": item_type,
                "total_entitlement_limit": entitlement,
                "amount_utilized": utilized,
                "balance_available": Decimal(0),
                "eligibility": eligibility_text,
                "can_apply": False,
                "last_claim_date": data_card_claim.claim_date,
                "next_eligible_date": next_eligible_date,
                "policy_message": "Eligible after completion of 3 years from last claim",
            }

        return {
            "category": category,
            "item_type": item_type,
            "total_entitlement_limit": entitlement,
            "amount_utilized": Decimal(0),
            "balance_available": entitlement,
            "eligibility": eligibility_text,
            "can_apply": True,
            "last_claim_date": data_card_claim.claim_date,
            "next_eligible_date": None,
            "policy_message": "Eligible for claim",
        }


    # =================================================
    # FURNITURE (BALANCE BASED)
    # =================================================
    elif category == "Furniture":
        if not sub_category:
            return rejection_response(
                category, item_type, "Furniture sub-category is required"
            )

        # -----------------------------
        # Grade based entitlement
        # -----------------------------
        grade_ceiling = {
            "E1": 100000,
            "E2": 100000,
            "E3": 140000,
            "E4": 140000,
            "E5": 165000,
            "E6": 225000,
            "E7": 280000,
        }

        entitlement = Decimal(grade_ceiling.get(user.grade, 0))

        eligibility_text = (
            "Buyback allowed after 6 years"
            if sub_category == "Utility & Decorative Furniture"
            else "Buyback allowed after 4 years"
        )

        # --------------------------------------------------
        # 1. TOTAL UTILIZED (ALL NON-REJECTED CLAIMS)
        # --------------------------------------------------
        total_utilized = (
            db.query(func.coalesce(func.sum(AssetClaimSubmission.claim_amount), 0))
            .filter(
                AssetClaimSubmission.created_by == user_id,
                AssetClaim.category == "Furniture",
                ~is_rejected(AssetClaimSubmission.status),
            )
            .join(
                AssetClaim,
                AssetClaim.asset_claim_id == AssetClaimSubmission.asset_claim_id,
            )

            .scalar()
        )

        total_utilized = Decimal(total_utilized)

        # --------------------------------------------------
        # 2. BOUGHT-BACK AMOUNT (REMOVE FROM UTILIZED)
        # --------------------------------------------------
        bought_back_amount = (
            db.query(func.coalesce(func.sum(AssetClaimSubmission.claim_amount), 0))
            .join(
                AssetClaim,
                AssetClaim.asset_claim_id == AssetClaimSubmission.asset_claim_id,
            )
            .filter(
                AssetClaimSubmission.created_by == user_id,
                AssetClaim.category == "Furniture",
                AssetClaim.bought_back.is_(True),
                AssetClaimSubmission.status == "Asset Buyback Approved",
            )
            .scalar()
        )

        bought_back_amount = Decimal(bought_back_amount)

        # --------------------------------------------------
        # 3. EFFECTIVE UTILIZATION & BALANCE
        # --------------------------------------------------
        effective_utilized = total_utilized - bought_back_amount
        balance = entitlement - effective_utilized

        # --------------------------------------------------
        # 4. LAST CLAIM DATE
        # --------------------------------------------------
        last_claim = (
            db.query(AssetClaim)
            .options(load_only(AssetClaim.claim_date))
            .filter(
                AssetClaim.created_by == user_id,
                AssetClaim.category == category,
            )
            .order_by(AssetClaim.claim_date.desc())
            .first()
        )

        # --------------------------------------------------
        # 5. RESPONSE
        # --------------------------------------------------
        if balance <= 0:
            return {
                "category": category,
                "item_type": item_type,
                "total_entitlement_limit": entitlement,
                "amount_utilized": effective_utilized,
                "balance_available": Decimal(0),
                "eligibility": eligibility_text,
                "can_apply": False,
                "last_claim_date": last_claim.claim_date if last_claim else None,
                "next_eligible_date": None,
                "policy_message": "Furniture entitlement fully utilized",
            }

        return {
            "category": category,
            "item_type": item_type,
            "total_entitlement_limit": entitlement,
            "amount_utilized": effective_utilized,
            "balance_available": balance,
            "eligibility": eligibility_text,
            "can_apply": True,
            "last_claim_date": last_claim.claim_date if last_claim else None,
            "next_eligible_date": None,
            "policy_message": "Eligible for claim",
        }



    # =================================================
    # INVALID CATEGORY
    # =================================================
    return rejection_response(category, item_type, "Invalid category")



