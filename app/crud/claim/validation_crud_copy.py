from datetime import datetime
from decimal import ROUND_FLOOR, Decimal
from collections import defaultdict

from sqlalchemy import text

from collections import defaultdict
from decimal import Decimal
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.models.UserModel import User
from app.models.claim.out_of_pocket_claim import OutOfPocketClaim
from app.models.claim.out_of_pocket_claim_entry import OutOfPocketClaimEntry
from app.models.employees_info.user_vehicle import UserVehicle
from app.models.claim.asset_claim import AssetClaim
from app.models.claim.asset_claim_submission import AssetClaimSubmission
# from app.models.OutOfPocketClaim import OutOfPocketClaim
# from app.models.OutOfPocketClaimEntry import OutOfPocketClaimEntry


ACTIVE_STATUSES = [
 "Pending Supervisor Approval",
 "Pending HR Apporval",
 "Pending Finance Apporval",
 "Out of Pocket Approved"
]


ALLOWED_ENTRY_TYPES = {
    "NORMAL_DAY",
    "HOLIDAY_NON_ROTATING",
    "HOLIDAY_ROTATING",
}

ENTRY_TYPE_MAX_HOURS = {
    "NORMAL_DAY": Decimal("8"),
    "HOLIDAY_NON_ROTATING": Decimal("8"),
    "HOLIDAY_ROTATING": Decimal("8"),
}

OPA_SLABS = {
    "NORMAL_DAY": {
        "2-4": Decimal("250"),
        "4-6": Decimal("750"),
        "6-8": Decimal("915"),
        "8": Decimal("1650"),
    },
    "HOLIDAY_NON_ROTATING": {
        "4-6": Decimal("1150"),
        "6-8": Decimal("1315"),
        "8": Decimal("1685"),
    },
    "HOLIDAY_ROTATING": {
        "8": Decimal("1285"),
    },
}

MAX_ENTRIES_PER_MONTH = 8


def resolve_slab_amount(entry_type: str, hour_slab: str):
    slabs = OPA_SLABS.get(entry_type)
    if not slabs:
        return None
    return slabs.get(hour_slab)


# 🔥 NEW (ONLY ADDITION): DB-backed monthly count
def get_existing_monthly_entry_count(
    db: Session,
    user_id: int,
    claim_month_year: str,
) -> int:
    count = (
        db.query(func.count(OutOfPocketClaimEntry.out_of_pocket_claim_entry_id))
        .join(
            OutOfPocketClaim,
            OutOfPocketClaim.out_of_pocket_claim_id
            == OutOfPocketClaimEntry.out_of_pocket_claim_id,
        )
        .filter(
            OutOfPocketClaim.created_by == user_id,
            OutOfPocketClaim.claim_month_year == claim_month_year,
            OutOfPocketClaim.status.in_(ACTIVE_STATUSES),
        )
        .scalar()
    )

    return count or 0


def validate_out_of_pocket(db: Session, payload):
    errors = []
    total_amount = Decimal("0")

    # -------------------------
    # Master-level checks
    # -------------------------
    if not payload.declaration_accepted:
        errors.append("Declaration must be accepted")

    if not payload.entries:
        errors.append("At least one claim entry is required")

    if len(payload.entries) > MAX_ENTRIES_PER_MONTH:
        errors.append("Maximum 8 claim entries allowed per calendar month")

    try:
        datetime.strptime(payload.claim_month_year, "%Y-%m")
    except ValueError:
        errors.append("claim_month_year must be in YYYY-MM format")

    if errors:
        return errors, None, None

    # -------------------------
    # 🔥 USER + MONTH LIMIT CHECK (ADDED)
    # -------------------------
    existing_count = get_existing_monthly_entry_count(
        db=db,
        user_id=payload.user_id,
        claim_month_year=payload.claim_month_year,
    )

    incoming_count = len(payload.entries)

    # 🔥 NEW RULE: Only ONE claim request allowed per month
    if existing_count >= 1:
        errors.append(
            f"You have already submitted an Out of Pocket claim for "
            f"{payload.claim_month_year}. Multiple claims in the same month are not allowed."
        )
        return errors, None, None


    # -------------------------
    # Entry-level checks (UNCHANGED)
    # -------------------------
    duplicate_check = defaultdict(set)

    for idx, entry in enumerate(payload.entries, start=1):

        if entry.entry_type not in ALLOWED_ENTRY_TYPES:
            errors.append(f"Entry {idx}: Invalid entry type {entry.entry_type}")
            continue

        if not isinstance(entry.hours, str):
            errors.append(f"Entry {idx}: hours must be a string slab like '2-4'")
            continue

        slab_amount = resolve_slab_amount(entry.entry_type, entry.hours)
        if not slab_amount:
            errors.append(
                f"Entry {idx}: Invalid hour slab '{entry.hours}' for {entry.entry_type}"
            )
            continue

        if entry.claim_date.strftime("%Y-%m") != payload.claim_month_year:
            errors.append(
                f"Entry {idx}: Date {entry.claim_date} outside claim month {payload.claim_month_year}"
            )

        if entry.entry_type in duplicate_check[entry.claim_date]:
            errors.append(
                f"Entry {idx}: Duplicate {entry.entry_type} entry for {entry.claim_date}"
            )
        duplicate_check[entry.claim_date].add(entry.entry_type)

        if not entry.justification.strip():
            errors.append(f"Entry {idx}: Justification is required")

        entry.amount = slab_amount
        total_amount += slab_amount

    if errors:
        return errors, None, None

    return None, incoming_count, total_amount


# --------------------------------------out of the pocket validation endes here -------------------------------------------------------#

from datetime import datetime
from decimal import Decimal

GRADE_ANNUAL_LIMITS = {
    "E1": Decimal("8400"),
    "E2": Decimal("8400"),
    "E3": Decimal("8400"),
    "E4": Decimal("12000"),
    "E5": Decimal("12000"),
    "E6": Decimal("12000"),
    "E7": Decimal("12000"),
}


def validate_mobile_bill(payload):
    errors = []
 
    # -------------------------
    # Basic eligibility
    # -------------------------
    if payload.employee_employment_type != "Permanent" and payload.employee_employment_type != "Probation":
        errors.append("Mobile bill reimbursement allowed only for Permanent employees")
 
    if not payload.declaration_accepted:
        errors.append("Declaration must be accepted")
 
    try:
        datetime.strptime(payload.bill_month_year, "%Y-%m")
    except ValueError:
        errors.append("bill_month_year must be in YYYY-MM format")
 
    if payload.employee_grade not in GRADE_ANNUAL_LIMITS:
        errors.append("Invalid employee grade")
 
    # -------------------------
    # Number & amount validation
    # -------------------------
    numbers = []
    total_amount = Decimal("0")
 
    if payload.mobile_number_1:
        if not payload.bill_amount_1 or payload.bill_amount_1 <= 0:
            errors.append("Bill amount required for mobile_number_1")
        else:
            numbers.append(payload.mobile_number_1)
            total_amount += payload.bill_amount_1
 
    if payload.mobile_number_2:
        if not payload.bill_amount_2 or payload.bill_amount_2 <= 0:
            errors.append("Bill amount required for mobile_number_2")
        else:
            numbers.append(payload.mobile_number_2)
            total_amount += payload.bill_amount_2
 
    if not numbers:
        errors.append("At least one mobile or landline number is required")
 
    if len(numbers) > 2:
        errors.append("Maximum two numbers allowed (1 mobile + 1 landline OR 2 mobiles)")
 
    if len(numbers) == 2 and numbers[0] == numbers[1]:
        errors.append("Duplicate mobile/landline numbers are not allowed")
 
    if errors:
        return errors, None, None
 
    # -------------------------
    # Monthly limit calculation
    # -------------------------
    annual_limit = GRADE_ANNUAL_LIMITS[payload.employee_grade]
    monthly_limit = (annual_limit / Decimal("12")).quantize(Decimal("0.01"))
 
    if total_amount > monthly_limit:
        errors.append(
            f"Total claimed amount ₹{total_amount} exceeds monthly limit ₹{monthly_limit}"
        )
 
    if errors:
        return errors, None, None
 
    return None, total_amount, monthly_limit
 
 
 

# --------------------------------------Mobile Bill Reimbursement validation endes here -------------------------------------------------------#

from datetime import datetime
from decimal import Decimal
from app.models.claim.furniture_rm_reimbursement import FurnitureRMReimbursement
from datetime import datetime
from decimal import Decimal
from sqlalchemy.orm import Session
from sqlalchemy import func


# PERCENTAGE_LIMIT = Decimal("15")  # 15%

# def validate_furniture_rm(payload, db: Session):
#     errors = []

#     # --------------------------------------------------
#     # BASIC ELIGIBILITY
#     # --------------------------------------------------
#     if payload.employee_employment_type != "Permanent":
#         errors.append("Furniture R&M reimbursement allowed only for Permanent employees")

#     if not payload.declaration_accepted:
#         errors.append("Declaration must be accepted")

#     try:
#         datetime.strptime(payload.claim_month_year, "%Y-%m")
#     except ValueError:
#         return ["claim_month_year must be in YYYY-MM format"], None, None

#     if not payload.furniture_name or not payload.furniture_name.strip():
#         errors.append("Furniture name is required")

#     if payload.furniture_bought_back:
#         errors.append("R&M reimbursement not allowed once furniture is bought back")

#     # --------------------------------------------------
#     # ONE CLAIM PER USER PER MONTH (ANY STATUS EXCEPT REJECTED)
#     # --------------------------------------------------
#     existing_claim = (
#         db.query(FurnitureRMReimbursement)
#         .filter(
#             FurnitureRMReimbursement.created_by == payload.user_id,
#             FurnitureRMReimbursement.claim_month_year == payload.claim_month_year,
#             func.lower(FurnitureRMReimbursement.status).notlike('%rejected%')
#         )
#         .first()
#     )

#     if existing_claim:
#         errors.append(
#             f"Furniture R&M claim already exists for {payload.claim_month_year} "
#             f"with status '{existing_claim.status}'"
#         )

#     # --------------------------------------------------
#     # COST VALIDATIONS
#     # --------------------------------------------------
#     if payload.total_cost_under_policy <= 0:
#         errors.append("Total cost under policy must be greater than zero")

#     if payload.expenditure_claimed <= 0:
#         errors.append("Expenditure claimed must be greater than zero")

#     if payload.amount_claimed <= 0:
#         errors.append("Amount claimed must be greater than zero")

#     if errors:
#         return errors, None, None

#     # --------------------------------------------------
#     # MAXIMUM ELIGIBILITY (15%)
#     # --------------------------------------------------
#     maximum_eligible_amount = (
#         payload.total_cost_under_policy * PERCENTAGE_LIMIT / Decimal("100")
#     ).quantize(Decimal("0.01"))

#     year = payload.claim_month_year.split("-")[0]

#     # --------------------------------------------------
#     # R&M USED (SAME FURNITURE, SAME YEAR)
#     # --------------------------------------------------
#     rm_used = (
#         db.query(
#             func.coalesce(func.sum(FurnitureRMReimbursement.amount_claimed), 0)
#         )
#         .filter(
#             FurnitureRMReimbursement.created_by == payload.user_id,
#             func.lower(FurnitureRMReimbursement.furniture_name)
#                 == payload.furniture_name.lower(),
#             FurnitureRMReimbursement.claim_month_year.startswith(year),
#             func.lower(FurnitureRMReimbursement.status).notlike('%rejected%')
#         )
#         .scalar()
#     )

#     rm_used = Decimal(rm_used or 0)

#     # --------------------------------------------------
#     # ASSET CLAIM USED (SAME ITEM, SAME YEAR, DISBURSED)
#     # --------------------------------------------------
#     asset_used = (
#         db.query(
#             func.coalesce(func.sum(AssetClaimSubmission.amount_to_be_disbursed), 0)
#         )
#         .join(
#             AssetClaim,
#             AssetClaim.asset_claim_id == AssetClaimSubmission.asset_claim_id
#         )
#         .filter(
#             AssetClaim.created_by == payload.user_id,
#             func.lower(AssetClaim.category) == "furniture",
#             func.lower(AssetClaimSubmission.item_name)
#                 == payload.furniture_name.lower(),
#             AssetClaimSubmission.status.ilike("%disbursed%"),
#             func.to_char(AssetClaimSubmission.created_at, 'YYYY') == year
#         )
#         .scalar()
#     )

#     asset_used = Decimal(asset_used or 0)

#     # --------------------------------------------------
#     # FINAL REMAINING ELIGIBILITY (PER FURNITURE)
#     # --------------------------------------------------
#     total_used = rm_used + asset_used
#     yearly_remaining = max(
#         Decimal("0"),
#         maximum_eligible_amount - total_used
#     )

#     # --------------------------------------------------
#     # FINAL AMOUNT CHECK
#     # --------------------------------------------------
#     if payload.amount_claimed > yearly_remaining:
#         errors.append(
#             f"Amount claimed ₹{payload.amount_claimed} exceeds remaining eligible amount ₹{yearly_remaining} "
#             f"for furniture '{payload.furniture_name}'"
#         )

#     if errors:
#         return errors, maximum_eligible_amount, yearly_remaining

#     # --------------------------------------------------
#     # SUCCESS
#     # --------------------------------------------------
#     return None, maximum_eligible_amount, yearly_remaining

from datetime import datetime, date

def get_financial_year_range(claim_month_year: str):
    year, month = map(int, claim_month_year.split("-"))

    if month >= 4:
        return date(year, 4, 1), date(year + 1, 3, 31)
    else:
        return date(year - 1, 4, 1), date(year, 3, 31)
def validate_furniture_rm(payload, db: Session):

    # Validate format only (needed or FY calc will crash)
    try:
        datetime.strptime(payload.claim_month_year, "%Y-%m")
    except ValueError:
        return ["claim_month_year must be in YYYY-MM format"]

    fy_start, fy_end = get_financial_year_range(payload.claim_month_year)

    from sqlalchemy import func

    existing_claim = (
        db.query(FurnitureRMReimbursement.furniture_rm_reimbursement_id)
        .filter(
            FurnitureRMReimbursement.created_by == payload.user_id,
            FurnitureRMReimbursement.created_at >= fy_start,
            FurnitureRMReimbursement.created_at <= fy_end,

            # ✅ Ignore rejected claims
            ~func.lower(FurnitureRMReimbursement.status).like('%rejected%')
        )
        .first()
    )


    if existing_claim:
        return [
            f"Furniture R&M already claimed for this financial year "
            f"({fy_start} to {fy_end}). Multiple claims are not allowed."
        ]

    return None



# --------------------------------------Furniture R&M Reimbursement validation endes here -------------------------------------------------------#

from datetime import timedelta
from decimal import Decimal

LAPTOP_ANNUAL_LIMIT = Decimal("5000")

def validate_laptop_maintenance(payload,db):
    errors = []

    # -------------------------
    # Master validations
    # -------------------------
    if payload.employee_employment_type != "Permanent":
        errors.append("Laptop maintenance reimbursement allowed only for Permanent employees")

    if not payload.declaration_accepted:
        errors.append("Declaration must be accepted")

    # -------------------------
    # Date validations
    # -------------------------
    if not payload.date_of_purchase:
        errors.append("Date of purchase is required")

    if not payload.date_of_claim:
        errors.append("Date of claim is required")

    if payload.date_of_purchase and payload.date_of_claim:
        one_year_later = payload.date_of_purchase + timedelta(days=365)
        if payload.date_of_claim < one_year_later:
            errors.append(
                "Laptop maintenance is eligible only after 1 year from date of purchase"
            )

    if payload.date_of_previous_claim:
        if payload.date_of_claim <= payload.date_of_previous_claim:
            errors.append(
                "Date of claim must be after the previous maintenance claim date"
            )

    # -------------------------
    # Amount validations
    # -------------------------
    if payload.amount_claimed <= 0:
        errors.append("Amount claimed must be greater than zero")

    if payload.amount_claimed > LAPTOP_ANNUAL_LIMIT:
        errors.append(
            f"Amount claimed ₹{payload.amount_claimed} exceeds annual limit ₹{LAPTOP_ANNUAL_LIMIT}"
        )

    if errors:
        return errors, None, None

    # -------------------------
    # Eligible amount calculation
    # -------------------------
    eligible_amount = min(payload.amount_claimed, LAPTOP_ANNUAL_LIMIT)
    return None, LAPTOP_ANNUAL_LIMIT, eligible_amount




# --------------------------------------Laptop Maintenance validation endes here -------------------------------------------------------#


from datetime import datetime
from decimal import Decimal

ANNUAL_LIMIT = Decimal("6000")
MONTHLY_LIMIT = Decimal("500")


# def validate_data_card(payload):
#     errors = []

#     # -------------------------
#     # Master validations
#     # -------------------------
#     if not payload.declaration_accepted:
#         errors.append("Declaration must be accepted")

#     if payload.employee_employment_type != "Permanent":
#         errors.append("Data Card reimbursement allowed only for Permanent employees")

#     try:
#         datetime.strptime(payload.claim_month, "%Y-%m")
#     except ValueError:
#         errors.append("claim_month must be in YYYY-MM format")

#     # -------------------------
#     # Data card details
#     # -------------------------
#     if not payload.data_card_number.strip():
#         errors.append("Data card number is required")

#     if not payload.service_provider.strip():
#         errors.append("Service provider is required")

#     if payload.connection_type != "Postpaid":
#         errors.append("Only postpaid data card connections are eligible")

#     # -------------------------
#     # Bill validations
#     # -------------------------
#     if payload.bill_amount <= 0:
#         errors.append("Bill amount must be greater than zero")

#     # Bill date must match claim month
#     if payload.bill_date.strftime("%Y-%m") != payload.claim_month:
#         errors.append(
#             f"Bill date {payload.bill_date} does not fall within claim month {payload.claim_month}"
#         )

#     # -------------------------
#     # Monthly cap enforcement
#     # -------------------------
#     if payload.bill_amount > MONTHLY_LIMIT:
#         errors.append(
#             f"Bill amount ₹{payload.bill_amount} exceeds monthly limit ₹{MONTHLY_LIMIT}"
#         )

#     if errors:
#         return errors, None, None

#     return None, payload.bill_amount, MONTHLY_LIMIT

def validate_data_card(payload, db):
    errors = []

    # -------------------------
    # Declaration & employee
    # -------------------------
    if not payload.declaration_accepted:
        errors.append("Declaration must be accepted")

    if payload.employee_employment_type != "Permanent":
        errors.append("Data Card reimbursement allowed only for Permanent employees")

    try:
        datetime.strptime(payload.claim_month, "%Y-%m")
    except ValueError:
        errors.append("claim_month must be in YYYY-MM format")

    # -------------------------
    # 🔥 NEW VALIDATION
    # Asset claim check
    # -------------------------
    asset_claim_exists = db.execute(
    text("""
        SELECT 1
        FROM asset_claim_submission acs
        JOIN asset_claim ac
          ON ac.asset_claim_id = acs.asset_claim_id
        WHERE acs.created_by = :user_id
          AND LOWER(acs.item_type) = 'data card'
          AND acs.status ILIKE '%approved%'
        LIMIT 1
    """),
    {"user_id": payload.user_id}
).fetchone()



    if not asset_claim_exists:
        errors.append(
            "You are not eligible for Data Card reimbursement as no approved Data Card asset claim exists"
        )

    # -------------------------
    # Data card details
    # -------------------------
    if not payload.data_card_number.strip():
        errors.append("Data card number is required")

    if not payload.service_provider.strip():
        errors.append("Service provider is required")

    if payload.connection_type != "Postpaid":
        errors.append("Only postpaid data card connections are eligible")

    # -------------------------
    # Bill validations
    # -------------------------
    if payload.bill_amount <= 0:
        errors.append("Bill amount must be greater than zero")

    if payload.bill_date.strftime("%Y-%m") != payload.claim_month:
        errors.append(
            f"Bill date {payload.bill_date} does not fall within claim month {payload.claim_month}"
        )

    # -------------------------
    # Monthly cap
    # -------------------------
    if payload.bill_amount > MONTHLY_LIMIT:
        errors.append(
            f"Bill amount ₹{payload.bill_amount} exceeds monthly limit ₹{MONTHLY_LIMIT}"
        )

    if errors:
        return errors, None, None

    return None, payload.bill_amount, MONTHLY_LIMIT


# --------------------------------------Data Card Charges Reimbursement validation endes here -------------------------------------------------------#

from decimal import Decimal
from datetime import date
import calendar




from app.models.claim.vehicle_cm_reimbursement import VehicleCMReimbursement

# ---------------------------------------------------
# POLICY CONFIG
# ---------------------------------------------------

from decimal import Decimal
from datetime import date
import calendar


from app.models.claim.vehicle_cm_reimbursement import VehicleCMReimbursement


# ============================================================
# ENTITLEMENT MATRIX
# ============================================================

from decimal import Decimal
from datetime import date
import calendar


from app.models.claim.vehicle_cm_reimbursement import VehicleCMReimbursement



from datetime import date
from decimal import Decimal
import calendar


from app.models.claim.vehicle_cm_reimbursement import VehicleCMReimbursement
ENTITLEMENTS = {
    "E1": {"Petrol": (500, 10800), "Other": (425, 12900)},
    "E2": {"Petrol": (700, 14400), "Other": (595, 17300)},
    "E3": {"Petrol": (800, 14400), "Other": (680, 17300)},
    "E4": {"Petrol": (900, 18000), "Other": (765, 21600)},
    "E5": {"Petrol": (960, 19200), "Other": (816, 23040)},
    "E6": {"Petrol": (1060, 19200), "Other": (901, 23040)},
    "E7": {"Petrol": (1200, 24000), "Other": (1020, 28800)},
}

FLEXIBILITY_FACTOR = Decimal("1.20")


def validate_vehicle_cm(payload, db: Session):
    errors = []

    # =========================================================
    # FETCH USER
    # =========================================================
    user = db.query(User).filter(User.user_id == payload.user_id).first()
    if not user:
        return ["Invalid user"], None, {}

    # =========================================================
    # FETCH USER VEHICLES
    # =========================================================
    vehicle_types = (
        db.query(UserVehicle.vehicle_type)
        .filter(UserVehicle.user_id == payload.user_id)
        .all()
    )

    vehicle_types = {v.vehicle_type for v in vehicle_types}

    has_two = "Two-Wheeler" in vehicle_types
    has_four = "Four-Wheeler" in vehicle_types

    user_has_both_vehicles = has_two and has_four
    user_has_two_wheeler = has_two and not has_four
    user_has_four_wheeler = has_four and not has_two
    user_has_no_vehicle = not has_two and not has_four

    # =========================================================
    # FIXED CONVEYANCE DECISION (FINAL SOURCE OF TRUTH)
    # =========================================================
    fixed_conveyance_forced = False

    if user_has_no_vehicle:
        fixed_conveyance_forced = True
    elif user_has_two_wheeler:
        fixed_conveyance_forced = True
    elif user.station_id == 2:
        fixed_conveyance_forced = True

    effective_fixed_conveyance = (
        True if fixed_conveyance_forced else payload.fixed_conveyance_claim
    )

    flags = {
        "user_has_two_wheeler": user_has_two_wheeler,
        "user_has_four_wheeler": user_has_four_wheeler,
        "user_has_both_vehicles": user_has_both_vehicles,
        "user_has_no_vehicle": user_has_no_vehicle,
        "fixed_conveyance_forced": fixed_conveyance_forced,
    }

    # =========================================================
    # BASIC ELIGIBILITY
    # =========================================================
    if payload.employee_employment_type != "Permanent":
        errors.append("Vehicle reimbursement allowed only for Permanent employees")

    if not payload.declaration_accepted:
        errors.append("Declaration must be accepted")

    if payload.employee_grade not in ENTITLEMENTS:
        errors.append("Invalid employee grade")

    if payload.fuel_type not in ("Petrol", "Other"):
        errors.append("Fuel type must be Petrol or Other")

    # =========================================================
    # CLAIM MONTH PARSING (JAN–DEC)
    # =========================================================
    try:
        year, month = map(int, payload.claim_month_year.split("-"))
        last_day = calendar.monthrange(year, month)[1]
        month_end = date(year, month, last_day)
    except Exception:
        return ["claim_month_year must be in YYYY-MM format"], None, flags

    # =========================================================
    # 🔧 UPDATED PART — SAFE DATE VALIDATION
    # =========================================================
    if not effective_fixed_conveyance:
        if not payload.rc_expiry_date:
            errors.append("RC expiry date is required")
        elif payload.rc_expiry_date < month_end:
            errors.append("RC expired for claim month")

        if not payload.insurance_expiry_date:
            errors.append("Insurance expiry date is required")
        elif payload.insurance_expiry_date < month_end:
            errors.append("Insurance expired for claim month")

    # =========================================================
    # BLOCK MULTIPLE CLAIMS SAME MONTH
    # =========================================================
    existing_claim = (
        db.query(VehicleCMReimbursement)
        .filter(
            VehicleCMReimbursement.created_by == payload.user_id,
            VehicleCMReimbursement.claim_month_year == payload.claim_month_year,
            func.lower(VehicleCMReimbursement.status) != "rejected",
        )
        .first()
    )

    if existing_claim:
        errors.append(
            f"A claim already exists for {payload.claim_month_year} "
            f"with status '{existing_claim.status}'"
        )

    # =========================================================
    # FIXED CONVEYANCE VALIDATION
    # =========================================================
    if effective_fixed_conveyance:
        if payload.fuel_claimed_liters > 0 or payload.maintenance_claim_amount > 0:
            errors.append(
                "Fuel and maintenance claims are not allowed with fixed conveyance"
            )

    # =========================================================
    # ENTITLEMENTS
    # =========================================================
    annual_fuel, annual_maintenance = ENTITLEMENTS[payload.employee_grade][payload.fuel_type]

    monthly_fuel = (Decimal(annual_fuel) / 12).quantize(Decimal("0.01"))
    monthly_maintenance = (Decimal(annual_maintenance) / 12).quantize(Decimal("0.01"))

    max_fuel_allowed = (monthly_fuel * FLEXIBILITY_FACTOR).quantize(Decimal("0.01"))
    max_maintenance_allowed = (monthly_maintenance * FLEXIBILITY_FACTOR).quantize(Decimal("0.01"))

    # =========================================================
    # FETCH ANNUAL USAGE (JAN–DEC)
    # =========================================================
    fuel_used = (
        db.query(func.sum(VehicleCMReimbursement.fuel_claimed_liters))
        .filter(
            VehicleCMReimbursement.created_by == payload.user_id,
            VehicleCMReimbursement.claim_month_year.like(f"{year}-%"),
            VehicleCMReimbursement.status.in_(
                ["Pending", "Approved", "Pending Supervisor Approval"]
            ),
        )
        .scalar()
    ) or 0

    maintenance_used = (
        db.query(func.sum(VehicleCMReimbursement.maintenance_claim_amount))
        .filter(
            VehicleCMReimbursement.created_by == payload.user_id,
            VehicleCMReimbursement.claim_month_year.like(f"{year}-%"),
            VehicleCMReimbursement.status.in_(
                ["Pending", "Approved", "Pending Supervisor Approval"]
            ),
        )
        .scalar()
    ) or 0

    fuel_used = Decimal(fuel_used)
    maintenance_used = Decimal(maintenance_used)

    annual_fuel_remaining = max(Decimal("0"), Decimal(annual_fuel) - fuel_used)
    annual_maintenance_remaining = max(
        Decimal("0"), Decimal(annual_maintenance) - maintenance_used
    )

    # =========================================================
    # PARTIAL ALLOWANCE + MONTHLY CAP
    # =========================================================
    if annual_fuel_remaining == 0 and payload.fuel_claimed_liters > 0:
        errors.append("Annual fuel entitlement exhausted")

    if annual_maintenance_remaining == 0 and payload.maintenance_claim_amount > 0:
        errors.append("Annual maintenance entitlement exhausted")

    if payload.fuel_claimed_liters > max_fuel_allowed:
        errors.append(f"Fuel exceeds monthly max {max_fuel_allowed}")

    if payload.maintenance_claim_amount > max_maintenance_allowed:
        errors.append(f"Maintenance exceeds monthly max {max_maintenance_allowed}")

    if errors:
        return errors, None, flags

    # =========================================================
    # SUCCESS RESPONSE
    # =========================================================
    result = {
        "fuel_claimed_liters": payload.fuel_claimed_liters,
        "maintenance_claim_amount": payload.maintenance_claim_amount,
        "applicable_fuel_rate": payload.applicable_fuel_rate,
        "fuel_claim_amount": payload.fuel_claimed_liters * payload.applicable_fuel_rate,
        "annual_entitlement_fuel_total": annual_fuel,
        "annual_entitlement_maintenance_total": annual_maintenance,
        "annual_fuel_used_after_claim": fuel_used + payload.fuel_claimed_liters,
        "annual_maintenance_used_after_claim": maintenance_used + payload.maintenance_claim_amount,
        "annual_fuel_remaining": max(
            Decimal("0"), annual_fuel_remaining - payload.fuel_claimed_liters
        ),
        "annual_maintenance_remaining": max(
            Decimal("0"),
            annual_maintenance_remaining - payload.maintenance_claim_amount,
        ),
        "monthly_ceiling_fuel": monthly_fuel,
        "monthly_ceiling_maintenance": monthly_maintenance,
        "max_claim_allowed_fuel": max_fuel_allowed,
        "max_claim_allowed_maintenance": max_maintenance_allowed,
    }

    return None, result, flags




# --------------------------------------Vehicle Conveyance & Maintenance validation endes here -------------------------------------------------------#

