from sqlalchemy.orm import Session
from sqlalchemy import text
from datetime import datetime, timedelta

from app.schemas.leave.leave_comp_off import BulkCompOffUpdate
# from app.schemas.leave.leave_comp_off import CompOffCreate, MessageResponse,CompOffResponse

# 🔵 CREATE (Supervisor assign multiple dates)
def create_comp_off(db: Session, supervisor_id: int, data):
    
    # 1️⃣ check user under supervisor
    user_check = db.execute(text("""
        SELECT user_id, first_name, last_name, employee_code, station_id
        FROM users
        WHERE user_id = :uid
        AND supervisor_id = :sid
        AND is_deleted = false
    """), {"uid": data.user_id, "sid": supervisor_id}).fetchone()

    if not user_check:
        return {"error": "User not under this supervisor"}

    employee_name = f"{user_check.first_name or ''} {user_check.last_name or ''}"
    employee_code = user_check.employee_code
    station_id = user_check.station_id

    # 2️⃣ date validation (last 30 days only)
    today = datetime.now().date()
    last_30 = today - timedelta(days=30)

    for d in data.leave_dates:
        if d < last_30 or d > today:
            return {"error": f"Date {d} not within last 30 days"}

    # 3️⃣ insert multiple dates
    inserted_ids = []

    for leave_date in data.leave_dates:
        res = db.execute(text("""
            INSERT INTO hr_leave_compof_day_new
            (employee_name, employee_code, leave_application_id,
             leave_date, station_id, type_id, user_id, supervisor_id)
            VALUES
            (:employee_name, :employee_code, :leave_application_id,
             :leave_date, :station_id, :type_id, :user_id, :supervisor_id)
            RETURNING id
        """), {
            "employee_name": employee_name,
            "employee_code": employee_code,
            "leave_application_id": data.leave_application_id,
            "leave_date": leave_date,
            "station_id": station_id,
            "type_id": data.type_id,
            "user_id": data.user_id,
            "supervisor_id": supervisor_id
        })

        inserted_ids.append(res.fetchone().id)

    db.commit()

    return {"success": True, "ids": inserted_ids}


# 🔵 GET ALL (supervisor view)

def get_all_comp_off(db, supervisor_id: int):
    res = db.execute(text("""
        SELECT 
            c.*,
            s.station_name
        FROM hr_leave_compof_day_new c
        LEFT JOIN station s ON c.station_id = s.station_id
        WHERE c.supervisor_id = :sid
        ORDER BY c.id DESC
    """), {"sid": supervisor_id}).fetchall()

    rows = [dict(r._mapping) for r in res]

    grouped = {}

    for r in rows:
        uid = r["user_id"]

        if uid not in grouped:
            grouped[uid] = {
                "user_id": uid,
                "employee_name": r["employee_name"],
                "employee_code": r["employee_code"],
                "station_name": r["station_name"],
                "supervisor_id": r["supervisor_id"],
                "comp_offs": []
            }

        grouped[uid]["comp_offs"].append({
            "id": r["id"],
            "leave_date": r["leave_date"],
            "type_id": r["type_id"],
            "leave_application_id": r["leave_application_id"],
            "created_at": r["created_at"],
            "station_id": r["station_id"]
        })

    return list(grouped.values())


def get_all_comp_off_all(db):
    res = db.execute(text("""
        SELECT 
            c.*,
            s.station_name
        FROM hr_leave_compof_day_new c
        LEFT JOIN station s ON c.station_id = s.station_id
        ORDER BY c.id DESC
    """)).fetchall()

    rows = [dict(r._mapping) for r in res]

    grouped = {}

    for r in rows:
        uid = r["user_id"]

        if uid not in grouped:
            grouped[uid] = {
                "user_id": uid,
                "employee_name": r["employee_name"],
                "employee_code": r["employee_code"],
                "station_name": r["station_name"],
                "supervisor_id": r["supervisor_id"],
                "comp_offs": []
            }

        grouped[uid]["comp_offs"].append({
            "id": r["id"],
            "leave_date": r["leave_date"],
            "type_id": r["type_id"],
            "leave_application_id": r["leave_application_id"],
            "created_at": r["created_at"],
            "station_id": r["station_id"]
        })

    return list(grouped.values())

def get_comp_off_by_id(db: Session, id: int, supervisor_id: int):
    res = db.execute(text("""
        SELECT 
            c.*,
            s.station_name
        FROM hr_leave_compof_day_new c
        LEFT JOIN station s ON c.station_id = s.station_id
        WHERE c.id = :id
        AND c.supervisor_id = :sid
    """), {"id": id, "sid": supervisor_id}).fetchone()

    if not res:
        return None

    return dict(res._mapping)


def get_comp_off_by_user(db: Session, user_id: int):

    # ------------------------------------------------------------
    # 1. Check user exists
    # ------------------------------------------------------------
    user = db.execute(text("""
        SELECT user_id, first_name, last_name, employee_code, station_id
        FROM users
        WHERE user_id = :uid
          AND is_deleted = false
    """), {"uid": user_id}).fetchone()

    if not user:
        return None

    # ------------------------------------------------------------
    # 2. Fetch ONLY unused comp-offs
    # ------------------------------------------------------------
    res = db.execute(text("""
        SELECT 
            c.*,
            s.station_name
        FROM hr_leave_compof_day_new c
        LEFT JOIN station s ON c.station_id = s.station_id
        WHERE c.user_id = :uid
 
        ORDER BY c.leave_date DESC
    """), {"uid": user_id}).fetchall()

    if not res:
        return {
            "user_id": user_id,
            "employee_name": f"{user.first_name or ''} {user.last_name or ''}",
            "employee_code": user.employee_code,
            "comp_offs": []
        }

    rows = [dict(r._mapping) for r in res]

    grouped = {
        "user_id": user_id,
        "employee_name": f"{user.first_name or ''} {user.last_name or ''}",
        "employee_code": user.employee_code,
        "station_name": rows[0]["station_name"],
        "comp_offs": []
    }

    for r in rows:
        grouped["comp_offs"].append({
            "id": r["id"],
            "leave_date": r["leave_date"],
            "type_id": r["type_id"],
            "leave_application_id": r["leave_application_id"],
            "created_at": r["created_at"],
            "station_id": r["station_id"],
            "is_used": r["is_used"]
        })

    return grouped


def validate_comp_off_leave(db: Session, req):

    if req.leave_type.upper() != "COMP_OFF":
        return {
            "success": True,
            "message": "Not comp-off leave"
        }

    # --------------------------------------------------
    # Calculate applying days
    # --------------------------------------------------
    applying_days = (req.to_date - req.from_date).days + 1

    if req.half_day_count:
        applying_days -= req.half_day_count * 0.5

    # --------------------------------------------------
    # Count available comp-off (last 30 days BEFORE from_date)
    # --------------------------------------------------
    res = db.execute(text("""
        SELECT COUNT(*) 
        FROM hr_leave_compof_day_new
        WHERE user_id = :uid
        AND is_used = false
        AND leave_date BETWEEN (:from_date - interval '30 day') AND :from_date
    """), {
        "uid": req.user_id,
        "from_date": req.from_date
    }).scalar()

    available = res or 0

    # --------------------------------------------------
    # VALIDATION
    # --------------------------------------------------
    if applying_days > available:
        return {
            "success": False,
            "message": "Insufficient comp-off balance",
            "available_comp_off": available,
            "applying_days": applying_days,
            "max_you_can_apply": available
        }

    return {
        "success": True,
        "message": "Comp-off leave can be applied",
        "available_comp_off": available,
        "applying_days": applying_days,
        "remaining_after_apply": available - applying_days
    }




def bulk_update_comp_off_usage(db: Session, payload: BulkCompOffUpdate):

    ids = [item.id for item in payload.comp_off_updates]

    try:
        # ------------------------------------------------------------
        # 1. Validate ownership
        # ------------------------------------------------------------
        records = db.execute(text("""
            SELECT id
            FROM hr_leave_compof_day_new
            WHERE user_id = :uid
              AND id = ANY(:ids)
        """), {
            "uid": payload.user_id,
            "ids": ids
        }).fetchall()

        if len(records) != len(ids):
            return False, "Some comp-offs do not belong to user"

        # ------------------------------------------------------------
        # 2. Bulk Update
        # ------------------------------------------------------------
        for item in payload.comp_off_updates:

            db.execute(text("""
                UPDATE hr_leave_compof_day_new
                SET 
                    is_used = :is_used,
                    leave_application_id = :leave_id
                WHERE id = :id
                  AND user_id = :uid
            """), {
                "id": item.id,
                "uid": payload.user_id,
                "is_used": item.is_used,
                "leave_id": payload.leave_application_id if item.is_used else None
            })

        db.commit()

        return True, "Comp-offs updated successfully"

    except Exception as e:
        db.rollback()
        return False, str(e)


def reset_comp_off_on_reversal(db: Session, leave_application_id: int, user_id: int):
    """
    Called when comp_off leave is withdrawn or reversed.
    Frees the earned comp_off days back to unused.
    """
    try:
        result = db.execute(text("""
            UPDATE hr_leave_compof_day_new
            SET 
                is_used              = FALSE,
                leave_application_id = NULL
            WHERE leave_application_id = :leave_id
              AND user_id = :uid
            RETURNING id, leave_date
        """), {
            "leave_id": leave_application_id,
            "uid": user_id
        })

        freed_rows = result.fetchall()

        print(f"[COMP_OFF RESET] leave_id={leave_application_id} "
              f"freed {len(freed_rows)} days: "
              f"{[r.leave_date for r in freed_rows]}")

        return {
            "success": True,
            "freed_count": len(freed_rows),
            "freed_dates": [r.leave_date for r in freed_rows]
        }

    except Exception as e:
        db.rollback()
        print(f"[COMP_OFF RESET ERROR] {e}")
        return {"success": False, "error": str(e)}




