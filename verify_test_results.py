# ==================================================
# ENCASHMENT DEBUG TRACE — run this BEFORE the cron
# Place in your project root and run:
#   python test_encash_trace.py
# ==================================================

from datetime import date
from app.database import SessionLocal
from sqlalchemy import text

db = SessionLocal()

try:
    today   = date.today()
    year    = today.year
    quarter = (today.month - 1) // 3 + 1

    print(f"Today={today}  Year={year}  Q{quarter}")
    print("=" * 60)

    # ── Leave type IDs ──────────────────────────────────────
    leave_types = {
        r.code: r.type_id
        for r in db.execute(text("SELECT type_id, code FROM leave_types"))
    }
    EL_E  = leave_types["EL_E"]
    EL_NE = leave_types["EL_NE"]
    print(f"EL_E type_id={EL_E}   EL_NE type_id={EL_NE}")
    print()

    uid = 462

    # ── User record ─────────────────────────────────────────
    print("── USER RECORD ────────────────────────────────────────")
    user = db.execute(text("""
        SELECT user_id, employment_type, date_of_joining,
               probation_from, probation_to, permanent_from
        FROM users WHERE user_id = :uid
    """), {"uid": uid}).mappings().first()

    for k, v in user.items():
        print(f"  {k:20s} = {v}")
    print()

    # ── All EL balance rows ──────────────────────────────────
    print("── ALL EL ROWS IN leave_balances ──────────────────────")
    all_el = db.execute(text("""
        SELECT balance_id, type_id, allocated, used, balance,
               leave_year,
               DATE_PART('quarter', created_date)::int AS qtr,
               created_date
        FROM leave_balances
        WHERE user_id  = :uid
          AND type_id IN (:el_e, :el_ne)
        ORDER BY created_date
    """), {"uid": uid, "el_e": EL_E, "el_ne": EL_NE}).fetchall()

    if not all_el:
        print("  ❌ NO EL ROWS FOUND — cron hasn't run yet or rows were deleted")
    for r in all_el:
        print(f"  balance_id={r[0]}  type_id={r[1]}  alloc={r[2]}  used={r[3]}  "
              f"bal={r[4]}  year={r[5]}  Q{r[6]}  created={r[7]}")
    print()

    # ── el_exists check (exactly what cron runs) ─────────────
    print(f"── EL EXISTS CHECK  (year={year}  Q{quarter}) ─────────────────")
    el_exists = db.execute(text("""
        SELECT balance_id, type_id, allocated, leave_year,
               DATE_PART('quarter', created_date)::int AS qtr
        FROM leave_balances
        WHERE user_id   = :uid
          AND type_id  IN (:el_e, :el_ne)
          AND leave_year = :yr
          AND DATE_PART('quarter', created_date) = :qr
    """), {
        "uid": uid, "el_e": EL_E, "el_ne": EL_NE,
        "yr": year, "qr": quarter,
    }).fetchall()

    if el_exists:
        print(f"  ⚠️  ROWS FOUND — cron will SKIP this user!")
        for r in el_exists:
            print(f"    balance_id={r[0]}  type_id={r[1]}  alloc={r[2]}  "
                  f"year={r[3]}  Q{r[4]}")
    else:
        print(f"  ✅ No rows — cron will PROCEED for this user")
    print()

    # ── EL balance calculation ───────────────────────────────
    print("── EL BALANCE CALCULATION ─────────────────────────────")

    alloc = db.execute(text("""
        SELECT COALESCE(SUM(allocated), 0)
        FROM leave_balances
        WHERE user_id  = :uid
          AND type_id IN (:enc, :non)
    """), {"uid": uid, "enc": EL_E, "non": EL_NE}).scalar() or 0

    used = db.execute(text("""
        SELECT COALESCE(SUM(number_of_days), 0)
        FROM hr_leave_application
        WHERE user_id    = :uid
          AND leave_type = 'EL'
          AND LOWER(status) IN ('approved', 'reversal approved', 'withdraw rejected')
    """), {"uid": uid}).scalar() or 0

    encashed = db.execute(text("""
        SELECT COALESCE(SUM(le.encash_el), 0)
        FROM leave_encashment le
        LEFT JOIN encashment_main em
               ON em.encashment_main_id = le.encashment_main_id
        WHERE LOWER(le.status) NOT LIKE '%rejected%'
          AND LOWER(le.status) NOT LIKE '%cancelled%'
          AND (le.created_by = :uid OR em.created_by = :uid)
    """), {"uid": uid}).scalar() or 0

    current = max(int(alloc - used - encashed), 0)
    enc_new, non_new = 6, 2
    projected = current + enc_new + non_new

    print(f"  Total allocated EL   = {alloc}")
    print(f"  Total used EL        = {used}")
    print(f"  Total encashed EL    = {encashed}")
    print(f"  Current balance      = {current}")
    print(f"  New credit (Q1 full) = {enc_new + non_new}")
    print(f"  Projected            = {projected}")
    print()

    if projected >= 292:
        print(f"  ✅ projected({projected}) >= 292 → process_el_allocation() SHOULD fire")
        if current >= 292:
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
            opening = min(current, 300)
            row = EL_HARDCODED_TABLE.get(opening)
            if row:
                print(f"  Table[{opening}] = {row}")
                print(f"  → Will encash: {row['encash']} days")
                print(f"  → Encashment created: {'YES' if opening > 292 else 'NO (opening==292, encash=0)'}")
            else:
                print(f"  ❌ opening={opening} not in EL_HARDCODED_TABLE!")
        else:
            print(f"  ⚠️  current({current}) < 292 → BUG 5 fallback path (no encashment)")
    else:
        print(f"  current({projected}) < 292 → normal insert path (no encashment)")
    print()

    # ── Existing encashment records ──────────────────────────
    print("── EXISTING ENCASHMENT RECORDS ────────────────────────")
    enc_main = db.execute(text("""
        SELECT encashment_main_id, encashment_ref_id, status, created_by
        FROM encashment_main
        WHERE created_by = :uid
        ORDER BY encashment_main_id DESC
        LIMIT 5
    """), {"uid": uid}).fetchall()

    if not enc_main:
        print("  No encashment_main rows found")
    for r in enc_main:
        print(f"  main_id={r[0]}  ref={r[1]}  status={r[2]}  by={r[3]}")

    enc_detail = db.execute(text("""
        SELECT le.encashment_main_id, le.encash_el, le.balance_as_on_date,
               le.status, le.created_by
        FROM leave_encashment le
        WHERE le.created_by = :uid
        ORDER BY le.encashment_main_id DESC
        LIMIT 5
    """), {"uid": uid}).fetchall()

    if not enc_detail:
        print("  No leave_encashment rows found")
    for r in enc_detail:
        print(f"  main_id={r[0]}  encash_el={r[1]}  bal_as_on={r[2]}  "
              f"status={r[3]}  by={r[4]}")
    print()

    # ── Eligibility check ────────────────────────────────────
    print("── ELIGIBILITY CHECK ──────────────────────────────────")
    doj  = user["date_of_joining"]
    perm = user["permanent_from"]
    if doj or perm:
        # Use permanent_from if available, DOJ is fallback only
        elig   = perm if perm else doj
        elig_q = ((elig.month - 1) // 3) + 1
        skip   = elig.year > year or (elig.year == year and elig_q > quarter)
        print(f"  DOJ={doj}  permanent_from={perm}")
        print(f"  elig={elig}  elig_q=Q{elig_q}")
        print(f"  Will skip? {skip}")
        if skip:
            print(f"  ❌ User will be SKIPPED — permanent_from is in future Q{elig_q} {elig.year}")
    else:
        print("  ❌ Both DOJ and permanent_from are NULL — user will be skipped")

finally:
    db.close()