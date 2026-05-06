import datetime
import json
import os
from typing import Optional
from fastapi import HTTPException, UploadFile
from sqlalchemy.orm import Session
from sqlalchemy import text

from app.schemas.gate_pass.GatePass import InwardGatePassUpdate, InwardMaterialDetailsRequest

from sqlalchemy.orm import Session
from sqlalchemy import text


# ================================
# 1️⃣ Get all gate passes by station/user role
# ================================
def get_all_gate_pass_by_user(db: Session, user_id: int):
    sql = text("SELECT public.get_all_gate_pass_by_station(:user_id)")
    result = db.execute(sql, {"user_id": user_id}).scalar()
    return result


def get_gatepass_by_formtype(
    db: Session,
    formtype: str,
    id: int,
    gatepass_no: Optional[str] = None
):
    sql = text("""
        SELECT public.get_gatepass_by_formtype(
            :formtype,
            :p_id,
            :p_gatepass_no
        )
    """)

    return db.execute(sql, {
        "formtype": formtype,
        "p_id": id,
        "p_gatepass_no": gatepass_no
    }).scalar()

def gv(obj, field):
    if isinstance(obj, dict):
        return obj.get(field)
    return getattr(obj, field, None)

def create_inward_gate_pass_crud(db, inward_data, file_paths):
    try:
        query = text("""
            SELECT create_inward_gate_pass_with_details(
                :p_station, :p_po_type, :p_po_number, :p_received_from,
                :p_supplier_address, :p_purpose, :p_reference_document,
                :p_vehicle_no, :p_driver_name, :p_driver_phone,
                :p_security_guard, :p_approver_name, :p_approver_id,
                :p_status, :p_created_by, :p_updated_by, :p_uploaded_by,
                :p_vehicle_photo, :p_delivery_personnel_photo,
                :p_delivery_personnel_id_photo, :p_date_time, :p_goods_photo
            ) AS result;
        """)

        params = {
    "p_station": gv(inward_data, "station"),
    "p_po_type": gv(inward_data, "po_type"),
    "p_po_number": gv(inward_data, "po_number"),
    "p_received_from": gv(inward_data, "received_from"),
    "p_supplier_address": gv(inward_data, "supplier_address"),
    "p_purpose": gv(inward_data, "purpose"),
    "p_reference_document": gv(inward_data, "reference_document"),

    "p_vehicle_no": gv(inward_data, "vehicle_no"),
    "p_driver_name": gv(inward_data, "driver_name"),
    "p_driver_phone": gv(inward_data, "driver_phone"),
    "p_security_guard": gv(inward_data, "security_guard"),

    "p_approver_name": gv(inward_data, "approver_name"),
    "p_approver_id": gv(inward_data, "approver_id"),
    "p_status": gv(inward_data, "status"),

    "p_created_by": gv(inward_data, "created_by"),
    "p_updated_by": gv(inward_data, "updated_by"),
    "p_uploaded_by": gv(inward_data, "uploaded_by"),

    "p_date_time": gv(inward_data, "date_time"),

"p_vehicle_photo": file_paths["vehicle_photo"],
"p_delivery_personnel_photo": file_paths["delivery_personnel_photo"],
"p_delivery_personnel_id_photo": file_paths["delivery_personnel_id_photo"],
"p_goods_photo": file_paths["goods_photo"],

}


        result = db.execute(query, params).scalar()
        db.commit()
        return result

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {e}")





def get_all_inward_gate_passes(db: Session, user_id: int):
    stmt = text("SELECT * FROM public.get_all_inward_gate_passes(:user_id)")
    result = db.execute(stmt, {"user_id": user_id}).fetchall()

    def resolve_user_name(value):
        if not value:
            return None
        try:
            user_row = db.execute(
                text("SELECT first_name, last_name FROM users WHERE user_id = :uid"),
                {"uid": int(value)}
            ).fetchone()
        except ValueError:
            user_row = db.execute(
                text("SELECT first_name, last_name FROM users WHERE username = :uname"),
                {"uname": value}
            ).fetchone()
        return f"{user_row[0]} {user_row[1]}".strip() if user_row else None

    rows = []
    for row in result:
        data = dict(row._mapping)
        data["created_by_name"] = resolve_user_name(data.get("created_by"))
        data["updated_by_name"] = resolve_user_name(data.get("updated_by"))
        rows.append(data)

    return rows


# def get_inward_gate_pass_by_id(db: Session, inward_id: int):
#     stmt = text("SELECT * FROM public.get_inward_gate_pass_by_id(:inward_id)")
#     result = db.execute(stmt, {"inward_id": inward_id}).fetchone()
#     return dict(result._mapping) if result else None

def get_inward_gate_pass_by_id(db: Session, inward_id: int):
    stmt = text("SELECT * FROM public.get_inward_gate_pass_by_id(:inward_id)")
    result = db.execute(stmt, {"inward_id": inward_id}).fetchone()
    
    if not result:
        return None
    
    data = dict(result._mapping)

    def resolve_user_name(value):
        if not value:
            return None
        try:
            user_row = db.execute(
                text("SELECT first_name, last_name FROM users WHERE user_id = :uid"),
                {"uid": int(value)}
            ).fetchone()
        except ValueError:
            user_row = db.execute(
                text("SELECT first_name, last_name FROM users WHERE username = :uname"),
                {"uname": value}
            ).fetchone()
        return f"{user_row[0]} {user_row[1]}".strip() if user_row else None

    # The actual content is nested under "get_inward_gate_pass_by_id" key
    inner = data.get("get_inward_gate_pass_by_id")
    if isinstance(inner, str):
        inner = json.loads(inner)
        data["get_inward_gate_pass_by_id"] = inner

    if inner and isinstance(inner, dict):
        inward_details = inner.get("inward_details")
        if isinstance(inward_details, str):
            inward_details = json.loads(inward_details)
            inner["inward_details"] = inward_details

        if inward_details and isinstance(inward_details, dict):
            inward_details["created_by_name"] = resolve_user_name(inward_details.get("created_by"))
            inward_details["updated_by_name"] = resolve_user_name(inward_details.get("updated_by"))

    return data





def update_inward_gate_pass_full(db: Session, inward_id: int, data: InwardGatePassUpdate):

    dt_value = None
    if data.date_time:
        try:
            dt_value = datetime.fromisoformat(data.date_time)
        except:
            dt_value = None

    stmt = text("""
        SELECT update_inward_gate_pass_full(
            :p_inward_id,
            :p_gate_pass_no,
            :p_date_time,
            :p_station,
            :p_po_type,
            :p_po_number,
            :p_received_from,
            :p_supplier_address,
            :p_purpose,
            :p_reference_document,
            :p_vehicle_no,
            :p_driver_name,
            :p_driver_phone,
            :p_security_guard,
            :p_approver_name,
            :p_approver_id,
            :p_status,
            :p_updated_by,
            :p_vehicle_photo,
            :p_delivery_personnel_photo,
            :p_delivery_personnel_id_photo,
            :p_goods_photo
        );
    """)

    params = {
        "p_inward_id": inward_id,
        "p_gate_pass_no": data.gate_pass_no,
        "p_date_time": data.date_time,
        "p_station": data.station,
        "p_po_type": data.po_type,
        "p_po_number": data.po_number,
        "p_received_from": data.received_from,
        "p_supplier_address": data.supplier_address,
        "p_purpose": data.purpose,
        "p_reference_document": data.reference_document,
        "p_vehicle_no": data.vehicle_no,
        "p_driver_name": data.driver_name,
        "p_driver_phone": data.driver_phone,
        "p_security_guard": data.security_guard,
        "p_approver_name": data.approver_name,
        "p_approver_id": data.approver_id,
        "p_status": data.status,
        "p_updated_by": data.updated_by,
        "p_vehicle_photo": data.vehicle_photo,
        "p_delivery_personnel_photo": data.delivery_personnel_photo,
        "p_delivery_personnel_id_photo": data.delivery_personnel_id_photo,
        "p_goods_photo": data.goods_photo
    }

    result = db.execute(stmt, params).scalar()
    db.commit()
    return result



# def get_cardData_crud(db: Session, user_id: int):
#     from sqlalchemy import text
#     from datetime import date

#     today = date.today()

#     # Get user's role and station name
#     user_query = text("""
#         SELECT u.role_id, s.station_name
#         FROM users u
#         LEFT JOIN station s ON u.station_id = s.station_id
#         WHERE u.user_id = :user_id
#     """)
#     user_result = db.execute(user_query, {"user_id": user_id}).fetchone()

#     if not user_result:
#         return {"error": "User not found"}

#     role_id = user_result.role_id
#     station_name = user_result.station_name
#     is_admin = role_id == 3  # Admin sees all stations

#     def count(query_str, params={}):
#         return db.execute(text(query_str), params).scalar() or 0

#     # ── 1. Total gate passes today ──────────────────────────────────────────
#     if is_admin:
#         total_inward_today = count(
#             "SELECT COUNT(*) FROM inward_gate_pass WHERE DATE(date_time) = :today",
#             {"today": today}
#         )
#         total_outward_today = count(
#             "SELECT COUNT(*) FROM outward_gate_pass WHERE DATE(date_time) = :today",
#             {"today": today}
#         )
#     else:
#         total_inward_today = count(
#             "SELECT COUNT(*) FROM inward_gate_pass WHERE DATE(date_time) = :today AND station = :station",
#             {"today": today, "station": station_name}
#         )
#         total_outward_today = count(
#             "SELECT COUNT(*) FROM outward_gate_pass WHERE DATE(date_time) = :today AND station = :station",
#             {"today": today, "station": station_name}
#         )
#         total_returnable_passes = count("SELECT COUNT(*) FROM returnable_gate_pass")

#     total_gate_pass_today = total_inward_today + total_outward_today + total_returnable_passes

#     # ── 2. Pending Approvals (inward + outward) ─────────────────────────────
#     if is_admin:
#         pending_inward = count(
#             "SELECT COUNT(*) FROM inward_gate_pass WHERE LOWER(status) = 'pending approval'"
#         )
#         pending_outward = count(
#             "SELECT COUNT(*) FROM outward_gate_pass WHERE LOWER(status) = 'pending approval'"
#         )
#     else:
#         pending_inward = count(
#             "SELECT COUNT(*) FROM inward_gate_pass WHERE LOWER(status) = 'pending approval' AND station = :station",
#             {"station": station_name}
#         )
#         pending_outward = count(
#             "SELECT COUNT(*) FROM outward_gate_pass WHERE LOWER(status) = 'pending approval' AND station = :station",
#             {"station": station_name}
#         )

#     pending_approvals = pending_inward + pending_outward

#     # ── 3. returnable ───────────────────────────────────────────────
#     if is_admin:
#         returnable_pending = count(
#             "SELECT COUNT(*) FROM returnable_gate_pass WHERE LOWER(status) = 'returnable'"
#         )
#     else:
#         returnable_pending = count(
#             """
#             SELECT COUNT(*) 
#             FROM returnable_gate_pass rgp
#             JOIN outward_gate_pass ogp ON rgp.outward_id = ogp.outward_id
#             WHERE LOWER(rgp.status) = 'returnable'
#             AND ogp.station = :station
#             """,
#             {"station": station_name}
#         )

#     # ── 4. Total Inward Passes (all time) ───────────────────────────────────
#     if is_admin:
#         total_inward_passes = count("SELECT COUNT(*) FROM inward_gate_pass")
#     else:
#         total_inward_passes = count(
#             "SELECT COUNT(*) FROM inward_gate_pass WHERE station = :station",
#             {"station": station_name}
#         )

#     # ── 5. Total Outward Passes (all time) ──────────────────────────────────
#     # ── 5. Total Outward Passes (all time) ──────────────────────────────────
#     if is_admin:
#         total_outward_passes = count("SELECT COUNT(*) FROM outward_gate_pass")
#     else:
#         total_outward_passes = count(
#             "SELECT COUNT(*) FROM outward_gate_pass WHERE station = :station",
#             {"station": station_name}
#         )

#     # ── 6. Total Returnable Passes (all time) ────────────────────────────────
#     if is_admin:
#         total_returnable_passes = count("SELECT COUNT(*) FROM returnable_gate_pass")
#     else:
#         total_returnable_passes = count(
#             """
#             SELECT COUNT(*)
#             FROM returnable_gate_pass rgp
#             JOIN outward_gate_pass ogp ON rgp.outward_id = ogp.outward_id
#             WHERE ogp.station = :station
#             """,
#             {"station": station_name}
#         )

#     # ── 7. Total Entries ────────────────────────────────────────────────────

#     total_entries = total_inward_passes + total_outward_passes + total_returnable_passes

#     return {
#         "total_gate_pass_today":   total_gate_pass_today,
#         "pending_approvals":       pending_approvals,
#         "returnable_pending":      returnable_pending,
#         "total_inward_passes":     total_inward_passes,
#         "total_outward_passes":    total_outward_passes,
#         "total_returnable_passes": total_returnable_passes,
#         "total_entries":           total_entries,
#     }
def get_cardData_crud(db: Session, user_id: int):
    from sqlalchemy import text
    from datetime import date

    today = date.today()

    # Get user's role and station name
    user_query = text("""
        SELECT u.role_id, s.station_name
        FROM users u
        LEFT JOIN station s ON u.station_id = s.station_id
        WHERE u.user_id = :user_id
    """)
    user_result = db.execute(user_query, {"user_id": user_id}).fetchone()

    if not user_result:
        return {"error": "User not found"}

    role_id = user_result.role_id
    station_name = user_result.station_name
    is_admin = role_id == 3  # Admin sees all stations

    def count(query_str, params={}):
        return db.execute(text(query_str), params).scalar() or 0

    # ── 1. Total gate passes today ──────────────────────────────────────────
    if is_admin:
        total_inward_today = count(
            "SELECT COUNT(*) FROM inward_gate_pass WHERE DATE(date_time) = :today",
            {"today": today}
        )
        total_outward_today = count(
            "SELECT COUNT(*) FROM outward_gate_pass WHERE DATE(date_time) = :today",
            {"today": today}
        )
        total_returnable_today = count(
            "SELECT COUNT(*) FROM returnable_gate_pass WHERE DATE(date_time) = :today",
            {"today": today}
        )
    else:
        total_inward_today = count(
            "SELECT COUNT(*) FROM inward_gate_pass WHERE DATE(date_time) = :today AND station = :station",
            {"today": today, "station": station_name}
        )
        total_outward_today = count(
            "SELECT COUNT(*) FROM outward_gate_pass WHERE DATE(date_time) = :today AND station = :station",
            {"today": today, "station": station_name}
        )
        total_returnable_today = count(
            """
            SELECT COUNT(*) 
            FROM returnable_gate_pass rgp
            JOIN outward_gate_pass ogp ON rgp.outward_id = ogp.outward_id
            WHERE DATE(rgp.date_time) = :today
            AND ogp.station = :station
            """,
            {"today": today, "station": station_name}
        )

    total_gate_pass_today = total_inward_today + total_outward_today + total_returnable_today

    # ── 2. Pending Approvals (inward + outward) ─────────────────────────────
    if is_admin:
        pending_inward = count(
            "SELECT COUNT(*) FROM inward_gate_pass WHERE LOWER(status) = 'pending approval'"
        )
        pending_outward = count(
            "SELECT COUNT(*) FROM outward_gate_pass WHERE LOWER(status) = 'pending approval'"
        )
    else:
        pending_inward = count(
            "SELECT COUNT(*) FROM inward_gate_pass WHERE LOWER(status) = 'pending approval' AND station = :station",
            {"station": station_name}
        )
        pending_outward = count(
            "SELECT COUNT(*) FROM outward_gate_pass WHERE LOWER(status) = 'pending approval' AND station = :station",
            {"station": station_name}
        )

    pending_approvals = pending_inward + pending_outward

    # ── 3. Returnable Pending ───────────────────────────────────────────────
    if is_admin:
        returnable_pending = count(
            "SELECT COUNT(*) FROM returnable_gate_pass WHERE LOWER(status) = 'returnable'"
        )
    else:
        returnable_pending = count(
            """
            SELECT COUNT(*) 
            FROM returnable_gate_pass rgp
            JOIN outward_gate_pass ogp ON rgp.outward_id = ogp.outward_id
            WHERE LOWER(rgp.status) = 'returnable'
            AND ogp.station = :station
            """,
            {"station": station_name}
        )

    # ── 4. Total Inward Passes (all time) ───────────────────────────────────
    if is_admin:
        total_inward_passes = count("SELECT COUNT(*) FROM inward_gate_pass")
    else:
        total_inward_passes = count(
            "SELECT COUNT(*) FROM inward_gate_pass WHERE station = :station",
            {"station": station_name}
        )

    # ── 5. Total Outward Passes (all time) ──────────────────────────────────
    if is_admin:
        total_outward_passes = count("SELECT COUNT(*) FROM outward_gate_pass")
    else:
        total_outward_passes = count(
            "SELECT COUNT(*) FROM outward_gate_pass WHERE station = :station",
            {"station": station_name}
        )

    # ── 6. Total Returnable Passes (all time) ────────────────────────────────
    if is_admin:
        total_returnable_passes = count("SELECT COUNT(*) FROM returnable_gate_pass")
    else:
        total_returnable_passes = count(
            """
            SELECT COUNT(*)
            FROM returnable_gate_pass rgp
            JOIN outward_gate_pass ogp ON rgp.outward_id = ogp.outward_id
            WHERE ogp.station = :station
            """,
            {"station": station_name}
        )

    # ── 7. Total Entries ────────────────────────────────────────────────────
    total_entries = total_inward_passes + total_outward_passes + total_returnable_passes

    return {
        "total_gate_pass_today":   total_gate_pass_today,
        "pending_approvals":       pending_approvals,
        "returnable_pending":      returnable_pending,
        "total_inward_passes":     total_inward_passes,
        "total_outward_passes":    total_outward_passes,
        "total_returnable_passes": total_returnable_passes,
        "total_entries":           total_entries,
    }
