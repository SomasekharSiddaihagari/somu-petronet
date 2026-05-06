from datetime import date
from decimal import Decimal
from typing import Optional, List

from sqlalchemy import text
from sqlalchemy.orm import Session

from app.schemas.leave.leave_report import (
    LeaveReportResponse, LeaveTypeSummary, UserLeaveReport
)

CONSUMING_STATUSES = (
    "approved",
    "pending",
    "withdraw pending",
    "reversal pending",
)

AVAILED_STATUSES = (
    "approved",
    "reversal pending",
)


def _in(values) -> str:
    return ", ".join(f"'{v}'" for v in values)


def get_leave_report(
    db: Session,
    from_date: date,
    to_date: date,
    user_id: Optional[int] = None,
    station: Optional[str] = None,
) -> LeaveReportResponse:

    params = {
        "from_date": from_date,
        "to_date":   to_date,
        "uid":       user_id,
    }

    uid_la  = "AND la.user_id    = :uid" if user_id else ""
    uid_lb  = "AND lb.user_id    = :uid" if user_id else ""
    uid_enc = "AND le.created_by = :uid" if user_id else ""

    # ── 0. All active leave types ─────────────────────────────────────────────
    lt_rows = db.execute(text("""
        SELECT type_id, UPPER(code) AS code, name
        FROM leave_types
        WHERE is_active = TRUE
        ORDER BY type_id
    """)).mappings().all()

    all_leave_types: list[dict] = [
        {"code": r["code"], "name": r["name"]} for r in lt_rows
    ]

    # ── 1. Allocated per user per leave-type (no leave_year filter) ───────────
    allocated_rows = db.execute(text(f"""
        SELECT
            lb.user_id,
            UPPER(lt.code)    AS code,
            SUM(lb.allocated) AS allocated
        FROM leave_balances lb
        JOIN leave_types lt ON lt.type_id = lb.type_id
        WHERE lb.is_usable   = TRUE
          AND lt.is_active   = TRUE
          {uid_lb}
        GROUP BY lb.user_id, UPPER(lt.code)
    """), params).mappings().all()

    # ── 2. Consumed: days with leave_date <= to_date ───────────────────────────
    consumed_rows = db.execute(text(f"""
        SELECT
            la.user_id,
            UPPER(lt.code) AS code,
            SUM(
                CASE WHEN lad.day_type = 'half' THEN 0.5 ELSE 1 END
                * (la.number_of_days / app_totals.total_cal_days)
            ) AS total_consumed
        FROM hr_leave_application la
        JOIN leave_types lt
            ON  LOWER(lt.name) = LOWER(la.leave_type)
            OR  LOWER(lt.code) = LOWER(la.leave_type)
        JOIN hr_leave_application_day lad
            ON  lad.leave_application_id = la.leave_id
        JOIN (
            SELECT leave_application_id,
                COUNT(*) AS total_cal_days
            FROM hr_leave_application_day
            GROUP BY leave_application_id
        ) app_totals ON app_totals.leave_application_id = la.leave_id
        WHERE LOWER(la.status) IN ({_in(CONSUMING_STATUSES)})
          AND lt.is_active  = TRUE
          AND lad.leave_date <= :to_date
          {uid_la}
        GROUP BY la.user_id, UPPER(lt.code)
    """), params).mappings().all()

    # ── 3. EL encashment ──────────────────────────────────────────────────────
    encashed_rows = db.execute(text(f"""
        SELECT
            COALESCE(em.created_by, le.created_by) AS user_id,
            SUM(le.encash_el)                       AS total_encashed
        FROM leave_encashment le
        LEFT JOIN encashment_main em
               ON em.encashment_main_id = le.encashment_main_id
        WHERE LOWER(le.status) NOT IN ('supervisor rejected', 'rejected', 'cancelled')
          AND le.encashment_date <= :to_date
          {uid_enc}
        GROUP BY COALESCE(em.created_by, le.created_by)
    """), params).mappings().all()

    # ── 4. Availed: leave_date falls inside [from_date, to_date] ─────────────
    availed_rows = db.execute(text(f"""
        SELECT
            la.user_id,
            UPPER(lt.code) AS code,
            SUM(
                CASE WHEN lad.day_type = 'half' THEN 0.5 ELSE 1 END
                * (la.number_of_days / app_totals.total_cal_days)
            ) AS days_availed
        FROM hr_leave_application la
        JOIN leave_types lt
            ON  LOWER(lt.name) = LOWER(la.leave_type)
            OR  LOWER(lt.code) = LOWER(la.leave_type)
        JOIN hr_leave_application_day lad
            ON  lad.leave_application_id = la.leave_id
        JOIN (
            SELECT leave_application_id,
                COUNT(*) AS total_cal_days
            FROM hr_leave_application_day
            GROUP BY leave_application_id
        ) app_totals ON app_totals.leave_application_id = la.leave_id
        WHERE LOWER(la.status) IN ({_in(AVAILED_STATUSES)})
          AND lt.is_active  = TRUE
          AND lad.leave_date BETWEEN :from_date AND :to_date
          {uid_la}
        GROUP BY la.user_id, UPPER(lt.code)
    """), params).mappings().all()

    # ── 5. Build lookup dicts ─────────────────────────────────────────────────
    def _zero_map() -> dict[str, Decimal]:
        return {lt["code"]: Decimal(0) for lt in all_leave_types}

    allocated_map: dict[int, dict[str, Decimal]] = {}
    consumed_map:  dict[int, dict[str, Decimal]] = {}
    encashed_map:  dict[int, Decimal]            = {}
    availed_map:   dict[int, dict[str, Decimal]] = {}

    for row in allocated_rows:
        uid, code = row["user_id"], row["code"]
        if uid not in allocated_map:
            allocated_map[uid] = _zero_map()
        if code in allocated_map[uid]:
            allocated_map[uid][code] += Decimal(str(row["allocated"] or 0))

    for row in consumed_rows:
        uid, code = row["user_id"], row["code"]
        if uid not in consumed_map:
            consumed_map[uid] = _zero_map()
        if code in consumed_map[uid]:
            consumed_map[uid][code] += Decimal(str(row["total_consumed"] or 0))

    for row in encashed_rows:
        uid = row["user_id"]
        encashed_map[uid] = encashed_map.get(uid, Decimal(0)) + Decimal(
            str(row["total_encashed"] or 0)
        )

    for row in availed_rows:
        uid, code = row["user_id"], row["code"]
        if uid not in availed_map:
            availed_map[uid] = _zero_map()
        if code in availed_map[uid]:
            availed_map[uid][code] += Decimal(str(row["days_availed"] or 0))

    # ── 6. Users + stations ───────────────────────────────────────────────────
    name_map:       dict[int, str] = {}
    emp_code_map:   dict[int, str] = {}
    station_map:    dict[int, str] = {}
    station_id_map: dict[int, int] = {}

    query = """
        SELECT
            u.user_id,
            u.employee_code,
            TRIM(CONCAT(u.first_name, ' ', u.last_name)) AS full_name,
            s.station_name,
            s.station_id
        FROM users u
        LEFT JOIN station s ON s.station_id = u.station_id
        WHERE u.is_deleted = FALSE
    """
    q_params: dict = {}
    if user_id:
        query += " AND u.user_id = :uid"
        q_params["uid"] = user_id
    if station:
        query += " AND LOWER(s.station_name) = LOWER(:station)"
        q_params["station"] = station

    user_rows = db.execute(text(query), q_params).mappings().all()

    all_uids: set[int] = set()
    for r in user_rows:
        uid = r["user_id"]
        all_uids.add(uid)
        name_map[uid]       = r["full_name"] or f"User {uid}"
        emp_code_map[uid]   = r["employee_code"] or str(uid)
        station_map[uid]    = r["station_name"] or ""
        station_id_map[uid] = r["station_id"]

    # ── 7. Build response ─────────────────────────────────────────────────────
    records: List[UserLeaveReport] = []

    for uid in sorted(all_uids):
        alloc    = allocated_map.get(uid, _zero_map())
        consumed = consumed_map.get(uid,  _zero_map())
        enc_el   = encashed_map.get(uid,  Decimal(0))
        availed  = availed_map.get(uid,   _zero_map())

        # ── EL combined logic: usage hits NE first, encashment only reduces E ─
        el_e_alloc  = alloc.get("EL_E",  Decimal(0))
        el_ne_alloc = alloc.get("EL_NE", Decimal(0))

        total_el_consumed = (
            consumed.get("EL_E",  Decimal(0)) +
            consumed.get("EL_NE", Decimal(0))
        )

        used_ne = min(total_el_consumed, el_ne_alloc)
        used_e  = max(total_el_consumed - el_ne_alloc, Decimal(0))

        el_e_available  = max(el_e_alloc  - used_e  - enc_el, Decimal(0))
        el_ne_available = max(el_ne_alloc - used_ne,           Decimal(0))

        el_available_override = {
            "EL_E":  el_e_available,
            "EL_NE": el_ne_available,
        }
        el_encashed_override = {
            "EL_E":  enc_el,
            "EL_NE": Decimal(0),
        }
        # ─────────────────────────────────────────────────────────────────────

        leave_summaries: List[LeaveTypeSummary] = []
        total_availed = Decimal(0)

        for lt in all_leave_types:
            code       = lt["code"]
            code_lower = code.lower()
            is_el_type = code_lower in ("el_e", "el_ne")

            if is_el_type:
                avail         = el_available_override[code].quantize(Decimal("0.01"))
                encashed_days = el_encashed_override[code].quantize(Decimal("0.01"))
            else:
                used  = consumed.get(code, Decimal(0))
                avail = max(
                    alloc.get(code, Decimal(0)) - used, Decimal(0)
                ).quantize(Decimal("0.01"))
                encashed_days = Decimal(0)

            days_availed = availed.get(code, Decimal(0)).quantize(Decimal("0.01"))
            total_availed += days_availed

            leave_summaries.append(LeaveTypeSummary(
                code=code,
                name=lt["name"],
                available=avail,
                availed=days_availed,
                encashed=encashed_days,
            ))

        records.append(UserLeaveReport(
            emp_id=uid,
            emp_code=emp_code_map.get(uid, str(uid)),
            emp_name=name_map.get(uid, f"User {uid}"),
            station=station_map.get(uid) or None,
            station_id=station_id_map.get(uid),
            leave_types=leave_summaries,
            total_leaves_availed=total_availed.quantize(Decimal("0.01")),
        ))

    return LeaveReportResponse(
        from_date=from_date,
        to_date=to_date,
        station=station,
        total_employees=len(records),
        leave_type_meta=all_leave_types,
        records=records,
    )