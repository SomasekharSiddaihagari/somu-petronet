from datetime import date, datetime
import math
import traceback

from sqlalchemy import text
from sqlalchemy.orm import Session


# ==================================================
# CONSTANTS
# ==================================================

CL_BY_MONTH = {
    1: 10, 2: 9,  3: 8,  4: 8,  5: 7,  6: 6,
    7: 5,  8: 4,  9: 3,  10: 3, 11: 2, 12: 1
}

HPL_BY_MONTH = {
    1: 20, 2: 18, 3: 17, 4: 15, 5: 13, 6: 12,
    7: 10, 8: 8,  9: 7,  10: 5, 11: 3, 12: 2
}

MAX_EL         = 300
STATUS_PENDING = "Pending Finance Approval"

EL_HARDCODED_TABLE = {
    292: {"enc": 6, "non": 2, "encash": 0},
    293: {"enc": 5, "non": 2, "encash": 1},
    294: {"enc": 5, "non": 1, "encash": 2},
    295: {"enc": 4, "non": 1, "encash": 3},
    296: {"enc": 3, "non": 1, "encash": 4},
    297: {"enc": 2, "non": 1, "encash": 5},
    298: {"enc": 2, "non": 0, "encash": 6},
    299: {"enc": 1, "non": 0, "encash": 7},
    300: {"enc": 0, "non": 0, "encash": 8},
}


# ==================================================
# DATE HELPERS
# ==================================================

def current_quarter(today: date) -> int:
    return (today.month - 1) // 3 + 1


def calculate_el_for_quarter(q_month_idx: int):
    eligible_months = {1: 3, 2: 2, 3: 1}[q_month_idx]
    enc = int(6 * eligible_months / 3)
    non = math.ceil(2 * eligible_months / 3) if eligible_months > 0 else 0
    return enc, non, enc + non


def effective_start_month(user, current_year):
    doj  = user.get("date_of_joining")
    perm = user.get("permanent_from")
    if not doj and not perm:
        return None, None
    # Use permanent_from if available (DOJ can be a future re-join date)
    start = perm if perm else doj
    return start.year, start.month

def _current_el_allocated(db, user_id, EL_E, EL_NE):
    return db.execute(text("""
        SELECT COALESCE(SUM(allocated), 0)
        FROM leave_balances
        WHERE user_id = :uid
          AND type_id IN (:enc, :non)
          AND is_usable = TRUE
    """), {"uid": user_id, "enc": EL_E, "non": EL_NE}).scalar() or 0



# ==================================================
# DB HELPERS
# ==================================================

def auto_confirm_employees(db):
    """Convert probation → permanent once probation_to is crossed."""
    db.execute(text("""
        UPDATE users
        SET employment_type = 'Permanent',
            permanent_from  = probation_to
        WHERE employment_type = 'Probation'
          AND probation_to IS NOT NULL
          AND probation_to <= CURRENT_DATE
    """))
    print(" auto_confirm_employees done")


def _insert_rh_balance(db, user_id, type_id, qty):
    db.execute(text("""
        INSERT INTO leave_balances
            (user_id, type_id, allocated, used, balance, is_usable, created_date)
        VALUES
            (:uid, :tid, :qty, 0, :qty, FALSE, NOW())
        ON CONFLICT ON CONSTRAINT uniq_leave_year_quarter_type
        DO NOTHING
    """), {"uid": user_id, "tid": type_id, "qty": qty})




def _insert_balance(db, user_id, type_id, qty, force=False):
    if qty <= 0 and not force:
        return
 
    try:
        db.execute(text("""
            INSERT INTO leave_balances
                (user_id, type_id, allocated, used, balance, is_usable, created_date)
            VALUES
                (:uid, :tid, :qty, 0, :qty, TRUE, NOW())
            ON CONFLICT (user_id, type_id, leave_year) 
            DO NOTHING
        """), {"uid": user_id, "tid": type_id, "qty": qty})
 
    except Exception:
        print(f"❌ ERROR inserting leave balance user={user_id} type={type_id} qty={qty}")
        print(traceback.format_exc())
        raise


def _insert_el_quarterly(db, user_id, type_id, qty):
    if qty <= 0:
        return

    try:
        db.execute(text("""
            INSERT INTO leave_balances
                (user_id, type_id, allocated, used, balance, is_usable, created_date)
            VALUES
                (:uid, :tid, :qty, 0, :qty, TRUE, NOW())
            ON CONFLICT (user_id, type_id, leave_year) 
            DO NOTHING
        """), {"uid": user_id, "tid": type_id, "qty": qty})

    except Exception:
        print(f"❌ ERROR inserting quarterly EL user={user_id} type={type_id} qty={qty}")
        print(traceback.format_exc())
        raise
    

def run_monthly_leave_cron(db):

    today   = date.today()
    year    = today.year
    quarter = current_quarter(today)

    print(f"\n{'='*60}")
    print(f"LEAVE CRON | {today} | Year={year} | Q{quarter}")
    print(f"{'='*60}\n")

    auto_confirm_employees(db)

    users = db.execute(text("""
        SELECT user_id,
               employment_type,
               date_of_joining,
               probation_from,
               probation_to,
               permanent_from
        FROM users
        WHERE employment_type IN ('Permanent', 'Probation')
          AND is_deleted = FALSE
    """)).mappings().all()

    print(f"Loaded {len(users)} users\n")

    leave_types = {
        r.code: r.type_id
        for r in db.execute(text("SELECT type_id, code FROM leave_types"))
    }

    CL    = leave_types["CL"]
    HPL   = leave_types["HPL"]
    EL_E  = leave_types["EL_E"]
    EL_NE = leave_types["EL_NE"]
    RH    = leave_types["RH"]

    print(f"Leave types → CL={CL} HPL={HPL} EL_E={EL_E} EL_NE={EL_NE} RH={RH}\n")

    # ==================================================
    # ANNUAL LEAVES (UNCHANGED)
    # ==================================================
    print("── ANNUAL LEAVES ──────────────────────────────────────")

    for u in users:
        uid = u["user_id"]

        rh_exists = db.execute(text("""
            SELECT 1 FROM leave_balances
            WHERE user_id = :uid AND type_id = :rh AND leave_year = :yr
        """), {"uid": uid, "rh": RH, "yr": year}).first()

        if not rh_exists:
            _insert_balance(db, uid, RH, 2)

        if u["employment_type"] == "Probation":
            cl_exists = db.execute(text("""
                SELECT 1 FROM leave_balances
                WHERE user_id = :uid AND type_id = :cl AND leave_year = :yr
            """), {"uid": uid, "cl": CL, "yr": year}).first()

            if cl_exists:
                continue

            elig_date = u.get("probation_from") or u.get("date_of_joining")
            if not elig_date:
                continue

            cl_qty = CL_BY_MONTH[1] if elig_date.year < year else CL_BY_MONTH[elig_date.month]
            _insert_balance(db, uid, CL, cl_qty)

        elif u["employment_type"] == "Permanent":
            start_year, start_month = effective_start_month(u, year)
            if not start_year:
                continue

            if start_year < year:
                cl_qty, hpl_qty = CL_BY_MONTH[1], HPL_BY_MONTH[1]
            elif start_year == year:
                cl_qty, hpl_qty = CL_BY_MONTH[start_month], HPL_BY_MONTH[start_month]
            else:
                continue

            if not db.execute(text("""
                SELECT 1 FROM leave_balances
                WHERE user_id=:uid AND type_id=:cl AND leave_year=:yr
            """), {"uid": uid, "cl": CL, "yr": year}).first():
                _insert_balance(db, uid, CL, cl_qty)

            if not db.execute(text("""
                SELECT 1 FROM leave_balances
                WHERE user_id=:uid AND type_id=:hpl AND leave_year=:yr
            """), {"uid": uid, "hpl": HPL, "yr": year}).first():
                _insert_balance(db, uid, HPL, hpl_qty)

    # ==================================================
    # 🔥 QUARTERLY EL (FIXED LOGIC)
    # ==================================================
    print("\n── QUARTERLY EL ───────────────────────────────────────")

    for u in users:
        if u["employment_type"] != "Permanent":
            continue

        uid = u["user_id"]

        # 🔥 ALWAYS calculate first
        allocated = _current_el_allocated(db, uid, EL_E, EL_NE)
        current   = _current_el_balance(db, uid, EL_E, EL_NE)

        print(f"  [EL STATE] user={uid} allocated={allocated} current={current}")

        # 🔥 STEP 1: ALWAYS CHECK ENCASHMENT FIRST
        if allocated >= 292:
            print(f"  [EL CHECK] user={uid} → eligible for encashment")

            process_el_allocation(
                db=db,
                user=u,
                current=current,
                allocated=allocated,
                enc=0,
                non=0,
                EL_E=EL_E,
                EL_NE=EL_NE,
            )
            continue

        # 🔥 STEP 2: CHECK IF ALREADY ALLOCATED THIS QUARTER
        el_exists = db.execute(text("""
            SELECT 1 FROM leave_balances
            WHERE user_id = :uid
              AND type_id IN (:el_e, :el_ne)
              AND leave_year = :yr
              AND DATE_PART('quarter', created_date) = :qr
        """), {
            "uid": uid,
            "el_e": EL_E,
            "el_ne": EL_NE,
            "yr": year,
            "qr": quarter,
        }).first()

        if el_exists:
            print(f"  SKIP EL | user={uid} — already allocated Q{quarter}")
            continue

        # 🔥 STEP 3: NORMAL ALLOCATION
        doj  = u.get("date_of_joining")
        perm = u.get("permanent_from")

        if not perm and not doj:
            continue

        elig = perm if perm else doj
        elig_q = ((elig.month - 1) // 3) + 1

        if elig.year > year or (elig.year == year and elig_q > quarter):
            continue

        q_month_idx = 1 if (elig.year < year or elig_q < quarter) else ((elig.month - 1) % 3) + 1

        enc, non, total_new = calculate_el_for_quarter(q_month_idx)

        projected = allocated + total_new

        print(f"  EL ALLOC | user={uid} +{total_new} → {projected}")

        if projected >= 292:
            process_el_allocation(
                db=db,
                user=u,
                current=current,
                allocated=allocated,
                enc=enc,
                non=non,
                EL_E=EL_E,
                EL_NE=EL_NE,
            )
        else:
            _insert_el_quarterly(db, uid, EL_E, enc)
            _insert_el_quarterly(db, uid, EL_NE, non)

        db.flush()

        final = _current_el_balance(db, uid, EL_E, EL_NE)
        print(f"  EL verified | user={uid} final={final}")

    # ==================================================
    # Disable old CL
    # ==================================================
    db.execute(text("""
        UPDATE leave_balances
        SET is_usable = FALSE
        WHERE type_id = :cl AND leave_year < :yr
    """), {"cl": CL, "yr": year})

    db.commit()
    print("\n✅ Monthly leave cron completed successfully.")



def deduct_el_fifo(db, user_id, qty, EL_E, EL_NE):
    """Deduct EL from existing balances using FIFO (oldest first)."""
    rows = db.execute(text("""
        SELECT balance_id, balance
        FROM leave_balances
        WHERE user_id  = :uid
          AND type_id IN (:enc, :non)
          AND balance  > 0
        ORDER BY created_date
    """), {"uid": user_id, "enc": EL_E, "non": EL_NE}).fetchall()

    remaining = qty
    for r in rows:
        if remaining <= 0:
            break
        consume = min(r[1], remaining)
        db.execute(text("""
            UPDATE leave_balances
            SET used    = used    + :q,
                balance = balance - :q
            WHERE balance_id = :bid
        """), {"q": consume, "bid": r[0]})
        remaining -= consume


# ==================================================
# EL BALANCE — AUTHORITATIVE
# ==================================================

def _current_el_balance(db, user_id, EL_E, EL_NE) -> int:
    """
    Opening EL = Total Allocated - Used (approved leaves) - Encashed

    BUG 1 FIX: was NOT IN ('%rejected%', '%cancelled%')
    NOT IN does exact string match — wildcards are ignored.
    Fixed to use NOT LIKE.
    """
    alloc = db.execute(text("""
        SELECT COALESCE(SUM(allocated), 0)
        FROM leave_balances
        WHERE user_id  = :uid
          AND type_id IN (:enc, :non)
    """), {"uid": user_id, "enc": EL_E, "non": EL_NE}).scalar() or 0

    used = db.execute(text("""
        SELECT COALESCE(SUM(number_of_days), 0)
        FROM hr_leave_application
        WHERE user_id    = :uid
          AND leave_type = 'EL'
          AND LOWER(status) IN ('approved', 'reversal approved', 'withdraw rejected')
    """), {"uid": user_id}).scalar() or 0

    # BUG 1 FIX: NOT IN with wildcards → use NOT LIKE
    encashed = db.execute(text("""
        SELECT COALESCE(SUM(le.encash_el), 0)
        FROM leave_encashment le
        LEFT JOIN encashment_main em
               ON em.encashment_main_id = le.encashment_main_id
        WHERE LOWER(le.status) NOT LIKE '%rejected%'
          AND LOWER(le.status) NOT LIKE '%cancelled%'
          AND (le.created_by = :uid OR em.created_by = :uid)
    """), {"uid": user_id}).scalar() or 0

    balance = max(int(alloc - used - encashed), 0)
    print(f"    [EL BALANCE] user={user_id} alloc={alloc} used={used} encashed={encashed} → {balance}")
    return balance


# ==================================================
# USER LOOKUP
# ==================================================

def get_user_by_id(db, user_id):
    if isinstance(user_id, dict):
        user_id = user_id.get("user_id")
    if hasattr(user_id, "_mapping"):
        user_id = user_id["user_id"]
    user_id = int(user_id)

    return db.execute(text("""
        SELECT
            u.user_id,
            CONCAT(u.first_name, ' ', u.last_name) AS employee_name,
            u.employee_code,
            u.designation,
            s.station_name AS station
        FROM users u
        LEFT JOIN station s ON s.station_id = u.station_id
        WHERE u.user_id = :uid
    """), {"uid": user_id}).mappings().first()
    
# ==================================================
# ENCASHMENT
# ==================================================

def generate_encashment_ref(db: Session) -> str:
    year   = datetime.now().year
    prefix = f"ENC/{year}/"

    last = db.execute(text("""
        SELECT encashment_ref_id
        FROM encashment_main
        WHERE encashment_ref_id LIKE :prefix
        ORDER BY encashment_main_id DESC
        LIMIT 1
    """), {"prefix": f"{prefix}%"}).scalar()

    next_no = 1
    if last:
        try:
            next_no = int(last.split("/")[-1]) + 1
        except ValueError:
            next_no = 1

    return f"{prefix}{str(next_no).zfill(6)}"


def create_encashment_main(db, user_id) -> int:
    user    = get_user_by_id(db, user_id)
    enc_ref = generate_encashment_ref(db)

    print(f"    [ENCASHMENT MAIN] user={user_id} ref={enc_ref}")

    mid = db.execute(text("""
        INSERT INTO encashment_main (
            encashment_ref_id, employee_name, employee_code,
            designation, station, claim_module, status, created_by
        ) VALUES (
            :ref, :name, :code, :desg, :station,
            'Leave Encashment', :status, :by
        )
        RETURNING encashment_main_id
    """), {
        "ref":     enc_ref,
        "name":    user["employee_name"],
        "code":    user["employee_code"],
        "desg":    user["designation"],
        "station": user["station"],
        "status":  STATUS_PENDING,
        "by":      user["user_id"],
    }).scalar()

    print(f"    [ENCASHMENT MAIN] Created id={mid}")
    return mid


def create_leave_encashment(db, mid, user_id, encash_qty, balance):
    user      = get_user_by_id(db, user_id)
    remaining = balance - encash_qty

    print(f"    [LEAVE ENCASHMENT] user={user_id} opening={balance} encash={encash_qty} remaining={remaining}")

    db.execute(text("""
        INSERT INTO leave_encashment (
            encashment_main_id, employee_name, employee_code,
            designation, station, encashment_date, leave_type,
            el_encashable, encash_el, balance_as_on_date, status, created_by,
            declaration_accepted, is_auto_encashed
        ) VALUES (
            :mid, :name, :code, :desg, :station,
            :dt, 'EL', :bal, :encash, :remain, :status, :by,
            TRUE, TRUE
        )
    """), {
        "mid":     mid,
        "name":    user["employee_name"],
        "code":    user["employee_code"],
        "desg":    user["designation"],
        "station": user["station"],
        "dt":      date.today(),
        "bal":     min(balance, MAX_EL),
        "encash":  encash_qty,
        "remain":  remaining,
        "status":  STATUS_PENDING,
        "by":      user["user_id"],
    })
def process_el_allocation(db, user, current, allocated, enc, non, EL_E, EL_NE):

    opening = min(allocated, MAX_EL)

    print(f"  [PROCESS EL] user={user['user_id']} current={current} allocated={allocated} opening={opening}")

    if opening < 292:
        headroom = MAX_EL - allocated   # ✅ FIXED
        safe_enc = min(enc, headroom)
        safe_non = min(non, max(headroom - safe_enc, 0))

        print(f"  [PROCESS EL] opening<292 fallback enc={safe_enc} non={safe_non}")

        _insert_balance(db, user["user_id"], EL_E,  safe_enc)
        _insert_balance(db, user["user_id"], EL_NE, safe_non)
        return

    row = EL_HARDCODED_TABLE[opening]

    enc_to_allocate = row["enc"]
    non_to_allocate = row["non"]
    auto_encash     = row["encash"]

    print(f"  [PROCESS EL] table[{opening}] → enc={enc_to_allocate} non={non_to_allocate} encash={auto_encash}")

    _insert_balance(db, user["user_id"], EL_E,  enc_to_allocate, force=True)
    _insert_balance(db, user["user_id"], EL_NE, non_to_allocate, force=True)

    if opening > 292:

        #  CHECK FIRST
        already_done = db.execute(text("""
            SELECT 1
            FROM leave_encashment
            WHERE created_by = :uid
            AND DATE_PART('quarter', encashment_date) = DATE_PART('quarter', CURRENT_DATE)
            AND DATE_PART('year', encashment_date) = DATE_PART('year', CURRENT_DATE)
            AND LOWER(status) NOT LIKE '%rejected%'
            AND LOWER(status) NOT LIKE '%cancelled%'
        """), {"uid": user["user_id"]}).first()

        if already_done:
            print(f"  [PROCESS EL] ⏭ Skipping encashment (already done this quarter)")
        else:
            mid = create_encashment_main(db, user["user_id"])

            create_leave_encashment(
                db=db,
                mid=mid,
                user_id=user["user_id"],
                encash_qty=auto_encash,
                balance=current,
            )

    final_allocated = allocated + enc_to_allocate + non_to_allocate

    if current > MAX_EL:
        print(f"  [PROCESS EL] final allocated = {final_allocated} (allowed to exceed)")

    print(f"  [PROCESS EL]  final allocated = {final_allocated}")



