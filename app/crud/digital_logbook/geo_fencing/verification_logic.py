from sqlalchemy import text
from fastapi import HTTPException

from app.routers.digital_logbook.geo_fencing.approval_router import issue_location_token
from app.utils.access_service import validate_ip_or_geo

from sqlalchemy import text
from sqlalchemy.orm import Session

from app.routers.digital_logbook.geo_fencing.approval_router import issue_location_token
from app.utils.access_service import validate_ip_or_geo


# ---------------- VERIFY HEADER TOKEN ----------------
def verify_location_token(db: Session, token: str):
    return db.execute(
        text("""
            SELECT token, expires_at
            FROM location_access_token
            WHERE token = :token
              AND is_active = TRUE
              AND expires_at > NOW()
            LIMIT 1
        """),
        {"token": token}
    ).mappings().first()


# ---------------- ACTIVE TOKEN FOR USER ----------------
# def get_active_token_for_user(db: Session, user_id: int):
#     return db.execute(
#         text("""
#             SELECT token, expires_at
#             FROM location_access_token
#             WHERE user_id = :user_id
#               AND is_active = TRUE
#               AND expires_at > NOW()
#             ORDER BY created_at DESC
#             LIMIT 1
#         """),
#         {"user_id": user_id}
#     ).mappings().first()


def get_active_token_for_user(db: Session, user_id: int):
    return db.execute(
        text("""
            SELECT token, expires_at
            FROM location_access_token
            WHERE user_id = :user_id
              AND is_active = TRUE
              AND expires_at > NOW()
            ORDER BY created_at DESC
            LIMIT 1
        """),
        {"user_id": user_id}
    ).mappings().first()


# ---------------- IP OR GEO VALIDATION ----------------
# 🔥 TEMP FLAG (set False later for production)
# 🔥 TEMP FLAG
BYPASS_ACCESS = True


def validate_ip_geo_and_issue_token(
    db: Session,
    user_id: int,
    ip: str,
    lat: float,
    lon: float
):
    # ===============================
    # 🔥 1️⃣ BYPASS MODE (TEMP FIX)
    # ===============================
    if BYPASS_ACCESS:
        import uuid
        from datetime import datetime, timedelta
        from zoneinfo import ZoneInfo
        from sqlalchemy import text

        IST = ZoneInfo("Asia/Kolkata")
        token = str(uuid.uuid4())
        expiry = datetime.now(IST) + timedelta(hours=1)

        db.execute(
            text("""
                INSERT INTO location_access_token (
                    user_id, station_id, token, access_type,
                    ip_address, latitude, longitude,
                    approved_by_user_id, expires_at, is_active, created_at
                )
                VALUES (
                    :user_id, :station_id, :token, :access_type,
                    :ip, :lat, :lon,
                    NULL, :expiry, TRUE, NOW()
                )
            """),
            {
                "user_id": user_id,
                "station_id": 1,
                "token": token,
                "access_type": "IP",
                "ip": ip,
                "lat": lat,
                "lon": lon,
                "expiry": expiry,
            }
        )
        db.commit()

        return {"token": token, "expires_at": expiry}  # ✅ clean return

    # ===============================
    # 🔒 2️⃣ ORIGINAL LOGIC (UNCHANGED)
    # ===============================
    ip_access = validate_ip_or_geo(db, ip=ip, lat=None, lon=None)
    if ip_access == "IP":
        return issue_location_token(
            db=db,
            user_id=user_id,
            station_id=1,
            ip=ip,
            lat=None,
            lon=None,
            approver_user_id=None,
            access_type='IP'
        )

    geo_access = validate_ip_or_geo(db, ip=None, lat=lat, lon=lon)
    if geo_access == "GEO":
        return issue_location_token(
            db=db,
            user_id=user_id,
            station_id=1,
            ip=ip,
            lat=lat,
            lon=lon,
            approver_user_id=None,
            access_type="GEO"
        )

    # FAILED → APPROVAL
    return None

# app/utils/shift_query_service.py
from sqlalchemy import text

# app/utils/shift_service.py
from sqlalchemy import text



def get_all_current_shift_incharges(conn):
    # print("DEBUG: Entered get_all_current_shift_incharges")

    # Step 1: Check raw table data
    raw = conn.execute(
        text("SELECT * FROM station_shift_incharge")
    ).mappings().all()

    # print("DEBUG: station_shift_incharge RAW DATA:")
    for r in raw:
        print(dict(r))

    # Step 2: Check only active rows
    active = conn.execute(
        text("""
            SELECT *
            FROM station_shift_incharge
            WHERE responsibility_to IS NULL
        """)
    ).mappings().all()

    # print("DEBUG: ACTIVE INCHARGE ROWS:")
    for a in active:
        print(dict(a))

    # Step 3: Final joined query
    query = text("""
        SELECT DISTINCT ON (ssi.station_id)
            ssi.station_id,
            st.station_name,
            st.station_code,
            ssi.shift_id,
            u.user_id,
            u.first_name,
            u.last_name,
            u.employee_code,
            u.designation,
            u.email,
            ssi.responsibility_from

        FROM station_shift_incharge ssi
        JOIN station st
            ON st.station_id = ssi.station_id
        JOIN users u
            ON u.user_id = ssi.user_id

        WHERE ssi.responsibility_to IS NULL

        ORDER BY ssi.station_id, ssi.responsibility_from DESC
    """)

    result = conn.execute(query).mappings().all()

    # print("DEBUG: FINAL QUERY RESULT:")
    for row in result:
        print(dict(row))

    return result





