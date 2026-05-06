# import ipaddress
# import uuid
# from datetime import datetime, timedelta, timezone
# from zoneinfo import ZoneInfo

# from fastapi import Depends, HTTPException, Header, Query
# from sqlalchemy import text

# from app.database import get_db
# from app.routers.digital_logbook.geo_fencing.approval_router import issue_location_token
# from app.utils.sql_utils import execute, fetch_one, now_utc
# # app/utils/access_service.py
# import uuid
# from datetime import timedelta
# from app.utils.sql_utils import fetch_one, execute, now_utc
# import math
# from sqlalchemy import text
# from sqlalchemy import text
# from sqlalchemy.orm import Session
# from fastapi import HTTPException, status
# from sqlalchemy import text
# import math
# from sqlalchemy import text
# from sqlalchemy.orm import Session


# def haversine(lat1, lon1, lat2, lon2):
#     R = 6371  # km
#     dlat = math.radians(lat2 - lat1)
#     dlon = math.radians(lon2 - lon1)
#     a = (
#         math.sin(dlat / 2) ** 2
#         + math.cos(math.radians(lat1))
#         * math.cos(math.radians(lat2))
#         * math.sin(dlon / 2) ** 2
#     )
#     return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

# def validate_ip_or_geo(
#     db: Session,
#     ip: str | None = None,
#     lat: float | None = None,
#     lon: float | None = None
# ) -> str | None:
#     """
#     Returns:
#         'IP'  -> IP matched
#         'GEO' -> Geo matched
#         None  -> No match
#     """

#     stations = db.execute(
#         text("""
#             SELECT
#                 ip_from,
#                 ip_to,
#                 lat,
#                 lon,
#                 radius
#             FROM access_control_station
#             WHERE is_active = TRUE
#         """)
#     ).mappings().all()

#     # ---------- IP CHECK ----------
#     if ip:
#         try:
#             ip_int = int(ipaddress.ip_address(ip))
#         except ValueError:
#             ip_int = None

#         if ip_int is not None:
#             for s in stations:
#                 if s["ip_from"] and s["ip_to"]:
#                     try:
#                         start = int(ipaddress.ip_address(s["ip_from"]))
#                         end = int(ipaddress.ip_address(s["ip_to"]))
#                     except ValueError:
#                         continue

#                     if start <= ip_int <= end:
#                         return "IP"

#     # ---------- GEO CHECK ----------
#     if lat is not None and lon is not None:
#         for s in stations:
#             if s["lat"] and s["lon"] and s["radius"]:
#                 distance = haversine(
#                     lat,
#                     lon,
#                     float(s["lat"]),
#                     float(s["lon"])
#                 )

#                 if distance <= float(s["radius"]):
#                     return "GEO"

#     return None
# import uuid
# from datetime import datetime, timedelta
# from zoneinfo import ZoneInfo
# from sqlalchemy import text

# IST = ZoneInfo("Asia/Kolkata")


# def issue_token(db, user_id, ip, lat, lon, access_type):
#     token = str(uuid.uuid4())  # acceptable (can upgrade later)
#     expiry = datetime.now(IST) + timedelta(hours=1)

#     query = text("""
#         INSERT INTO location_access_token (
#             user_id,
#             station_id,
#             token,
#             access_type,
#             ip_address,
#             latitude,
#             longitude,
#             expires_at,
#             is_active,
#             created_at
#         )
#         VALUES (
#             :user_id,
#             1,
#             :token,
#             :access_type,
#             :ip_address,
#             :latitude,
#             :longitude,
#             :expires_at,
#             TRUE,
#             NOW()
#         )
#         RETURNING token, expires_at
#     """)

#     result = db.execute(
#         query,
#         {
#             "user_id": user_id,
#             "token": token,
#             "access_type": access_type,
#             "ip_address": ip,
#             "latitude": float(lat) if lat is not None else None,
#             "longitude": float(lon) if lon is not None else None,
#             "expires_at": expiry,
#         }
#     )

#     row = result.fetchone()
#     db.commit()

#     return row.token, row.expires_at
# def validate_and_issue(db, user_id, ip, lat, lon):


#     # 1️⃣ IP FIRST
#     access = validate_ip_or_geo(db, ip=ip)
#     if access == "IP":
#         return issue_location_token(
#             db, user_id, 1, ip, lat, lon, None,"IP"
#         )

#     # 2️⃣ GEO ONLY IF IP FAILS
#     if lat is not None and lon is not None:
#         access = validate_ip_or_geo(db, lat=lat, lon=lon)
#         if access == "GEO":
#             return issue_location_token(
#                 db, user_id, 1, ip, lat, lon, None,"IP"
#             )

#     # 3️⃣ APPROVAL
#     return None

# def validate_token(
#     # authorization: str | None = Header(None),
#     token: str | None = Query(None),
#     db: Session = Depends(get_db)
# ):
#     # print("Authorization header:", authorization)
#     print("Query token:", token)

#     final_token = None

#     # # 🔹 Priority 1: Authorization header
#     # if authorization and authorization.startswith("Bearer "):
#     #     final_token = authorization.replace("Bearer ", "").strip()
#     #     print("Token from header:", final_token)

#     # 🔹 Priority 2: Query parameter fallback
#     if token:
#         final_token = token.strip()
#         # print("Token from query param:", final_token)

#     else:
#         raise HTTPException(
#             status_code=401,
#             detail="Token not provided (header or query param)"
#         )

#     # 🔹 Verify token
#     token_data = verify_token(db, final_token)

#     if not token_data:
#         raise HTTPException(
#             status_code=401,
#             detail="Invalid or expired token"
#         )

#     return token_data

# def verify_token(db, token: str):
#     if not token:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Location access token missing"
#         )

#     query = text("""
#         SELECT
#             id,
#             user_id,
#             token,
#             access_type,
#             ip_address,
#             latitude,
#             longitude,
#             expires_at
#         FROM location_access_token
#         WHERE token = :token
#           AND is_active = TRUE
#           AND expires_at > NOW()
#         LIMIT 1
#     """)

#     result = db.execute(query, {"token": token})
#     row = result.mappings().first()

#     if not row:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Invalid or expired location access token"
#         )

#     return row

import ipaddress
import math
import uuid
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

from fastapi import Depends, HTTPException, Query, status
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.database import get_db

IST = ZoneInfo("Asia/Kolkata")


# ─────────────────────────────────────────────
# HAVERSINE — distance between two coordinates
# ─────────────────────────────────────────────
def haversine(lat1, lon1, lat2, lon2) -> float:
    R = 6371000  # km
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = (
        math.sin(dlat / 2) ** 2
        + math.cos(math.radians(lat1))
        * math.cos(math.radians(lat2))
        * math.sin(dlon / 2) ** 2
    )
    return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))


# ─────────────────────────────────────────────
# VALIDATE IP OR GEO
# Returns: 'IP' | 'GEO' | None
# ─────────────────────────────────────────────
# def validate_ip_or_geo(
#     db: Session,
#     ip: str | None = None,
#     lat: float | None = None,
#     lon: float | None = None,
# ) -> str | None:
#     stations = db.execute(
#         text("""
#             SELECT ip_from, ip_to, lat, lon, radius
#             FROM access_control_station
#             WHERE is_active = TRUE
#         """)
#     ).mappings().all()

#     # ── IP CHECK ──
#     if ip:
#         try:
#             ip_int = int(ipaddress.ip_address(ip))
#         except ValueError:
#             ip_int = None

#         if ip_int is not None:
#             for s in stations:
#                 if s["ip_from"] and s["ip_to"]:
#                     try:
#                         start = int(ipaddress.ip_address(s["ip_from"]))
#                         end   = int(ipaddress.ip_address(s["ip_to"]))
#                     except ValueError:
#                         continue
#                     if start <= ip_int <= end:
#                         return "IP"

#     # ── GEO CHECK ──
#     if lat is not None and lon is not None:
#         for s in stations:
#             if s["lat"] and s["lon"] and s["radius"]:
#                 try:
#                     s_lat = float(s["lat"])
#                     s_lon = float(s["lon"])
#                     s_radius = float(s["radius"])
#                 except (ValueError, TypeError):
#                     continue  # skip stations with corrupt coordinate data
#                 distance = haversine(lat, lon, s_lat, s_lon)
#                 if distance <= s_radius:
#                     return "GEO"

#     return None


def validate_ip_or_geo(
    db: Session,
    ip: str | None = None,
    lat: float | None = None,
    lon: float | None = None,
) -> str | None:

    stations = db.execute(
        text("""
            SELECT ip_from, ip_to, lat, lon, radius
            FROM access_control_station
            WHERE is_active = TRUE
        """)
    ).mappings().all()

    # ================= IP ONLY =================
    if ip:
        try:
            ip_int = int(ipaddress.ip_address(ip))
        except ValueError:
            return None

        for s in stations:
            if s["ip_from"] and s["ip_to"]:
                try:
                    start = int(ipaddress.ip_address(s["ip_from"]))
                    end   = int(ipaddress.ip_address(s["ip_to"]))
                except ValueError:
                    continue

                if start <= ip_int <= end:
                    return "IP"

        return None   # 🔥 IMPORTANT: STOP here if IP given

    # ================= GEO ONLY =================
    if lat is not None and lon is not None:
        for s in stations:
            if s["lat"] and s["lon"] and s["radius"]:
                try:
                    s_lat = float(s["lat"])
                    s_lon = float(s["lon"])
                    s_radius = float(s["radius"])
                except (ValueError, TypeError):
                    continue

                distance = haversine(lat, lon, s_lat, s_lon)

                if distance <= s_radius + 10:
                    return "GEO"

    return None


# ─────────────────────────────────────────────
# ISSUE TOKEN  (single canonical function)
#
# access_type : "IP" | "GEO" | "APPROVAL"
# station_id  : the station the user is accessing
# approved_by : user_id of approver (only for APPROVAL type)
# ─────────────────────────────────────────────
def issue_token(
    db: Session,
    user_id: int,
    station_id: int,
    ip: str,
    lat: float | None,
    lon: float | None,
    access_type: str,           # "IP" | "GEO" | "APPROVAL"
    approved_by: int | None = None,
) -> tuple[str, datetime]:

    token  = str(uuid.uuid4())
    expiry = datetime.now(IST) + timedelta(hours=1)

    db.execute(
        text("""
            INSERT INTO location_access_token (
                user_id,
                station_id,
                token,
                access_type,
                ip_address,
                latitude,
                longitude,
                approved_by_user_id,
                expires_at,
                is_active,
                created_at
            )
            VALUES (
                :user_id,
                :station_id,
                :token,
                :access_type,
                :ip_address,
                :latitude,
                :longitude,
                :approved_by,
                :expires_at,
                TRUE,
                NOW()
            )
        """),
        {
            "user_id":     user_id,
            "station_id":  station_id,
            "token":       token,
            "access_type": access_type,
            "ip_address":  ip,
            "latitude":    float(lat) if lat is not None else None,
            "longitude":   float(lon) if lon is not None else None,
            "approved_by": approved_by,
            "expires_at":  expiry,
        }
    )
    db.commit()

    return token, expiry


# ─────────────────────────────────────────────
# VALIDATE AND ISSUE
# Used by /access/validate endpoint.
# Tries IP → GEO → returns None if neither match
# (caller raises 403 if None returned)
# ─────────────────────────────────────────────
def validate_and_issue(
    db: Session,
    user_id: int,
    station_id: int,
    ip: str,
    lat: float | None,
    lon: float | None,
) -> tuple[str, datetime] | None:

    # 1️⃣ IP first
    if validate_ip_or_geo(db, ip=ip) == "IP":
        return issue_token(db, user_id, station_id, ip, lat, lon, "IP")

    # 2️⃣ GEO fallback
    if lat is not None and lon is not None:
        if validate_ip_or_geo(db, lat=lat, lon=lon) == "GEO":
            return issue_token(db, user_id, station_id, ip, lat, lon, "GEO")

    # 3️⃣ Neither matched → caller should trigger approval flow
    return None


# ─────────────────────────────────────────────
# VERIFY TOKEN  (used as FastAPI dependency)
# ─────────────────────────────────────────────
def verify_token(db: Session, token: str) -> dict:
    row = db.execute(
        text("""
            SELECT
                id,
                user_id,
                station_id,
                token,
                access_type,
                ip_address,
                latitude,
                longitude,
                approved_by_user_id,
                expires_at
            FROM location_access_token
            WHERE token     = :token
              AND is_active  = TRUE
              AND expires_at > NOW()
            LIMIT 1
        """),
        {"token": token}
    ).mappings().first()

    if not row:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired location access token"
        )

    return dict(row)


# ─────────────────────────────────────────────
# VALIDATE TOKEN  (FastAPI Depends guard)
# Usage:  dependencies=[Depends(validate_token)]
# ─────────────────────────────────────────────
def validate_token(
    token: str | None = Query(None),
    db: Session = Depends(get_db),
) -> dict:
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token not provided"
        )

    return verify_token(db, token.strip())

