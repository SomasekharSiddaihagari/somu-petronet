from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, Field
from typing import Optional
from datetime import date, datetime
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.database import get_db

router = APIRouter(prefix="/api/travel", tags=["Travel Validation"])

# =====================================================
# CITY GROUPS
# =====================================================
METRO_CITIES = ["delhi", "kolkata", "mumbai", "chennai"]

A_CLASS_CITIES = [
    "delhi", "noida", "gurgaon", "faridabad", "ghaziabad",
    "mumbai", "kolkata", "chennai", "bangalore", "hyderabad"
]

# =====================================================
# POLICY LIMITS (AS PER OLD FILE)
# =====================================================
DA_LIMITS = {
    "E1": {"aclass": 1400, "other": 1250},
    "E2": {"aclass": 1400, "other": 1250},
    "E3": {"aclass": 1400, "other": 1250},
    "E4": {"aclass": 1400, "other": 1250},
    "E5": {"aclass": 1500, "other": 1350},
    "E6": {"aclass": 1700, "other": 1500},
    "E7": {"aclass": 1900, "other": 1750},
    "MD": {"aclass": 1900, "other": 1750},
    "PMHBL": {"aclass": 1900, "other": 1750},
}

HOTEL_LIMITS = {
    "E1": {"metro": 4500, "other": 3000},
    "E2": {"metro": 4500, "other": 3000},
    "E3": {"metro": 4500, "other": 3000},
    "E4": {"metro": 6500, "other": 4500},
    "E5": {"metro": 6500, "other": 4500},
    "E6": {"metro": 8500, "other": 6500},
    "E7": {"metro": 8500, "other": 6500},
    "MD": {"metro": None, "other": None},
    "PMHBL": {"metro": None, "other": None},
}

OVERSEAS_HOTEL_LIMIT = 150  # USD/day
OVERSEAS_DA_LIMIT = 50     # USD/day

# =====================================================
# INTERNAL: GRADE RESOLUTION (ONLY CHANGE)
# =====================================================
def get_effective_grade(db: Session, user_id: int) -> str:
    md = db.execute(
        text("""
            SELECT 1
            FROM role_permissions
            WHERE user_id = :uid
              AND submenu_id = 11
              AND role_id = 10
            LIMIT 1
        """),
        {"uid": user_id}
    ).fetchone()

    if md:
        return "MD"

    row = db.execute(
        text("SELECT grade FROM users WHERE user_id = :uid"),
        {"uid": user_id}
    ).fetchone()

    if not row or not row[0]:
        raise HTTPException(404, "User grade not found")

    return row[0].upper().strip()

# =====================================================
# 1️⃣ DA VALIDATION API
# =====================================================
class DAValidationInput(BaseModel):
    user_id: int
    travel_to: str
    from_date_time: datetime
    to_date_time: datetime
    distance_from_station: float
    day_count_at_same_station: int


def calculate_hours(start_dt: datetime, end_dt: datetime) -> float:
    diff_sec = (end_dt - start_dt).total_seconds()
    return max(diff_sec / 3600, 0)


@router.post("/validate-da")
def validate_da(
    data: DAValidationInput,
    db: Session = Depends(get_db)
):
    grade = get_effective_grade(db, data.user_id)
    city = data.travel_to.lower().strip()

    if grade not in DA_LIMITS:
        raise HTTPException(400, f"Invalid grade {grade}")

    result = {
        "eligible": True,
        "violation": False,
        "violation_reason": None,
        "hours": None,
        "time_entitlement_factor": None,
        "base_da_per_day": None,
        "prolonged_halt_factor": None,
        "final_da_amount": None
    }

    if data.distance_from_station <= 15:
        result.update({
            "eligible": False,
            "violation": True,
            "violation_reason": "DISTANCE_NOT_ELIGIBLE (<= 15 KM)"
        })
        return result

    hours = calculate_hours(data.from_date_time, data.to_date_time)
    result["hours"] = round(hours, 2)

    if hours < 6:
        time_factor = 0.25
    elif hours < 12:
        time_factor = 0.50
    else:
        time_factor = 1.00

    result["time_entitlement_factor"] = time_factor

    city_type = "aclass" if city in A_CLASS_CITIES else "other"
    base_da = DA_LIMITS[grade][city_type]
    result["base_da_per_day"] = base_da

    d = data.day_count_at_same_station
    halt_factor = 1.0 if d <= 30 else 0.75 if d <= 45 else 0.50
    result["prolonged_halt_factor"] = halt_factor

    result["final_da_amount"] = round(base_da * time_factor * halt_factor, 2)
    return result




# CONSTANTS (replace with your actual values)
# -----------------------------------------------------

A_CLASS_CITIES =[
    "delhi", "noida", "gurgaon", "faridabad", "ghaziabad",
    "mumbai", "kolkata", "chennai", "bangalore", "hyderabad"
]
METRO_CITIES = ["delhi", "mumbai", "kolkata", "chennai", "bangalore"]

DA_LIMITS = {
    "E1": {"aclass": 1400, "other": 1250},
    "E2": {"aclass": 1400, "other": 1250},
    "E3": {"aclass": 1400, "other": 1250},
    "E4": {"aclass": 1400, "other": 1250},
    "E5": {"aclass": 1500, "other": 1350},
    "E6": {"aclass": 1700, "other": 1500},
    "E7": {"aclass": 1900, "other": 1750},
            "MD": {"aclass": 1900, "other": 1750},
    "PMHBL": {"aclass": 1900, "other": 1750},
}

HOTEL_LIMITS = {
    "E1": {"metro": 4500, "other": 3000},
    "E2": {"metro": 4500, "other": 3000},
    "E3": {"metro": 4500, "other": 3000},
    "E4": {"metro": 6500, "other": 4500},
    "E5": {"metro": 6500, "other": 4500},
    "E6": {"metro": 8500, "other": 6500},
    "E7": {"metro": 8500, "other": 6500},
    "MD": {"metro": None, "other": None},
    "PMHBL": {"metro": None, "other": None},
}

# -----------------------------------------------------
# REQUEST MODEL
# -----------------------------------------------------

class ExpenseValidationDomestic(BaseModel):
    user_id: int
    from_location: Optional[str] = ""
    to_location: str
    from_date: date
    to_date: date
    days: int                     # used ONLY for DA
    hotel_amount: Optional[float] = 0.0
    daily_allowance_amount: Optional[float] = 0.0
    is_amount_total: bool = True


# -----------------------------------------------------
# DA SLAB HELPER (USES TOUR DAYS)
# -----------------------------------------------------

def calculate_city_da_total(
    total_tour_days: int,
    city_days: int,
    da_per_day: float
) -> float:
    city_start = total_tour_days - city_days + 1
    city_end = total_tour_days

    days_100 = max(0, min(city_end, 30) - max(city_start, 1) + 1)
    days_75 = max(0, min(city_end, 45) - max(city_start, 31) + 1)
    days_50 = max(0, city_end - max(city_start, 46) + 1)

    total = (
        days_100 * da_per_day +
        days_75 * da_per_day * 0.75 +
        days_50 * da_per_day * 0.5
    )

    return round(total, 2)


# -----------------------------------------------------
# API ENDPOINT
# -----------------------------------------------------

@router.post("/validate-expense-domestic")
def validate_expense_domestic(
    data: ExpenseValidationDomestic,
    db: Session = Depends(get_db)
):
    grade = get_effective_grade(db, data.user_id)
    print(grade)
    grade=grade.upper()
    to_city = data.to_location.lower().strip()

    # ---------- DATE VALIDATION ----------
    if data.to_date < data.from_date:
        raise HTTPException(
            status_code=400,
            detail="to_date must be same or after from_date"
        )

    # ---------- CITY DAYS (ONLY FROM DATES) ----------
    city_days = (data.to_date - data.from_date).days + 1

    if city_days <= 0:
        raise HTTPException(400, "Invalid date range")

    # ---------- CLAIMED VALUES ----------
    hotel_per_day_claimed = (
        data.hotel_amount / city_days
        if data.is_amount_total else data.hotel_amount
    )

    da_per_day_claimed = (
        data.daily_allowance_amount / city_days
        if data.is_amount_total else data.daily_allowance_amount
    )

    # ---------- RESPONSE (UNCHANGED STRUCTURE) ----------
    result = {
        "days": city_days,
        "hotel": {
            "claimed_total": round(hotel_per_day_claimed * city_days, 2),
            "claimed_per_day": round(hotel_per_day_claimed, 2),
            "allowed_per_day": None,
            "allowed_total": None,
            "violation": False,
            "violation_type": None
        },
        "daily_allowance": {
            "claimed_total": round(da_per_day_claimed * city_days, 2),
            "claimed_per_day": round(da_per_day_claimed, 2),
            "allowed_per_day": None,
            "allowed_total": None,
            "violation": False,
            "violation_type": None
        }
    }

    # =================================================
    # HOTEL — ONLY FROM_DATE → TO_DATE (NO TOUR DAYS)
    # =================================================
# ---------- HOTEL (DOMESTIC) ----------
    allowed_per_day = None

    if grade in HOTEL_LIMITS:
        city_type = "metro" if to_city in METRO_CITIES else "other"
        allowed_per_day = HOTEL_LIMITS[grade][city_type]

        # 👇 IMPORTANT: handle None allowance (MD / PMHBL)
        if allowed_per_day is None:
            result["hotel"]["allowed_per_day"] = None
            result["hotel"]["allowed_total"] = None
            result["hotel"]["violation"] = False
            result["hotel"]["violation_type"] = "NO_HOTEL_LIMIT_DEFINED"
        else:
            result["hotel"]["allowed_per_day"] = allowed_per_day
            result["hotel"]["allowed_total"] = round(
                allowed_per_day * city_days, 2
            )

            if hotel_per_day_claimed > allowed_per_day:
                result["hotel"]["violation"] = True
                result["hotel"]["violation_type"] = "HOTEL_LIMIT_EXCEEDED_PER_DAY"
    # =================================================
    # DAILY ALLOWANCE — USES TOUR DAYS + SLAB
    # =================================================
    if grade in DA_LIMITS  :
        # print(to_city)
        # print(A_CLASS_CITIES)
        city_type = "aclass" if to_city in A_CLASS_CITIES else "other"
        # print(grade)
        # print(city_type)


        allowed_per_day = DA_LIMITS[grade][city_type]
        # print(allowed_per_day)
        allowed_total = calculate_city_da_total(
            total_tour_days=data.days,   # ONLY DA uses this
            city_days=city_days,
            da_per_day=allowed_per_day
        )

        result["daily_allowance"]["allowed_per_day"] = allowed_per_day
        result["daily_allowance"]["allowed_total"] = allowed_total

        if result["daily_allowance"]["claimed_total"] > allowed_total:
            result["daily_allowance"]["violation"] = True
            result["daily_allowance"]["violation_type"] = "DA_LIMIT_EXCEEDED_SLAB"

    return result


OVERSEAS_ELIGIBLE_GRADES = ["E5", "E6", "E7", "MD", "PMHBL"]

OVERSEAS_HOTEL_LIMIT = 150.0   # USD per day
OVERSEAS_DA_LIMIT = 50.0       # USD per day


class ExpenseValidationInternational(BaseModel):
    user_id: int
    from_location: str
    to_location: str
    from_date: date
    to_date: date
    hotel_amount: Optional[float] = 0.0
    daily_allowance_amount: Optional[float] = 0.0
    is_overseas: bool = False
    currency: str = "INR"
    customer_entertainment: bool = False
    is_amount_total: bool = True


# -----------------------------------------------------
# API ENDPOINT
# -----------------------------------------------------

@router.post("/validate-expense-international")
def validate_expense_international(
    data: ExpenseValidationInternational,
    db: Session = Depends(get_db)
):
    grade = get_effective_grade(db, data.user_id)

    # ---------- DATE VALIDATION ----------
    if data.to_date < data.from_date:
        raise HTTPException(
            status_code=400,
            detail="to_date must be same or after from_date"
        )

    # ---------- DAYS (STRICTLY DATE-BASED) ----------
    days = (data.to_date - data.from_date).days + 1

    # ---------- CLAIMED PER DAY ----------
    hotel_per_day_claimed = (
        data.hotel_amount / days
        if data.is_amount_total else data.hotel_amount
    )

    da_per_day_claimed = (
        data.daily_allowance_amount / days
        if data.is_amount_total else data.daily_allowance_amount
    )

    # ---------- RESPONSE (UNCHANGED STRUCTURE) ----------
    result = {
        "days": days,
        "hotel": {
            "claimed_total": round(hotel_per_day_claimed * days, 2),
            "claimed_per_day": round(hotel_per_day_claimed, 2),
            "allowed_per_day": None,
            "allowed_total": None,
            "violation": False,
            "violation_type": None
        },
        "daily_allowance": {
            "claimed_total": round(da_per_day_claimed * days, 2),
            "claimed_per_day": round(da_per_day_claimed, 2),
            "allowed_per_day": None,
            "allowed_total": None,
            "violation": False,
            "violation_type": None
        },
        "overseas_violation": False,
        "overseas_reason": None
    }

    # =================================================
    # OVERSEAS VALIDATION RULES
    # =================================================
    if data.is_overseas:

        # ---- Grade eligibility ----
        if grade not in OVERSEAS_ELIGIBLE_GRADES:
            result["overseas_violation"] = True
            result["overseas_reason"] = "GRADE_NOT_ELIGIBLE_FOR_OVERSEAS"
            return result

        # ---- Currency must be USD ----
        if data.currency != "USD":
            result["overseas_violation"] = True
            result["overseas_reason"] = "OVERSEAS_EXPENSES_MUST_BE_USD"
            return result

        # ---- Customer entertainment rule ----
        if data.customer_entertainment and grade != "MD":
            result["overseas_violation"] = True
            result["overseas_reason"] = "CUSTOMER_ENTERTAINMENT_REQUIRES_MD_APPROVAL"
            return result

        # =================================================
        # HOTEL — OVERSEAS (DATE BASED, ACTUALS)
        # =================================================
        result["hotel"]["allowed_per_day"] = OVERSEAS_HOTEL_LIMIT
        result["hotel"]["allowed_total"] = round(
            OVERSEAS_HOTEL_LIMIT * days, 2
        )

        if hotel_per_day_claimed > OVERSEAS_HOTEL_LIMIT:
            result["hotel"]["violation"] = True
            result["hotel"]["violation_type"] = (
                "OVERSEAS_HOTEL_LIMIT_PER_DAY_EXCEEDED"
            )

        # =================================================
        # DAILY ALLOWANCE — OVERSEAS (DATE BASED)
        # =================================================
        result["daily_allowance"]["allowed_per_day"] = OVERSEAS_DA_LIMIT
        result["daily_allowance"]["allowed_total"] = round(
            OVERSEAS_DA_LIMIT * days, 2
        )

        if da_per_day_claimed > OVERSEAS_DA_LIMIT:
            result["daily_allowance"]["violation"] = True
            result["daily_allowance"]["violation_type"] = (
                "OVERSEAS_DA_LIMIT_PER_DAY_EXCEEDED"
            )

    return result