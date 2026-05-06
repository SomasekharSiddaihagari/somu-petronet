from decimal import Decimal
from fastapi import HTTPException
from typing import List
from app.models.claim.allowance_admission_child import AllowanceAdmissionChild
from app.models.claim.allowance_claim import AllowanceClaim
from app.schemas.claim.allowance_validation_schema import AdmissionChild
 
 
# -------------------------

# Grade-wise limits

# -------------------------

PACKING_GRADE_LIMITS = {

    "E1": Decimal("13000"),

    "E2": Decimal("13000"),

    "E3": Decimal("13000"),

    "E4": Decimal("13000"),

    "E5": Decimal("16000"),

    "E6": Decimal("16000"),

    "E7": Decimal("16000"),

}
 
 
# -------------------------

# Packing Charges Validation

# -------------------------

def validate_packing_charges(grade: str, amount_claimed: Decimal):

    if grade not in PACKING_GRADE_LIMITS:

        raise HTTPException(

            status_code=400,

            detail="Invalid grade"

        )
 
    max_allowed = PACKING_GRADE_LIMITS[grade]
 
    if amount_claimed > max_allowed:

        raise HTTPException(

            status_code=400,

            detail=f"Packing & loading charges for grade {grade} cannot exceed ₹{max_allowed}"

        )
 
    return {

        "status": "APPROVED",

        "grade": grade,

        "approved_amount": amount_claimed,

        "max_allowed": max_allowed

    }
 
 


from sqlalchemy.orm import Session
from decimal import Decimal
from fastapi import HTTPException


from decimal import Decimal
from fastapi import HTTPException
from sqlalchemy.orm import Session


from decimal import Decimal
from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func


def validate_admission_claim(
    user_id: int,
    station_id: int,
    city: str,
    children: list[AdmissionChild],
    db: Session
):

    MAX_CHILDREN = 2

    # ======================================================
    # CITY → PER CHILD LIMIT
    # ======================================================
    CITY_ALLOWANCE = {
        "blr_devn": Decimal("45000"),
        "mangalore": Decimal("35000"),
        "neriya": Decimal("30000"),
        "hassan": Decimal("30000"),
    }

    city_key = city.lower().strip()

    if city_key not in CITY_ALLOWANCE:
        raise HTTPException(
            status_code=200,
            detail="Invalid city for admission allowance."
        )

    PER_CHILD_LIMIT = CITY_ALLOWANCE[city_key]

    # ======================================================
    # STEP 1: Count ONLY ACTIVE (non-rejected) children
    # ======================================================
    existing_children_count = (
        db.query(AllowanceAdmissionChild)
        .join(
            AllowanceClaim,
            AllowanceAdmissionChild.allowance_claim_id
            == AllowanceClaim.allowance_claim_id
        )
        .filter(
            AllowanceAdmissionChild.user_id == user_id,
            AllowanceAdmissionChild.station_id == station_id,
            ~AllowanceClaim.status.ilike("%rejected%") | ~AllowanceClaim.status.ilike("%auto lapsed%")
        )
        .count()
    )

    # ======================================================
    # STEP 2: Prevent exceeding child limit
    # ======================================================
    if existing_children_count + len(children) > MAX_CHILDREN:
        raise HTTPException(
            status_code=200,
            detail="Admission allowance allowed only for 2 children per station."
        )

    # ======================================================
    # STEP 3: Already claimed child names (ACTIVE ONLY)
    # ======================================================
    existing_children = (
        db.query(AllowanceAdmissionChild.child_name)
        .join(
            AllowanceClaim,
            AllowanceAdmissionChild.allowance_claim_id
            == AllowanceClaim.allowance_claim_id
        )
        .filter(
            AllowanceAdmissionChild.user_id == user_id,
            AllowanceAdmissionChild.station_id == station_id,
            ~AllowanceClaim.status.ilike("%rejected%") | ~AllowanceClaim.status.ilike("%auto lapsed%")
        )
        .all()
    )

    claimed_child_names = {
        c.child_name.lower().strip()
        for c in existing_children
        if c.child_name
    }

    # ======================================================
    # STEP 4: Prevent duplicate names in SAME request
    # ======================================================
    incoming_names = [
        c.child_name.lower().strip()
        for c in children
        if c.child_name
    ]

    if len(incoming_names) != len(set(incoming_names)):
        raise HTTPException(
            status_code=200,
            detail="Duplicate child found in request."
        )

    # ======================================================
    # STEP 5: Per-child validation
    # ======================================================
    total_amount = Decimal("0")

    for child in children:

        child_name = child.child_name.lower().strip()

        # already claimed?
        if child_name in claimed_child_names:
            raise HTTPException(
                status_code=200,
                detail=f"Admission allowance already claimed for {child.child_name} at this station."
            )

        # per child limit
        if child.amount_claimed > PER_CHILD_LIMIT:
            raise HTTPException(
                status_code=200,
                detail=f"{child.child_name} exceeds per child limit of ₹{PER_CHILD_LIMIT}"
            )

        total_amount += child.amount_claimed

    # ======================================================
    # SUCCESS RESPONSE
    # ======================================================
    return {
        "status": "APPROVED",
        "city": city.title(),
        "per_child_limit": PER_CHILD_LIMIT,
        "children_count": len(children),
        "total_approved_amount": total_amount
    }
