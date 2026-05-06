from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.orm import Session

from sqlalchemy import text

from datetime import date, datetime

from pydantic import BaseModel, Field
 
from app.database import get_db
 
router = APIRouter(

    prefix="/da_meal",

    tags=["Allowance Validation"],

)
 
# =========================================================

# REQUEST SCHEMA (ONLY ADDITION)

# =========================================================
 
class AllowanceValidationRequest(BaseModel):

    user_id: int

    claim_type: str 

    claim_date: date
 
 
# =========================================================

# CORE VALIDATION FUNCTION (UNCHANGED)

# =========================================================
def check_da_meal_conflict(
    db: Session,
    user_id: int,
    claim_date: date,
):
    """
    Prevent:
    - Multiple meals on same date
    - DA + Meal on same date
    - Multiple DA on same date
    """

    # ---------- Check DA ----------
    da_sql = """
        SELECT 1
        FROM daily_allowance_sheet_detail d
        JOIN daily_allowance_sheet s ON s.da_sheet_id = d.da_sheet_id
        WHERE d.user_id = :uid
          AND DATE(d.from_date_time) = :dt
          AND LOWER(s.status) NOT IN ('rejected', 'cancelled')
        LIMIT 1;
    """

    da_exists = db.execute(
        text(da_sql),
        {"uid": user_id, "dt": claim_date},
    ).fetchone()

    # ---------- Check Meal ----------
    meal_sql = """
        SELECT 1
        FROM meal_allowance_sheet_detail m
        JOIN meal_allowance_sheet s ON s.meal_sheet_id = m.meal_sheet_id
        WHERE s.user_id = :uid
          AND m.date = :dt
          AND LOWER(s.status) NOT IN ('rejected', 'cancelled')
        LIMIT 1;
    """

    meal_exists = db.execute(
        text(meal_sql),
        {"uid": user_id, "dt": claim_date},
    ).fetchone()

    # ---------- FINAL DECISION ----------
    if da_exists and meal_exists:
        return False, "Daily Allowance and Meal Allowance already claimed for this date."

    if da_exists:
        return False, "Daily Allowance already claimed for this date."

    if meal_exists:
        return False, "Meal Allowance already claimed for this date."

    return True, "Allowance can be claimed for this date."

# =========================================================

# SINGLE POST API (FINAL)

# =========================================================
@router.post("/validate")
def validate_da_meal(
    req: AllowanceValidationRequest,
    db: Session = Depends(get_db),
):
    can_apply, message = check_da_meal_conflict(
        db=db,
        user_id=req.user_id,
        claim_date=req.claim_date,
    )

    return {
        "can_apply": can_apply,
        "message": message
    }
 