from datetime import date, timedelta
from sqlalchemy import text
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.leave.hr_leave_application import HRLeaveApplication
from app.models.leave.hr_leave_application_day import HRLeaveApplicationDay
from app.models.leave.leave_balance import LeaveBalance
from app.models.leave.leave_type import LeaveType


# ========================================================================
#  NORMALIZATION
# ========================================================================
def normalize_leave_type(raw: str) -> str:
    if not raw:
        return ""
    s = raw.strip().lower()

    # Earned Leave
    if s in ("el", "el_ne", "el_e", "earned leave", "earned_leave", "earned", "earnedleave"):
        return "el_ne"

    # Casual Leave
    if s in ("cl", "casual leave", "casual_leave", "casual"):
        return "cl"

    # Half Pay Leave
    if s in ("hpl", "half pay leave", "half_pay_leave"):
        return "hpl"

    # Maternity Leave
    if s in ("ml", "mat", "maternity leave", "maternity"):
        return "ml"

    # Paternity Leave
    if s in ("pl", "pat", "paternity leave", "paternity"):
        return "pl"

    # Restricted Holidays
    if s in ("rh", "restricted holiday", "restricted holidays"):
        return "rh"

    # Public Holidays
    if s in ("ph", "public holiday", "public holidays"):
        return "ph"

    # Extraordinary Leave
    if s in ("eol", "extraordinary leave", "extra ordinary leave"):
        return "eol"
    if s in ("comp_off", "comp off", "compensatory off", "co"):
        return "comp_off"

    return s
def get_paternity_leave_used_count(db: Session, user_id: int) -> int:
    sql = """
        SELECT COUNT(*) AS cnt
        FROM hr_leave_application
        WHERE user_id = :uid
          AND lower(leave_type) IN ('pl', 'paternity leave')
          AND lower(status) IN (
              'approved',
              'pending',
              'applied',
              'submitted',
              'reversal pending',
              'reversal approved'
          );
    """
    row = db.execute(text(sql), {"uid": user_id}).fetchone()
    return int(row.cnt) if row and row.cnt is not None else 0

def get_db_leave_type_names(normalized: str) -> list[str]:
    if normalized == "cl":
        return ["casual leave"]

    if normalized == "el_ne":
        return ["earned leave"]
    
    if normalized == "comp_off":
        return ["compensatory off", "comp_off"]

    if normalized == "hpl":
        return ["half pay leave"]

    if normalized == "ml":
        return ["maternity leave"]

    if normalized == "pl":
        return ["paternity leave"]

    if normalized == "rh":
        return ["restricted holiday", "restricted holidays"]

    if normalized == "ph":
        return ["public holiday", "public holidays"]

    if normalized == "eol":
        return ["extraordinary leave"]

    return []

# ========================================================================
#  DAY COUNT
# ========================================================================
from datetime import timedelta


def count_weekends_and_holidays(
    db: Session,
    user_id: int,
    from_date: date,
    to_date: date,
    leave_type: str,
    ):
    total_days = 0
    weekly_offs = 0
    holidays = 0

    sql = """
        SELECT holiday_date
        FROM hr_public_holiday
        WHERE holiday_date BETWEEN :s AND :e
          AND lower(holiday_type) = 'public'
          AND lower(status) = 'active';
    """

    holidays_set = {
        r.holiday_date
        for r in db.execute(
            text(sql),
            {"s": from_date, "e": to_date},
        )
    }

    exclude = leave_type.lower() in ("cl", "rh")

    curr = from_date
    while curr <= to_date:
        is_off = is_weekly_off(db, user_id, curr)
        is_holiday = curr in holidays_set

        if exclude:
            if not is_off and not is_holiday:
                total_days += 1
        else:
            total_days += 1

        if is_off:
            weekly_offs += 1
        if is_holiday:
            holidays += 1

        curr += timedelta(days=1)

    return {
        "total_days": total_days,
        "weekends": weekly_offs,  # now means WEEKLY OFF
        "holidays": holidays,
    }

# ========================================================================
#  SANDWICH
# ========================================================================
def is_sandwich_type(leave_type: str) -> bool:
    return leave_type in ("el_ne", "hpl", "ml", "pl", "eol", "rh", "ph")


# ========================================================================
#  EMPLOYMENT TYPE
# ========================================================================
def get_employment_type(db: Session, user_id: int) -> str | None:
    sql = "SELECT lower(employment_type) AS et FROM users WHERE user_id = :uid"
    row = db.execute(text(sql), {"uid": user_id}).fetchone()
    return row.et if row else None


def get_total_cl_days_for_user(db: Session, user_id: int) -> float:
    sql = """
        SELECT COUNT(*)::numeric AS days
        FROM hr_leave_application_day d
        JOIN hr_leave_application h ON h.leave_id = d.leave_application_id
        WHERE h.user_id = :uid
          AND lower(h.leave_type) = 'cl'
          AND COALESCE(lower(h.status),'pending') IN ('pending','approved');
    """
    row = db.execute(text(sql), {"uid": user_id}).fetchone()
    return float(row.days) if row and row.days is not None else 0.0

def get_yearly_el_count(db: Session, user_id: int, year: int) -> int:
    sql = """
        SELECT COUNT(*) AS cnt
        FROM hr_leave_application h
        WHERE h.user_id = :uid
          AND lower(h.leave_type) IN (
              'el_ne', 'el', 'earned leave', 'earned_leave'
          )
          AND date_part('year', h.from_date) = :year
          AND lower(h.status) NOT IN (
              'withdraw approved',
              'rejected',
              'cancelled'
          );
    """
    row = db.execute(
        text(sql),
        {"uid": user_id, "year": year}
    ).fetchone()
    print(row.cnt)
    return int(row.cnt) if row and row.cnt is not None else 0

# ========================================================================
#  VALIDATORS WITHOUT DB
# ========================================================================
def validate_comp_off(data):
    # if data["days"] >1:
    #     return False, "Compensatory Off can be applied for 0.5 day or 1 day only."
    return True, None

def validate_el(data):
    if data["days"] < 3:
        return False, "EL requires minimum 3 days."
    if data["from"] < data["today"] + timedelta(days=3):
        return False, "EL must be applied 3 days in advance."
    return True, None
def validate_cl(data):
    # --------------------------------------------------
    # Rule 1: CL allowed only within same calendar year
    # --------------------------------------------------
    from_date = data["from"]
    to_date = data["to"]
    current_year = date.today().year


    if from_date.year > current_year or to_date.year > current_year:
            return False, "Casual Leave cannot be applied for the next calendar year."

    # --------------------------------------------------
    # Rule 2: Day limit
    # --------------------------------------------------
    if data["days"] < 0.5 or data["days"] > 5:
        return False, "Casual Leave is allowed from 0.5 to 5 days."

    return True, None

def validate_hpl(data):
    if data["days"] > 4 and not data["has_med_cert"]:
        return False, "HPL > 4 days requires medical certificate."
    return True, None

def validate_ml(data):
    DAYS_26_WEEKS = 182
    DAYS_12_WEEKS = 84

    days = data["days"]
    has_med_cert = data["has_med_cert"]
    child_count = data["child_count"]
    maternity_type = data.get("maternity_type", "biological")

    # --------------------------------------------------
    # Rule 1: Medical certificate mandatory
    # --------------------------------------------------
    if not has_med_cert:
        return False, "Maternity leave requires a medical certificate."

    # --------------------------------------------------
    # Rule 2: Adoption case
    # --------------------------------------------------
    if maternity_type == "adopted":
        if days > DAYS_12_WEEKS:
            return False, "Adoption maternity leave is limited to 12 weeks."
        return True, None

    # --------------------------------------------------
    # Rule 3: Biological maternity (child-based entitlement)
    # --------------------------------------------------
    max_allowed = DAYS_12_WEEKS if child_count >= 2 else DAYS_26_WEEKS

    if days > max_allowed:
        if child_count >= 2:
            return False, "Maternity leave after two children is limited to 12 weeks."
        return False, "Maternity leave is limited to 26 weeks."

    return True, None

def validate_pl( data):
    # --------------------------------------------------
    # Rule 1: Max duration
    # --------------------------------------------------
    if data["days"] > 15:
        return False, "Paternity leave maximum allowed is 15 days."

    # --------------------------------------------------
    # Rule 2: Child count restriction
    # --------------------------------------------------
    if data["child_count"] >= 2:
        return False, "Paternity leave is not allowed for employees with two or more children."

    # --------------------------------------------------
    # Rule 3: Max two PL applications in lifetime
    # --------------------------------------------------
    # used_pl = get_paternity_leave_used_count(db, user_id)
    # if used_pl >= 2:
    #     return False, "Paternity leave can be availed only twice in a lifetime."

    return True, None

VALIDATORS = {
    "el_ne": validate_el,
    "cl": validate_cl,
    "hpl": validate_hpl,
    "ml": validate_ml,
    "pl": validate_pl,
        "comp_off": validate_comp_off,

}
def get_child_count(db: Session, user_id: int) -> int:
    sql = """
        SELECT COUNT(*) AS cnt
        FROM employee_family
        WHERE user_id = :uid
          AND lower(relation) = 'child';
    """
    row = db.execute(text(sql), {"uid": user_id}).fetchone()
    return int(row.cnt) if row and row.cnt is not None else 0

def check_eol_allocation(db: Session, user_id: int):
    sql = """
        SELECT 
            lb.user_id,
            lb.allocated,
            lt.type_id,
            lt.code
        FROM leave_balances lb
        JOIN leave_types lt ON lt.type_id = lb.type_id
        WHERE lb.user_id = :uid
              AND lb.is_usable = TRUE;

    """

    rows = db.execute(text(sql), {"uid": user_id}).fetchall()
    print("DEBUG EOL ALLOCATION ROWS:", rows)

    sql_sum = """
        SELECT COALESCE(SUM(lb.allocated), 0) AS total
        FROM leave_balances lb
        JOIN leave_types lt ON lt.type_id = lb.type_id
        WHERE lb.user_id = :uid
        AND lower(lt.code) IN ('eol')
        AND lb.is_usable = TRUE;
    """


    row = db.execute(text(sql_sum), {"uid": user_id}).fetchone()
    print("DEBUG EOL ALLOCATED TOTAL:", row)

    if not row or row.total <= 0:
        return False, "Extraordinary Leave allocation not found."

    return True, None


def get_md_user_id(db: Session) -> int | None:
    sql = """
        SELECT rp.user_id
        FROM role_permissions rp
        WHERE rp.role_id = 10
          AND rp.submenu_id = 9
          AND rp.user_id IS NOT NULL
        LIMIT 1;
    """

    row = db.execute(text(sql)).fetchone()
    return row.user_id if row else None

def validate_eol(db: Session, user_id: int, data):
    MAX_EO_DAYS = 548  # 18 months

    # Rule 1: Max duration
    if data["days"] > MAX_EO_DAYS:
        return False, "Extraordinary Leave cannot exceed 18 months."

    # Rule 2: Can be applied only once in lifetime
    sql = """
        SELECT 1
        FROM hr_leave_application
        WHERE user_id = :uid
          AND lower(leave_type) IN ('eol', 'extraordinary leave')
          AND lower(status) IN (
              'approved',
              'pending',
              'applied',
              'submitted',
              'reversal pending',
              'reversal approved',
             'withdraw pending',
			   'withdraw rejected'
          )
        LIMIT 1;
    """
    row = db.execute(text(sql), {"uid": user_id}).fetchone()
    if row:
        return False, "Extraordinary Leave can be applied only once in a lifetime."

    return True, None



# ========================================================================
#  DB VALIDATION FOR EL
# ========================================================================
def apply_el_db_rules(
    db: Session,
    user_id: int,
    from_date,
    number_of_days: float,
    result: dict,
):
    year = from_date.year
    used_count = get_yearly_el_count(db, user_id, year)
    result["comment"] = ("")
    # Hard stop after 6 EL applications
    if used_count >= 6:
        return False, "Earned Leave can be applied only 6 times in a calendar year."

    # Warning on 4th and 5th application
    if used_count >= 3:
        result["comment"] = (
            f"Warning: This is your {used_count+1} Earned Leave application "
            "for the year. Only 6 EL applications are allowed per year."
        )
        result["special_approval_needed"] = True

    return True, result["comment"]



# ========================================================================
#  PROBATION RULES
# ========================================================================
def apply_probation_rules(db: Session, user_id: int, employment_type, leave_type, number_of_days):
    if employment_type != "probation":
        return True, None
 
    if leave_type not in ["cl", "rh"]:
        return False, "Only CL and RH leave are allowed during probation."
 
    return True, None


# ========================================================================
#  CLUBBING RULE MATRIX (PostgreSQL-style)
# ========================================================================
NORMALIZED_RULE_CODE = {
    "el_ne": "el",
    "hpl": "hpl",
    "cl": "cl",
    "ml": "mat",
    "pl": "pat",
    "rh": "rh",
    "ph": "rh",
    "comp_off": "comp_off",
}


def to_rule_code(t: str | None) -> str | None:
    if not t:
        return None
    t = t.lower().strip()
    return NORMALIZED_RULE_CODE.get(t, t)


ALLOWED_BEFORE = {
    "el":  {"hpl", "mat", "pat", "rh","el"},
    "hpl": {"el", "mat", "pat", "rh","hpl"},
    "cl":  {"mat", "pat", "rh","cl","comp_off"},
    "mat": {"hpl", "el", "pat", "rh","cl","mat"},
    "pat": {"hpl", "el", "mat", "rh","cl","pat"},
    "rh":  {"cl", "el", "hpl", "mat", "pat","rh"},
    "comp_off": {"cl","comp_off"},
}

def can_club_types(current: str, other: str | None) -> bool:
    """
    Returns True ONLY if PostgreSQL rule-matrix allows this combination.
    """

    # print("\n=== DEBUG: can_club_types ===")
    # print(f"Current Leave: {current}")
    # print(f"Other Leave: {other}")

    if other is None:
        # print("Other is None → Allowed = True")
        return True

    c = to_rule_code(current)
    o = to_rule_code(other)

    # print(f"Normalized Current (c): {c}")
    # print(f"Normalized Other (o): {o}")

    # If rule not defined, treat as allowed
    if c not in ALLOWED_BEFORE:
        # print(f"{c} NOT in rule matrix → Allowed = True")
        return True

    allowed_prev = ALLOWED_BEFORE[c]
    # print(f"Allowed previous types for {c}: {allowed_prev}")

    allowed = o in allowed_prev
    # print(f"Is '{o}' allowed before '{c}'? {allowed}")

    # print("=== END DEBUG can_club_types ===\n")

    return allowed


def get_leave_type_on_date(db: Session, user_id, dt):
    sql = """
        SELECT lower(h.leave_type) AS lt
        FROM hr_leave_application_day d
        JOIN hr_leave_application h ON h.leave_id = d.leave_application_id
        WHERE d.leave_date = :date
          AND h.user_id = :uid
          AND LOWER(h.status) IN (
              'approved',
              'pending',
              'applied',
              'submitted',
              'reversal pending',
              'reversal approved'
          )
        ORDER BY h.from_date DESC
        LIMIT 1;
    """

    row = db.execute(
        text(sql),
        {"date": dt, "uid": user_id},
    ).fetchone()

    return normalize_leave_type(row.lt) if row else None

def validate_clubbing(db: Session, user_id, leave_type, from_date, to_date):
    prev_raw = get_leave_type_on_date(db, user_id, from_date - timedelta(days=1))
    next_raw = get_leave_type_on_date(db, user_id, to_date + timedelta(days=1))

    current = normalize_leave_type(leave_type)
    prev_type = normalize_leave_type(prev_raw) if prev_raw else None
    next_type = normalize_leave_type(next_raw) if next_raw else None

    if prev_type and not can_club_types(current, prev_type):
        return False, f"Cannot club {current.upper()} with {prev_type.upper()}."

    if next_type and not can_club_types(current, next_type):
        return False, f"Cannot club {current.upper()} with {next_type.upper()}."

    return True, None


def get_allocated_leave(db, user_id, leave_code):
    allocated = (
        db.query(func.sum(LeaveBalance.allocated))  
        .join(LeaveType, LeaveType.type_id == LeaveBalance.type_id)
        .filter(
            LeaveBalance.user_id == user_id,
            func.lower(LeaveType.code) == leave_code.lower(),
            LeaveBalance.is_usable == True
        )
        .scalar()  
    )
    return float(allocated or 0)






def get_remaining_leave(db, user_id, leave_code):

    allocated = get_allocated_leave(db, user_id, leave_code)
    used = get_used_leave_days(db, user_id, leave_code)

    return allocated - used

# ========================================================================
#  BALANCE CHECK
# ========================================================================
from decimal import Decimal




def check_balance(db: Session, user_id: int, leave_type: str, required_days: float):

    if leave_type in NON_BALANCE_LEAVES:
        return True, None

    normalized = normalize_leave_type(leave_type)

    if normalized in ("el", "el_ne", "el_e"):
        remaining = get_non_encashable_el_balance(db, user_id)
    else:
        allocated = get_allocated_leave(db, user_id, normalized)
        used = get_used_leave_days(db, user_id, normalized)
        remaining = allocated - used

    if required_days > remaining:
        return False, f"Insufficient balance. Available: {remaining}, Requested: {required_days}"

    return True, None


# ========================================================================
#  APPROVER
# ========================================================================
def get_approver(db: Session, user_id):
    sql = "SELECT supervisor_id FROM users WHERE user_id = :uid"
    row = db.execute(text(sql), {"uid": user_id}).fetchone()
    return row.supervisor_id if row else None

def is_comp_off(db: Session, req):
    ok, msg = check_overlapping_leave(
        db,
        req.user_id,
        req.from_date,
        req.to_date,
        req.reversal
    )
    if not ok:
        return False, msg
    return True, None

# ========================================================================
#  CRUD DISPATCH HANDLERS
# ========================================================================
def dispatch_leave_type(db: Session, req, leave_type: str):
    mapping = {
        "el_ne": is_el,
        "cl": is_cl,
        "hpl": is_hpl,
        "ml": is_maternity,
        "pl": is_paternity,
        "rh": is_rh,
        "ph": is_rh,
        "eol": is_eol,
            "comp_off": is_comp_off,

    }
    handler = mapping.get(leave_type)
    if not handler:
        return True, None
    return handler(db, req)

def is_el(db: Session, req):
    ok, msg = check_overlapping_leave(
        db,
        req.user_id,
        req.from_date,
        req.to_date,
        req.reversal
    )
    if not ok:
        return False, msg
    return True, None


def is_cl(db: Session, req):
    ok, msg = check_overlapping_leave(
        db,
        req.user_id,
        req.from_date,
        req.to_date,
        req.reversal
    )
    if not ok:
        return False, msg
    return True, None


def is_hpl(db: Session, req):
    ok, msg = check_overlapping_leave(
        db,
        req.user_id,
        req.from_date,
        req.to_date,
        req.reversal
    )
    if not ok:
        return False, msg
    return True, None


def is_maternity(db: Session, req):
    ok, msg = check_overlapping_leave(
        db,
        req.user_id,
        req.from_date,
        req.to_date,
        req.reversal
    )
    if not ok:
        return False, msg
    return True, None


def is_paternity(db: Session, req):
    ok, msg = check_overlapping_leave(
        db,
        req.user_id,
        req.from_date,
        req.to_date,
        req.reversal
    )
    if not ok:
        return False, msg
    return True, None


def is_rh(db: Session, req):
    ok, msg = check_overlapping_leave(
        db,
        req.user_id,
        req.from_date,
        req.to_date,
        req.reversal
    )
    if not ok:
        return False, msg
    return True, None


def is_eol(db: Session, req):
    ok, msg = check_overlapping_leave(
        db,
        req.user_id,
        req.from_date,
        req.to_date,
        req.reversal
    )
    if not ok:
        return False, msg
    return True, None


# ========================================================================
# SUPPORTING CHECKS
# ========================================================================
def check_overlapping_leave(db, user_id, start, end, reversal: bool = False):
    # SKIP overlap validation for reversal requests
    if reversal:
        return True, None

    if start > end:
        start, end = end, start

    sql = """
        SELECT 1
        FROM hr_leave_application
        WHERE user_id = :uid
          AND LOWER(status) IN (
              'approved',
              'pending',
              'applied',
              'reversal pending',
              'withdraw pending',
              'submitted',
                          'withdraw pending',
			   'withdraw rejected'
          )
          AND from_date <= :e
            AND to_date >= :s

        LIMIT 1;
    """

    row = db.execute(
        text(sql),
        {"uid": user_id, "s": start, "e": end}
    ).fetchone()

    if row:
        return False, "Overlapping leave already exists for the selected period"

    return True, None

EL_COMBINED_TYPES = {"el_e", "el_ne"}

def get_balance_leave_codes(leave_type: str) -> list[str]:
    """
    Returns list of leave codes to consider for balance calculation.
    """
    if leave_type in EL_COMBINED_TYPES:
        return ["el_e", "el_ne"]
    return [leave_type]

BALANCE_BASED_LEAVES = {"el_ne", "el", "cl", "hpl", "rh"}
NON_BALANCE_LEAVES = {"pl", "ml", "comp_off"}

def get_non_encashable_el_balance(db: Session, user_id: int) -> float:
    """
    Authoritative EL balance calculation

    EL Balance =
        Allocated (EL_E + EL_NE)
      - Used (approved EL leaves)
      - Encashed (leave_encashment)
    """

    # 1️⃣ ALLOCATED (EL_E + EL_NE)
    alloc = db.execute(text("""
        SELECT COALESCE(SUM(lb.allocated), 0)
        FROM leave_balances lb
        JOIN leave_types lt ON lt.type_id = lb.type_id
        WHERE lb.user_id = :uid
          AND LOWER(lt.code) IN ('el_e', 'el_ne')
          AND lb.is_usable = TRUE
    """), {"uid": user_id}).scalar() or 0

    # 2️⃣ USED EL 
    used = db.execute(text("""
        SELECT COALESCE(SUM(h.number_of_days), 0)
        FROM hr_leave_application h
        WHERE h.user_id = :uid
        AND LOWER(h.leave_type) IN (
            'el', 'el_e', 'el_ne', 'earned leave', 'earned_leave'
        )
        AND LOWER(h.status) IN (
            'approved',
            'pending',             
            'reversal pending',  
            'reversal approved',  
            'withdraw rejected'
        )
    """), {"uid": user_id}).scalar() or 0

    # 3️⃣ ENCASHED EL
    encashed = db.execute(text("""
        SELECT COALESCE(SUM(le.encash_el), 0)
        FROM leave_encashment le
        LEFT JOIN encashment_main em
               ON em.encashment_main_id = le.encashment_main_id
        WHERE LOWER(le.status) NOT IN ('rejected', 'cancelled')
          AND (
                le.created_by = :uid
             OR em.created_by = :uid
          )
    """), {"uid": user_id}).scalar() or 0

    balance = float(alloc - used - encashed)

    print("\n=========== EL OPENING BALANCE DEBUG ===========")
    print(f"Allocated   : {alloc}")
    print(f"Used        : {used}")
    print(f"Encashed    : {encashed}")
    print(f"Remaining   : {balance}")
    print("==============================================\n")

    return max(balance, 0)



def get_allocated_balance(db: Session, user_id: int, leave_type: str) -> float:
    codes = get_balance_leave_codes(leave_type)

    sql = """
        SELECT COALESCE(SUM(lb.allocated), 0) AS total
        FROM leave_balances lb
        JOIN leave_types lt ON lt.type_id = lb.type_id
        WHERE lb.user_id = :uid
        AND lower(lt.code) = ANY(:codes)
        AND lb.is_usable = TRUE;
    """

    row = db.execute(
        text(sql),
        {
            "uid": user_id,
            "codes": codes,
        },
    ).fetchone()

    return float(row.total or 0)



def approve_reversal(
    db: Session,
    leave_id: int,
    reversal_from,
    reversal_to
):
    # Step 1: Fetch leave_type BEFORE deleting
    leave_row = db.execute(text("""
        SELECT LOWER(leave_type) AS leave_type
        FROM hr_leave_application
        WHERE leave_id = :leave_id
    """), {"leave_id": leave_id}).fetchone()

    is_hpl = leave_row and normalize_leave_type(leave_row.leave_type) == "hpl"

    # Step 2: Delete the reversed day rows
    db.execute(text("""
        DELETE FROM hr_leave_application_day
        WHERE leave_application_id = :leave_id
          AND leave_date BETWEEN :rf AND :rt
    """), {
        "leave_id": leave_id,
        "rf": reversal_from,
        "rt": reversal_to
    })

    # Step 3: Fetch remaining rows
    remaining_rows = db.execute(text("""
        SELECT leave_date, day_type
        FROM hr_leave_application_day
        WHERE leave_application_id = :leave_id
        ORDER BY leave_date ASC
    """), {"leave_id": leave_id}).fetchall()

    if not remaining_rows:
        db.execute(text("""
            UPDATE hr_leave_application
            SET number_of_days = 0,
                from_date      = :rf,
                to_date        = :rt,
                status         = 'Reversal Approved'
            WHERE leave_id = :leave_id
        """), {
            "leave_id": leave_id,
            "rf": reversal_from,
            "rt": reversal_to
        })

        db.execute(text("""
            UPDATE hr_leave_compof_day_new
            SET is_used = FALSE,
                leave_application_id = NULL
            WHERE leave_application_id = :leave_id
        """), {"leave_id": leave_id})

    else:
        new_from = remaining_rows[0][0]
        new_to   = remaining_rows[-1][0]

        new_days = sum(
            0.5 if (row[1] or "").lower() in ("half", "half_day", "0.5")
            else 1.0
            for row in remaining_rows
        )

        # ✅ HPL: each calendar day = 2 number_of_days
        if is_hpl:
            new_days *= 2

        db.execute(text("""
            UPDATE hr_leave_application
            SET from_date      = :new_from,
                to_date        = :new_to,
                number_of_days = :days,
                status         = 'Reversal Approved'
            WHERE leave_id = :leave_id
        """), {
            "leave_id": leave_id,
            "new_from": new_from,
            "new_to":   new_to,
            "days":     new_days
        })

        reversed_day_count = int((reversal_to - reversal_from).days + 1)

        db.execute(text("""
            UPDATE hr_leave_compof_day_new
            SET is_used = FALSE,
                leave_application_id = NULL
            WHERE id IN (
                SELECT id
                FROM hr_leave_compof_day_new
                WHERE leave_application_id = :leave_id
                  AND is_used = TRUE
                ORDER BY leave_date ASC
                LIMIT :cnt
            )
        """), {
            "leave_id": leave_id,
            "cnt": reversed_day_count
        })

    db.commit()


def get_used_leave_days(db: Session, user_id: int, leave_type: str) -> float:

    normalized = normalize_leave_type(leave_type)
    db_types = get_db_leave_type_names(normalized)

    if not db_types:
        return 0.0

    sql = """
        SELECT COALESCE(SUM(h.number_of_days), 0)::float
        FROM hr_leave_application h
        WHERE h.user_id = :uid
          AND LOWER(h.leave_type) = ANY(:types)
          AND LOWER(h.status) IN (
              'approved',
              'pending',
              'applied',
              'submitted',
              'withdraw rejected'
          );
    """

    used = db.execute(
        text(sql),
        {"uid": user_id, "types": db_types}
    ).scalar()

    return float(used or 0)
def resolve_approver(db: Session, user_id: int, leave_type: str) -> int | None:
    """
    EOL  -> MD
    ALL  -> Supervisor
    """
    if leave_type == "eol":
        return get_md_user_id(db)

    return get_approver(db, user_id)



def validate_start_end_working_day(db: Session, user_id: int, from_date, to_date):

    def is_weekly_off_day(d):
        return is_weekly_off(db, user_id, d)

    def is_public_holiday(d):
        sql = """
            SELECT 1
            FROM hr_public_holiday
            WHERE holiday_date = :d
              AND lower(holiday_type) = 'public'
              AND lower(status) = 'active'
            LIMIT 1;
        """
        return db.execute(text(sql), {"d": d}).fetchone() is not None

    # FROM DATE
    if is_weekly_off_day(from_date):
        return False, "Leave cannot be applied when FROM date is a weekly off."

    if is_public_holiday(from_date):
        return False, "Leave cannot be applied when FROM date is a public holiday."

    # TO DATE
    if is_weekly_off_day(to_date):
        return False, "Leave cannot be applied when TO date is a weekly off."

    if is_public_holiday(to_date):
        return False, "Leave cannot be applied when TO date is a public holiday."

    return True, None
# ========================================================================
#  MAIN VALIDATOR
# ========================================================================
def get_active_weekly_off(
    db: Session,
    user_id: int,
    from_date: date,
    to_date: date,
):
    sql = """
        SELECT week_off_day, effective_from, effective_to
        FROM employee_weekly_off
        WHERE user_id = :uid
          AND is_active = TRUE
          AND effective_from <= :to_date
          AND (effective_to IS NULL OR effective_to >= :from_date)
        ORDER BY effective_from DESC
        LIMIT 1;
    """

    row = db.execute(
        text(sql),
        {
            "uid": user_id,
            "from_date": from_date,
            "to_date": to_date,
        },
    ).fetchone()

    if not row:
        return None, (
            "No active weekly off found. "
            "Please update weekly off for the selected time frame."
        )

    # "4" or "4,5" → [4] or [4,5]
    week_off_days = [int(x.strip()) for x in row.week_off_day.split(",")]

    return week_off_days, None

def is_weekly_off(
    db: Session,
    user_id: int,
    check_date: date,
) -> bool:
    sql = """
        SELECT week_off_day
        FROM employee_weekly_off
        WHERE user_id = :uid
          AND is_active = TRUE
          AND effective_from <= :d
          AND (effective_to IS NULL OR effective_to >= :d)
        ORDER BY effective_from DESC
        LIMIT 1;
    """

    row = db.execute(
        text(sql),
        {"uid": user_id, "d": check_date},
    ).fetchone()

    if not row:
        # No config = no weekly off (or raise if business wants)
        return False

    # week_off_day stored as "6" or "6,7"
    week_off_days = [int(x.strip()) for x in row.week_off_day.split(",")]

    return check_date.isoweekday() in week_off_days






def validate_leave_python(db: Session, req):
    leave_type = normalize_leave_type(req.leave_type)

    if req.reversal:
        approver_id = resolve_approver(db, req.user_id, leave_type)

        return {
            "can_apply": True,
            "number_of_days": req.selected_days,
            "weekends": 0,
            "holidays": 0,
            "sandwich_days": 0,
            "approver_id": approver_id,
            "comment": "Reversal request validated.",
            "special_approval_needed": False,
        }

    # --------------------------------------------------
    # Dispatch overlap / base rules
    # --------------------------------------------------
    ok, msg = dispatch_leave_type(db, req, leave_type)
    if not ok:
        return error(msg)
    week_off_days, err = get_active_weekly_off(
    db,
    req.user_id,
    req.from_date,
    req.to_date,
)

    if err:
        return error(
            "No active weekly off found. Please update weekly off for the selected time frame.",
            {
                "number_of_days": 0,
                "sandwich_days": 0,
                "holidays": 0,
                "weekends": 0,
                "special_approval_needed": False,
            },
        )
    # --------------------------------------------------
    # Day calculation
    # --------------------------------------------------
    day_info = count_weekends_and_holidays(
        db,
        req.user_id,
        req.from_date,
        req.to_date,
        leave_type,
    )


    number_of_days = day_info["total_days"] - (req.half_day_count * 0.5)

    # HPL counts as 2 days per leave day applied
    if leave_type == "hpl":
        number_of_days *= 2

    sandwich = calculate_sandwich_days(
        db,
        req.user_id,
        leave_type,
        req.from_date,
        req.to_date,
    )

    number_of_days += sandwich["total_sandwich_days"]
    # --------------------------------------------------
    # COMP OFF: Selected days must match calculated days
    # --------------------------------------------------
    if leave_type == "comp_off":
        if float(number_of_days) > float(req.selected_days):
            return {
                "can_apply": False,
                "number_of_days": number_of_days,
                "weekends": day_info["weekends"],
                "holidays": day_info["holidays"],
                "sandwich_days": sandwich["total_sandwich_days"],
                "approver_id": None,
                "special_approval_needed": False,
                "comment": (
                    "The number of holiday days does not add up to "
                    "the compensatory days."
                ),
            }


    # --------------------------------------------------
    # Base result object
    # --------------------------------------------------
    result = {
        "can_apply": False,
        "number_of_days": number_of_days,
        "weekends": day_info["weekends"],
        "holidays": day_info["holidays"],
        "sandwich_days": sandwich["total_sandwich_days"],
        "approver_id": None,
        "comment": None,
        "special_approval_needed": False,
    }

    # --------------------------------------------------
    # Employment / probation rules
    # --------------------------------------------------
    employment_type = get_employment_type(db, req.user_id)

    ok, msg = apply_probation_rules(
        db,
        req.user_id,
        employment_type,
        leave_type,
        number_of_days,
    )
    if not ok:
        return error(msg, result)

    # --------------------------------------------------
    # Rule data (shared)
    # --------------------------------------------------
    child_count = get_child_count(db, req.user_id)


    rule_data = {
    "days": number_of_days,
    "from": req.from_date,
    "to": req.to_date,
    "today": date.today(),
    "child_count": child_count,
    "has_med_cert": req.has_med_cert,
    "maternity_type": (req.maternity_type or "biological").lower(),
}
# --------------------------------------------------
# Start / End date working-day validation
# --------------------------------------------------
    ok, msg = validate_start_end_working_day(
        db,
        req.user_id,
        req.from_date,
        req.to_date,
    )

    if not ok:
        return error(msg, result)


    # --------------------------------------------------
    # STANDARD VALIDATORS (NON-EOL)
    # --------------------------------------------------
    if leave_type in VALIDATORS:
        ok, msg = VALIDATORS[leave_type](rule_data)
        if not ok:
            return error(msg, result)

    # --------------------------------------------------
    # EXTRAORDINARY LEAVE (EOL) — ALL RULES
    # --------------------------------------------------
    if leave_type == "eol":
            ok, msg = check_eol_allocation(db, req.user_id)
            if not ok:
                return error(msg, result)

            ok, msg = validate_eol(
                db,
                req.user_id,
                {"days": number_of_days},
            )
            if not ok:
                return error(msg, result)

            result["special_approval_needed"] = True


    # --------------------------------------------------
    # EL DB-level rules
    # --------------------------------------------------
    if leave_type == "el_ne":
        ok, msg = apply_el_db_rules(
            db,
            req.user_id,
            req.from_date,
            number_of_days,
            result,
        )
        if not ok:
            return error(msg, result)

    # --------------------------------------------------
    # Clubbing validation
    # --------------------------------------------------
    ok, msg = validate_clubbing(
        db,
        req.user_id,
        leave_type,
        req.from_date,
        req.to_date,
    )
    if not ok:
        return error(msg, result)

    # --------------------------------------------------
    # Restricted Holiday validation
    # --------------------------------------------------
    if leave_type == "rh":
        ok, msg = validate_restricted_holiday(
            db,
            req.user_id,
            req.from_date,
            req.to_date,
        )
        if not ok:
            return error(msg, result)

    # --------------------------------------------------
    # Balance check (EXCLUDES EOL)
    # --------------------------------------------------
    if leave_type != "eol" and leave_type not in NON_BALANCE_LEAVES:
        ok, msg = check_balance(
            db,
            req.user_id,
            leave_type,
            number_of_days,
        )
        if not ok:
            return error(msg, result)
 # --------------------------------------------------
    # FINAL APPROVER RESOLUTION (FIXED)
    # --------------------------------------------------
    approver_id = resolve_approver(db, req.user_id, leave_type)

    if not approver_id:
        if leave_type == "eol":
            return error("MD approver not configured.", result)
        return error("Supervisor not configured.", result)

    result["approver_id"] = approver_id


    # --------------------------------------------------
    # Success
    # --------------------------------------------------
    result["can_apply"] = True
    return result



def validate_restricted_holiday(db: Session, user_id: int, from_date, to_date):
    # RH must be for a single day only
    if from_date != to_date:
        return False, "Restricted Holiday can be applied for a single day only."

    sql = """
        SELECT 1
        FROM hr_public_holiday
        WHERE holiday_date = :d
          AND lower(holiday_type) = 'restricted'
          AND lower(status) = 'active'
        LIMIT 1;
    """

    row = db.execute(
        text(sql),
        {"d": from_date},
    ).fetchone()

    if not row:
        return (
            False,
            "Restricted Holiday can only be applied on an active restricted holiday date."
        )

    return True, None
def calculate_sandwich_days(db: Session, user_id, leave_type, from_date, to_date):
    SANDWICH_DEBUG=True
    if not is_sandwich_type(leave_type):
        # if SANDWICH_DEBUG:
        #     print(f"[SANDWICH] Leave type '{leave_type}' is NOT sandwich-applicable")
        return {
            "sandwich_inside": 0,
            "sandwich_between": 0,
            "total_sandwich_days": 0,
        }

    sandwich_days = set()

    # if SANDWICH_DEBUG:
    #     print("\n================ SANDWICH DEBUG START ================")
    #     print(f"User ID        : {user_id}")
    #     print(f"Leave Type     : {leave_type}")
    #     print(f"From → To      : {from_date} → {to_date}")
    #     print("------------------------------------------------------")

    # =====================================================
    # CHECK BEFORE
    # =====================================================
    curr = from_date - timedelta(days=1)
    skipped = []

    # if SANDWICH_DEBUG:
    #     print("\n[CHECK BEFORE] Walking backward...")

    while True:
        week_off_days, err = get_active_weekly_off(db, user_id, from_date, to_date)
        print("here bro")
        print(get_active_weekly_off(db, user_id, from_date, to_date))
        if err:
            return {
                "can_apply":False,
                "sandwich_inside": 0,
                "sandwich_between": 0,
                "total_sandwich_days": 0,
                "comment": err,
            }

        is_weekend = is_weekly_off(db, user_id, curr)

        is_holiday = db.execute(
            text("""
                SELECT 1
                FROM hr_public_holiday
                WHERE holiday_date = :d
                  AND lower(holiday_type) = 'public'
                  AND lower(status) = 'active'
            """),
            {"d": curr},
        ).fetchone()

        if is_weekend or is_holiday:
            skipped.append(curr)
            if SANDWICH_DEBUG:
                reason = "WEEKEND" if is_weekend else "PUBLIC HOLIDAY"
                # print(f"  Skipped {curr} → {reason}")
            curr -= timedelta(days=1)
            continue

        prev_leave = get_leave_type_on_date(db, user_id, curr)

        # if SANDWICH_DEBUG:
        #     print(f"  Nearest working day before: {curr}")
        #     print(f"  Leave found on that day   : {prev_leave}")

        if prev_leave:
            allowed = can_club_types(leave_type, prev_leave)

            # if SANDWICH_DEBUG:
            #     print(f"  Can club {leave_type} with {prev_leave}? → {allowed}")

            if allowed:
                sandwich_days.update(skipped)
            #     if SANDWICH_DEBUG:
            #         print(f"  ✅ Sandwich applied for dates: {skipped}")
            # else:
            #     if SANDWICH_DEBUG:
            #         print("  ❌ Clubbing rule blocked sandwich")

        break

    # =====================================================
    # CHECK AFTER
    # =====================================================
    curr = to_date + timedelta(days=1)
    skipped = []

    # if SANDWICH_DEBUG:
    #     print("\n[CHECK AFTER] Walking forward...")

    while True:
        is_weekend = is_weekly_off(db, user_id, curr)

        is_holiday = db.execute(
            text("""
                SELECT 1
                FROM hr_public_holiday
                WHERE holiday_date = :d
                  AND lower(holiday_type) = 'public'
                  AND lower(status) = 'active'
            """),
            {"d": curr},
        ).fetchone()

        if is_weekend or is_holiday:
            skipped.append(curr)
            if SANDWICH_DEBUG:
                reason = "WEEKEND" if is_weekend else "PUBLIC HOLIDAY"
                # print(f"  Skipped {curr} → {reason}")
            curr += timedelta(days=1)
            continue

        next_leave = get_leave_type_on_date(db, user_id, curr)

        # if SANDWICH_DEBUG:
        #     print(f"  Nearest working day after : {curr}")
        #     print(f"  Leave found on that day   : {next_leave}")

        if next_leave:
            allowed = can_club_types(leave_type, next_leave)

            # if SANDWICH_DEBUG:
            #     print(f"  Can club {leave_type} with {next_leave}? → {allowed}")

            if allowed:
                sandwich_days.update(skipped)
            #     if SANDWICH_DEBUG:
            #         print(f"  ✅ Sandwich applied for dates: {skipped}")
            # else:
            #     if SANDWICH_DEBUG:
            #         print("  ❌ Clubbing rule blocked sandwich")

        break

    total = len(sandwich_days)

    # if SANDWICH_DEBUG:
    #     print("\n---------------- RESULT ----------------")
    #     print(f"Sandwich Dates : {sorted(sandwich_days)}")
    #     print(f"Total Added    : {total}")
    #     print("================ SANDWICH DEBUG END ==================\n")

    return {
        "sandwich_inside": 0,
        "sandwich_between": total,
        "total_sandwich_days": total,
    }
# ========================================================================
#  ERROR
# ========================================================================
def error(msg: str, base_result: dict | None = None):
    if base_result is None:
        base_result = {}
    base_result.update({"can_apply": False, "comment": msg})
    return base_result
