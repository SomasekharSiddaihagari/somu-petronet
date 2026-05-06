from datetime import date, time, timedelta
from fastapi import Depends
from pydantic import BaseModel
from requests import Session
from sqlalchemy import text
from typing import Any, Dict, Optional
from typing import List, Optional

from app.crud.digital_logbook.geo_fencing.verification_logic import get_all_current_shift_incharges
from app.database import get_db
from app.schemas.digital_logbook.geo_fencing.common import HandoverAcceptSchema, HandoverRequestSchema
from app.schemas.digital_logbook.geo_fencing.geo_acs_schemas import APIResponse
from app.utils.UserAuthUtils import verify_access_token
from app.utils.shift_service import accept_handover, request_handover
from fastapi import APIRouter, Depends, HTTPException, Header
from fastapi import Header, HTTPException, Depends
import uuid

from apscheduler.schedulers.background import BackgroundScheduler
from app.database import SessionLocal


from fastapi import APIRouter, Depends, Header, Query, HTTPException
from app.database import get_db
router = APIRouter(tags=["Shift handover "] ,prefix="/digital")


from pydantic import BaseModel
from datetime import datetime


class CurrentShiftInchargeResponse(BaseModel):
    station_id: int
    station_name: str
    station_code: str

    shift_id: int

    user_id: int
    first_name: Optional[str]
    last_name: Optional[str]
    employee_code: Optional[str]
    designation: Optional[str]
    email: Optional[str]

    responsibility_from: datetime

    class Config:
        from_attributes = True

# @router.get(
#     "/current-incharge",
#     response_model=List[CurrentShiftInchargeResponse],
#     summary="Get current shift in-charge for all stations"
# )
# def get_current_shift_incharge(
#     conn=Depends(get_db)
# ):
#     return get_all_current_shift_incharges(conn)




# @router.get("/my")
# def get_my_location_access_approvals(
#     user_id: int = Query(...),
#     db=Depends(get_db)
# ):
#     print("DEBUG: user_id =", user_id)

#     query = text("""
#         SELECT DISTINCT
#             laa.id,
#             laa.requested_station_id,
#             rs.station_name AS requested_station_name,

#             laa.approved_by_station_id,
#             aps.station_name AS approved_station_name,

#             laa.requested_by_user_id,
#             ru.username AS requested_by_username,
#             ru.first_name AS requested_by_first_name,
#             ru.last_name AS requested_by_last_name,

#             laa.approved_by_user_id,
#             au.username AS approved_by_username,
#             au.first_name AS approved_by_first_name,
#             au.last_name AS approved_by_last_name,
#               laa.status  AS status,


#             laa.approved_at,
#             laa.expires_at
#         FROM location_access_approval laa

#         JOIN users ru ON ru.user_id = laa.requested_by_user_id
#         JOIN users au ON au.user_id = laa.approved_by_user_id

#         JOIN station rs ON rs.station_id = laa.requested_station_id
#         JOIN station aps ON aps.station_id = laa.approved_by_station_id

#         WHERE laa.requested_by_user_id = :user_id
#            OR laa.approved_by_user_id = :user_id

#         ORDER BY laa.id DESC
#     """)

#     result = db.execute(query, {"user_id": user_id}).mappings().all()

#     print("DEBUG: result count =", len(result))

#     return {
#         "count": len(result),
#         "data": result
#     }


@router.get("/my")
def get_my_location_access_approvals(
    user_id: int = Query(...),
    db=Depends(get_db)
):
    print("DEBUG: user_id =", user_id)

    # Step 1: Check if user has role_id = 4
    role_query = text("""
        SELECT 1
        FROM role_permissions
        WHERE user_id = :user_id
        AND role_id = 4 AND submenu_id = 1
        LIMIT 1
    """)

    role_result = db.execute(role_query, {"user_id": user_id}).fetchone()

    # Step 2: Decide filter condition
    if role_result:
        # Admin → show all records
        filter_condition = ""
        params = {}
        print("DEBUG: User has role_id=4 → Fetching ALL records")
    else:
        # Normal user → only approvals done by this user
        filter_condition = "WHERE laa.approved_by_user_id = :user_id"
        params = {"user_id": user_id}
        print("DEBUG: Normal user → Fetching only approved_by_user_id records")

    query = text(f"""
        SELECT DISTINCT
            laa.id,
            laa.requested_station_id,
            rs.station_name AS requested_station_name,

            laa.approved_by_station_id,
            aps.station_name AS approved_station_name,

            laa.requested_by_user_id,
            ru.username AS requested_by_username,
            ru.first_name AS requested_by_first_name,
            ru.last_name AS requested_by_last_name,

            laa.approved_by_user_id,
            au.username AS approved_by_username,
            au.first_name AS approved_by_first_name,
            au.last_name AS approved_by_first_name,
            laa.reason,
            laa.status,
            laa.approved_at,
            laa.expires_at

        FROM location_access_approval laa

        JOIN users ru ON ru.user_id = laa.requested_by_user_id
        JOIN users au ON au.user_id = laa.approved_by_user_id

        JOIN station rs ON rs.station_id = laa.requested_station_id
        JOIN station aps ON aps.station_id = laa.approved_by_station_id

        {filter_condition}

        ORDER BY laa.id DESC
    """)

    result = db.execute(query, params).mappings().all()

    print("DEBUG: result count =", len(result))

    return {
        "count": len(result),
        "data": result
    }

@router.get("/by_id")
def get_location_access_approval_by_id(
    approval_id: int = Query(...),
    db=Depends(get_db)
):
    print("DEBUG: approval_id =", approval_id)

    query = text("""
        SELECT DISTINCT
            laa.id,
            laa.requested_station_id,
            rs.station_name AS requested_station_name,

            laa.approved_by_station_id,
            aps.station_name AS approved_station_name,

            laa.requested_by_user_id,
            ru.username AS requested_by_username,
            ru.first_name AS requested_by_first_name,
            ru.last_name AS requested_by_last_name,

            laa.approved_by_user_id,
            au.username AS approved_by_username,
            au.first_name AS approved_by_first_name,
            au.last_name AS approved_by_last_name,
            laa.reason,
            laa.status,
            laa.approved_at,
            laa.expires_at

        FROM location_access_approval laa

        JOIN users ru ON ru.user_id = laa.requested_by_user_id
        JOIN users au ON au.user_id = laa.approved_by_user_id

        JOIN station rs ON rs.station_id = laa.requested_station_id
        JOIN station aps ON aps.station_id = laa.approved_by_station_id

        WHERE laa.id = :approval_id
    """)

    result = db.execute(query, {"approval_id": approval_id}).mappings().fetchone()

    print("DEBUG: result =", result)

    if not result:
        raise HTTPException(status_code=404, detail="Approval record not found")

    return {
        "data": result
    }



@router.get("/all")
def get_all_location_access_approvals(
    db=Depends(get_db)
):
    query = text("""
        SELECT DISTINCT
            laa.id,
            laa.requested_station_id,
            rs.station_name AS requested_station_name,

            laa.approved_by_station_id,
            aps.station_name AS approved_station_name,

            laa.requested_by_user_id,
            ru.username AS requested_by_username,
            ru.first_name AS requested_by_first_name,
            ru.last_name AS requested_by_last_name,

            laa.approved_by_user_id,
            au.username AS approved_by_username,
            au.first_name AS approved_by_first_name,
            au.last_name AS approved_by_last_name,
            laa.status  AS status,

            laa.approved_at,
            laa.expires_at
        FROM location_access_approval laa

        JOIN users ru ON ru.user_id = laa.requested_by_user_id
        JOIN users au ON au.user_id = laa.approved_by_user_id

        JOIN station rs ON rs.station_id = laa.requested_station_id
        JOIN station aps ON aps.station_id = laa.approved_by_station_id

        ORDER BY laa.id DESC
    """)

    result = db.execute(query).mappings().all()

    return {
        "count": len(result),
        "data": result
    }

@router.get(
    "/pending-handover",
    summary="Get latest pending handover request for a user"
)
def get_latest_pending_handover(
    user_id: int = Query(..., description="User ID"),
    db: Session = Depends(get_db)
):
    print("\n==============================")
    print("DEBUG: get_latest_pending_handover")
    print("DEBUG: user_id =", user_id)
    print("==============================")

    query = text("""
        SELECT
            ssi.id,
            ssi.station_id,
            ssi.shift_id,

            ssi.user_id AS from_user_id,
            fu.first_name AS from_user_first_name,
            fu.last_name AS from_user_last_name,

            ssi.handover_to_user_id AS to_user_id,
            tu.first_name AS to_user_first_name,
            tu.last_name AS to_user_last_name,

            ssi.handover_requested_at,
            ssi.comment_for_next_incharge,
            ssi.created_at
        FROM station_shift_incharge ssi
        JOIN users fu ON fu.user_id = ssi.user_id
        JOIN users tu ON tu.user_id = ssi.handover_to_user_id
        WHERE ssi.handover_to_user_id = :user_id
          AND ssi.handover_accepted_at IS NULL
        ORDER BY
            ssi.handover_requested_at DESC NULLS LAST,
            ssi.created_at DESC
        LIMIT 1
    """)

    row = db.execute(query, {"user_id": user_id}).mappings().first()

    print("DEBUG: pending_handover_row =", row)

    if not row:
        return {
            "user_id": user_id,
            "has_pending_handover": False,
            "data": None
        }

    return {
        "user_id": user_id,
        "has_pending_handover": True,
        "data": {
            "handover_id": row["id"],
            "station_id": row["station_id"],
            "shift_id": row["shift_id"],

            "from_user": {
                "id": row["from_user_id"],
                "first_name": row["from_user_first_name"],
                "last_name": row["from_user_last_name"]
            },

            "to_user": {
                "id": row["to_user_id"],
                "first_name": row["to_user_first_name"],
                "last_name": row["to_user_last_name"]
            },

            "handover_requested_at": row["handover_requested_at"],
            "comment_for_next_incharge": row["comment_for_next_incharge"]
        }
    }

# @router.get(
#     "/digital-role",
#     summary="Resolve user role + always return current shift in-charge"
# )
# def resolve_user_role_and_status(
#     user_id: int = Query(..., description="User ID to resolve"),
#     db: Session = Depends(get_db)
# ):
#     # AUTO-CANCEL expired handover requests

#     user_station = db.execute(
#         text("""
#             SELECT 
#                 s.station_id,
#                 s.station_name
#             FROM users u
#             JOIN station s 
#                 ON s.station_id = u.station_id
#             WHERE u.user_id = :user_id
#         """),
#         {"user_id": user_id}
#     ).mappings().first()
    


#     # ==================================================
#     # A️⃣ GET CURRENT ACTIVE SHIFT IN-CHARGE (ALWAYS)
#     # ==================================================
#     current_shift = db.execute(
#         text("""
#             SELECT
#                 ssi.station_id,
#                 ssi.shift_id,
#                 ssi.responsibility_from,
            
#                 st.station_name,
            
#                 u.first_name,
#                 u.last_name,
            
#                 LSM.ms_logbook_id,
#                 LSM.created_by,
#                 LSM.created_at,
#                 LSM.technician_id,
#                 CONCAT(u2.first_name, ' ', u2.last_name) AS technician_name

             
            
#             FROM station_shift_incharge ssi
            
#             JOIN station st
#                 ON st.station_id = ssi.station_id
            
#             JOIN users u
#                 ON u.user_id = ssi.user_id
                        
#             JOIN logbook_shift_master LSM
#                 ON LSM.assigned_to = ssi.user_id
             
#              LEFT JOIN users u2
#                 ON u2.user_id = LSM.technician_id
            
#             WHERE ssi.responsibility_to IS NULL
#             AND ssi.user_id = :user_id
            
#             ORDER BY ssi.responsibility_from DESC, LSM.ms_logbook_id DESC
#             LIMIT 1;
#         """),
#          {"user_id": user_id}
#     ).mappings().first()

#     # Normalize shift-incharge info
#     shift_info = {
#         "station_id": user_station["station_id"] if user_station else None,
#         "station_name": user_station["station_name"] if user_station else None,
#         "shift_id": None,
#         "shift_start_date": None,
#         "shift_start_time": None,
#         "first_name": None,
#         "last_name": None,
#         "ms_logbook_id": None,
#         "created_by" : None,
#         "created_at" : None,
#         "technician_id" : None,
#         "technician_name" : None
#     }

#     if current_shift:
#         rf = current_shift["responsibility_from"]
#         shift_info = {
#             "station_id": current_shift["station_id"],
#             "station_name": current_shift["station_name"],
#             "shift_id": current_shift["shift_id"],
#             "shift_start_date": rf.date() if rf else None,
#             "shift_start_time": rf.time() if rf else None,
#             "first_name": current_shift["first_name"],
#             "last_name": current_shift["last_name"],
#             "ms_logbook_id": current_shift["ms_logbook_id"],
#             "created_by": current_shift["created_by"],
#             "created_at": current_shift["created_at"],
#             "technician_id": current_shift["technician_id"],
#             "technician_name": current_shift["technician_name"]
#         }

#     # ==================================================
#     # 1️⃣ PENDING TAKEOVER REQUEST
#     # ==================================================
#     pending_row = db.execute(
#         text("""
#             SELECT 1
#             FROM station_shift_incharge
#             WHERE handover_to_user_id = :user_id
#               AND handover_accepted_at IS NULL
#             LIMIT 1
#         """),
#         {"user_id": user_id}
#     ).first()

#     if pending_row:
#         return {
#             "user_id": user_id,
#             "pending_takeover_request": True,
#             "is_shift_incharge": False,
#             "normal_employee": False,
#             "role_id": None,
#             "role_name": "Pending Shift Takeover",
#             "source": "PENDING_TAKEOVER",
#             **shift_info
#         }

#     # ==================================================
#     # 2️⃣ ACTIVE SHIFT IN-CHARGE (FOR THIS USER)
#     # ==================================================
#     is_shift_incharge = db.execute(
#         text("""
#             SELECT 1
#             FROM station_shift_incharge
#             WHERE user_id = :user_id
#               AND responsibility_to IS NULL
#             LIMIT 1
#         """),
#         {"user_id": user_id}
#     ).first()

#     if is_shift_incharge:
#         return {
#             "user_id": user_id,
#             "pending_takeover_request": False,
#             "is_shift_incharge": True,
#             "normal_employee": False,
#             "role_id": None,
#             "role_name": "Shift Incharge",
#             "source": "SHIFT_INCHARGE",
#             **shift_info
#         }

#     # ==================================================
#     # 3️⃣ ROLE FROM ROLE PERMISSIONS
#     # ==================================================
#     role_row = db.execute(
#         text("""
#             SELECT DISTINCT
#                 r.role_id,
#                 r.role_name
#             FROM roles r
#             JOIN role_permissions rp
#                 ON rp.role_id = r.role_id
#             WHERE rp.user_id = :user_id
#               AND rp.submenu_id = 1
#               AND r.is_deleted = FALSE
#             LIMIT 1
#         """),
#         {"user_id": user_id}
#     ).mappings().first()

#     if role_row:
#         return {
#             "user_id": user_id,
#             "pending_takeover_request": False,
#             "is_shift_incharge": False,
#             "normal_employee": False,
#             "role_id": role_row["role_id"],
#             "role_name": role_row["role_name"],
#             "source": "ROLE_PERMISSION",
#             **shift_info
#         }

#     # ==================================================
#     # 4️⃣ NORMAL EMPLOYEE (DEFAULT)
#     # ==================================================
#     return {
#         "user_id": user_id,
#         "pending_takeover_request": False,
#         "is_shift_incharge": False,
#         "normal_employee": True,
#         "role_id": None,
#         "role_name": "Employee",
#         "source": "DEFAULT",
#         **shift_info
#     }




# @router.get(
#     "/digital-role",
#     summary="Resolve user role + always return current shift in-charge"
# )
# def resolve_user_role_and_status(
#     user_id: int = Query(..., description="User ID to resolve"),
#     db: Session = Depends(get_db)
# ):
#     # ==================================================
#     # 🔄 AUTO-CANCEL EXPIRED HANDOVER REQUESTS (>15 min)
#     # ==================================================
#     db.execute(
#         text("""
#             UPDATE station_shift_incharge
#             SET 
#                 handover_to_user_id = NULL,
#                 handover_requested_at = NULL,
#                 comment_for_next_incharge = NULL
#             WHERE handover_to_user_id IS NOT NULL
#               AND handover_accepted_at IS NULL
#               AND handover_requested_at < NOW() - INTERVAL '15 minutes'
#               AND responsibility_to IS NULL
#         """)
#     )
#     db.commit()

#     # ==================================================
#     # 🏠 GET USER'S STATION
#     # ==================================================
#     user_station = db.execute(
#         text("""
#             SELECT 
#                 s.station_id,
#                 s.station_name
#             FROM users u
#             JOIN station s 
#                 ON s.station_id = u.station_id
#             WHERE u.user_id = :user_id
#         """),
#         {"user_id": user_id}
#     ).mappings().first()

#     # ==================================================
#     # A️⃣ GET CURRENT ACTIVE SHIFT IN-CHARGE (ALWAYS)
#     # ==================================================
#     current_shift = db.execute(
#         text("""
#             SELECT
#                 ssi.station_id,
#                 ssi.shift_id,
#                 ssi.responsibility_from,
#                 st.station_name,
#                 u.first_name,
#                 u.last_name,
#                 LSM.ms_logbook_id,
#                 LSM.created_by,
#                 LSM.created_at,
#                 LSM.technician_id,
#                 CONCAT(u2.first_name, ' ', u2.last_name) AS technician_name
#             FROM station_shift_incharge ssi
#             JOIN station st
#                 ON st.station_id = ssi.station_id
#             JOIN users u
#                 ON u.user_id = ssi.user_id
#             JOIN logbook_shift_master LSM
#                 ON LSM.assigned_to = ssi.user_id
#             LEFT JOIN users u2
#                 ON u2.user_id = LSM.technician_id
#             WHERE ssi.responsibility_to IS NULL
#               AND ssi.user_id = :user_id
#             ORDER BY ssi.responsibility_from DESC, LSM.ms_logbook_id DESC
#             LIMIT 1
#         """),
#         {"user_id": user_id}
#     ).mappings().first()

#     # Normalize shift-incharge info
#     shift_info = {
#         "station_id": user_station["station_id"] if user_station else None,
#         "station_name": user_station["station_name"] if user_station else None,
#         "shift_id": None,
#         "shift_start_date": None,
#         "shift_start_time": None,
#         "first_name": None,
#         "last_name": None,
#         "ms_logbook_id": None,
#         "created_by": None,
#         "created_at": None,
#         "technician_id": None,
#         "technician_name": None
#     }

#     if current_shift:
#         rf = current_shift["responsibility_from"]
#         shift_info = {
#             "station_id": current_shift["station_id"],
#             "station_name": current_shift["station_name"],
#             "shift_id": current_shift["shift_id"],
#             "shift_start_date": rf.date() if rf else None,
#             "shift_start_time": rf.time() if rf else None,
#             "first_name": current_shift["first_name"],
#             "last_name": current_shift["last_name"],
#             "ms_logbook_id": current_shift["ms_logbook_id"],
#             "created_by": current_shift["created_by"],
#             "created_at": current_shift["created_at"],
#             "technician_id": current_shift["technician_id"],
#             "technician_name": current_shift["technician_name"]
#         }

#     # ==================================================
#     # 1️⃣ CHECK IF USER IS ACTIVE SHIFT INCHARGE 
#     #    AND HAS REQUESTED HANDOVER (SENDER)
#     # ==================================================
#     sender_row = db.execute(
#         text("""
#             SELECT 
#                 CASE 
#                     WHEN handover_requested_at IS NOT NULL
#                     AND handover_accepted_at IS NULL
#                     AND handover_requested_at AT TIME ZONE 'UTC' >= (NOW() AT TIME ZONE 'UTC') - INTERVAL '15 minutes'
#                     THEN TRUE
#                     ELSE FALSE
#                 END AS has_pending_request
#             FROM station_shift_incharge
#             WHERE user_id = :user_id
#             AND responsibility_to IS NULL
#             LIMIT 1
#         """),
#         {"user_id": user_id}
#     ).mappings().first()

#     if sender_row:
#         has_pending = sender_row["has_pending_request"]
#         return {
#             "user_id": user_id,
#             "pending_takeover_request": True if has_pending else False,
#             "is_shift_incharge": True,
#             "normal_employee": False,
#             "role_id": None,
#             "role_name": "Shift Incharge",
#             "source": "SHIFT_INCHARGE",
#             **shift_info
#         }

#     # ==================================================
#     # 2️⃣ PENDING TAKEOVER REQUEST (RECEIVER, 15-min window)
#     # ==================================================
#     pending_row = db.execute(
#         text("""
#             SELECT 1
#             FROM station_shift_incharge
#             WHERE handover_to_user_id = :user_id
#             AND handover_accepted_at IS NULL
#             AND handover_requested_at AT TIME ZONE 'UTC' >= (NOW() AT TIME ZONE 'UTC') - INTERVAL '15 minutes'
#             LIMIT 1
#         """),
#         {"user_id": user_id}
#     ).first()

#     if pending_row:
#         return {
#             "user_id": user_id,
#             "pending_takeover_request": True,
#             "is_shift_incharge": False,
#             "normal_employee": False,
#             "role_id": None,
#             "role_name": "Pending Shift Takeover",
#             "source": "PENDING_TAKEOVER",
#             **shift_info
#         }

#     # ==================================================
#     # 3️⃣ ROLE FROM ROLE PERMISSIONS
#     # ==================================================
#     role_row = db.execute(
#         text("""
#             SELECT DISTINCT
#                 r.role_id,
#                 r.role_name
#             FROM roles r
#             JOIN role_permissions rp
#                 ON rp.role_id = r.role_id
#             WHERE rp.user_id = :user_id
#               AND rp.submenu_id = 1
#               AND r.is_deleted = FALSE
#             LIMIT 1
#         """),
#         {"user_id": user_id}
#     ).mappings().first()

#     if role_row:
#         return {
#             "user_id": user_id,
#             "pending_takeover_request": False,
#             "is_shift_incharge": False,
#             "normal_employee": False,
#             "role_id": role_row["role_id"],
#             "role_name": role_row["role_name"],
#             "source": "ROLE_PERMISSION",
#             **shift_info
#         }

#     # ==================================================
#     # 4️⃣ NORMAL EMPLOYEE (DEFAULT)
#     # ==================================================
#     return {
#         "user_id": user_id,
#         "pending_takeover_request": False,
#         "is_shift_incharge": False,
#         "normal_employee": True,
#         "role_id": None,
#         "role_name": "Employee",
#         "source": "DEFAULT",
#         **shift_info
#     }

@router.get(
    "/digital-role",
    summary="Resolve user role + always return current shift in-charge"
)
def resolve_user_role_and_status(
    user_id: int = Query(..., description="User ID to resolve"),
    db: Session = Depends(get_db)
):
    # ==================================================
    # 🔄 AUTO-CANCEL EXPIRED HANDOVER REQUESTS (>15 min)
    # ==================================================
    db.execute(
        text("""
            UPDATE station_shift_incharge
            SET 
                handover_to_user_id = NULL,
                handover_requested_at = NULL,
                comment_for_next_incharge = NULL
            WHERE handover_to_user_id IS NOT NULL
              AND handover_accepted_at IS NULL
              AND handover_requested_at < NOW() - INTERVAL '15 minutes'
              AND responsibility_to IS NULL
        """)
    )
    db.commit()

    # ==================================================
    # 🏠 GET USER'S STATION
    # ==================================================
    user_station = db.execute(
        text("""
            SELECT 
                s.station_id,
                s.station_name
            FROM users u
            JOIN station s 
                ON s.station_id = u.station_id
            WHERE u.user_id = :user_id
        """),
        {"user_id": user_id}
    ).mappings().first()

    # ==================================================
    # A️⃣ GET CURRENT ACTIVE SHIFT IN-CHARGE (ALWAYS)
    # ✅ FIXED: Filter by station_id instead of user_id
    #    so any role gets the active incharge of their station
    # ==================================================
    current_shift = None
    if user_station:
        current_shift = db.execute(
            text("""
                SELECT
                    ssi.station_id,
                    ssi.shift_id,
                    ssi.responsibility_from,
                    st.station_name,
                    u.first_name,
                    u.last_name,
                    LSM.ms_logbook_id,
                    LSM.created_by,
                    LSM.created_at,
                    LSM.technician_id,
                    CONCAT(u2.first_name, ' ', u2.last_name) AS technician_name
                FROM station_shift_incharge ssi
                JOIN station st
                    ON st.station_id = ssi.station_id
                JOIN users u
                    ON u.user_id = ssi.user_id
                JOIN logbook_shift_master LSM
                    ON LSM.assigned_to = ssi.user_id
                LEFT JOIN users u2
                    ON u2.user_id = LSM.technician_id
                WHERE ssi.responsibility_to IS NULL
                  AND ssi.station_id = :station_id
                ORDER BY ssi.responsibility_from DESC, LSM.ms_logbook_id DESC
                LIMIT 1
            """),
            {"station_id": user_station["station_id"]}
        ).mappings().first()

    # Normalize shift-incharge info
    shift_info = {
        "station_id": user_station["station_id"] if user_station else None,
        "station_name": user_station["station_name"] if user_station else None,
        "shift_id": None,
        "shift_start_date": None,
        "shift_start_time": None,
        "first_name": None,
        "last_name": None,
        "ms_logbook_id": None,
        "created_by": None,
        "created_at": None,
        "technician_id": None,
        "technician_name": None
    }

    if current_shift:
        rf = current_shift["responsibility_from"]
        shift_info = {
            "station_id": current_shift["station_id"],
            "station_name": current_shift["station_name"],
            "shift_id": current_shift["shift_id"],
            "shift_start_date": rf.date() if rf else None,
            "shift_start_time": rf.time() if rf else None,
            "first_name": current_shift["first_name"],
            "last_name": current_shift["last_name"],
            "ms_logbook_id": current_shift["ms_logbook_id"],
            "created_by": current_shift["created_by"],
            "created_at": current_shift["created_at"],
            "technician_id": current_shift["technician_id"],
            "technician_name": current_shift["technician_name"]
        }

    # ==================================================
    # 1️⃣ CHECK IF USER IS ACTIVE SHIFT INCHARGE 
    #    AND HAS REQUESTED HANDOVER (SENDER)
    # ==================================================
    sender_row = db.execute(
        text("""
            SELECT 
                CASE 
                    WHEN handover_requested_at IS NOT NULL
                    AND handover_accepted_at IS NULL
                    AND handover_requested_at AT TIME ZONE 'UTC' >= (NOW() AT TIME ZONE 'UTC') - INTERVAL '15 minutes'
                    THEN TRUE
                    ELSE FALSE
                END AS has_pending_request
            FROM station_shift_incharge
            WHERE user_id = :user_id
            AND responsibility_to IS NULL
            LIMIT 1
        """),
        {"user_id": user_id}
    ).mappings().first()

    if sender_row:
        has_pending = sender_row["has_pending_request"]
        return {
            "user_id": user_id,
            "pending_takeover_request": True if has_pending else False,
            "is_shift_incharge": True,
            "normal_employee": False,
            "role_id": None,
            "role_name": "Shift Incharge",
            "source": "SHIFT_INCHARGE",
            **shift_info
        }

    # ==================================================
    # 2️⃣ PENDING TAKEOVER REQUEST (RECEIVER, 15-min window)
    # ==================================================
    pending_row = db.execute(
        text("""
            SELECT 1
            FROM station_shift_incharge
            WHERE handover_to_user_id = :user_id
            AND handover_accepted_at IS NULL
            AND handover_requested_at AT TIME ZONE 'UTC' >= (NOW() AT TIME ZONE 'UTC') - INTERVAL '15 minutes'
            LIMIT 1
        """),
        {"user_id": user_id}
    ).first()

    if pending_row:
        return {
            "user_id": user_id,
            "pending_takeover_request": True,
            "is_shift_incharge": False,
            "normal_employee": False,
            "role_id": None,
            "role_name": "Pending Shift Takeover",
            "source": "PENDING_TAKEOVER",
            **shift_info
        }

    # ==================================================
    # 3️⃣ ROLE FROM ROLE PERMISSIONS
    # ==================================================
    role_row = db.execute(
        text("""
            SELECT DISTINCT
                r.role_id,
                r.role_name
            FROM roles r
            JOIN role_permissions rp
                ON rp.role_id = r.role_id
            WHERE rp.user_id = :user_id
              AND rp.submenu_id = 1
              AND r.is_deleted = FALSE
            LIMIT 1
        """),
        {"user_id": user_id}
    ).mappings().first()

    if role_row:
        return {
            "user_id": user_id,
            "pending_takeover_request": False,
            "is_shift_incharge": False,
            "normal_employee": False,
            "role_id": role_row["role_id"],
            "role_name": role_row["role_name"],
            "source": "ROLE_PERMISSION",
            **shift_info
        }

    # ==================================================
    # 4️⃣ NORMAL EMPLOYEE (DEFAULT)
    # ==================================================
    return {
        "user_id": user_id,
        "pending_takeover_request": False,
        "is_shift_incharge": False,
        "normal_employee": True,
        "role_id": None,
        "role_name": "Employee",
        "source": "DEFAULT",
        **shift_info
    }





class UpdateTechnician(BaseModel):
    technician_id: int

@router.patch("/update-technician/{ms_logbook_id}")
def update_technician(ms_logbook_id: int, data: UpdateTechnician, db: Session = Depends(get_db)):
    
    query = text("""
        UPDATE logbook_shift_master
        SET technician_id = :technician_id
        WHERE ms_logbook_id = :ms_logbook_id
        RETURNING ms_logbook_id, technician_id
    """)

    result = db.execute(query, {
        "technician_id": data.technician_id,
        "ms_logbook_id": ms_logbook_id
    }).fetchone()

    if not result:
        raise HTTPException(status_code=404, detail="Record not found")

    db.commit()

    return {
        "status": "success",
        "ms_logbook_id": result.ms_logbook_id,
        "technician_id": result.technician_id
    }

from datetime import datetime
from fastapi import HTTPException, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session

class UpdateTechnicians(BaseModel):
    technician_id: int
    created_by: int


@router.patch("/update-technicians/{ms_logbook_id}")
def update_technician(ms_logbook_id: int, data: UpdateTechnicians, db: Session = Depends(get_db)):

    now = datetime.utcnow()

    query = text("""
        UPDATE logbook_shift_master
    SET 
        technician_id = :technician_id,

        all_technicians = (
            (
                SELECT COALESCE(jsonb_agg(
                    CASE 
                        WHEN (value->>'to_date') IS NULL
                        THEN jsonb_set(value, '{to_date}', to_jsonb(:now))
                        ELSE value
                    END
                ), '[]'::jsonb)
                FROM jsonb_array_elements(
                    COALESCE(all_technicians::jsonb, '[]'::jsonb)
                ) AS arr(value)
            )

            ||

            jsonb_build_array(
                jsonb_build_object(
                    'technician_id', :technician_id,
                    'created_by', :created_by,
                    'from_date', :now,
                    'to_date', NULL
                )
            )
        )::json   -- 🔥 convert back to JSON

    WHERE ms_logbook_id = :ms_logbook_id

    RETURNING ms_logbook_id, technician_id, all_technicians
    """)

    result = db.execute(query, {
        "technician_id": data.technician_id,
        "created_by": data.created_by,
        "now": now,
        "ms_logbook_id": ms_logbook_id
    }).fetchone()

    if not result:
        raise HTTPException(status_code=404, detail="Record not found")

    db.commit()

    return {
        "status": "success",
        "ms_logbook_id": result.ms_logbook_id,
        "technician_id": result.technician_id,
        # "all_technicians": result.all_technicians
    }

@router.get("/technicians")
def get_technicians(
    station_id: int = Query(..., description="Station ID"),
    db: Session = Depends(get_db)
):
    query = text("""
        SELECT 
            u.user_id,
            COALESCE(u.username, '') AS username,
            COALESCE(CONCAT(u.first_name, ' ', u.last_name), '') AS full_name,
            r.role_name
        FROM users u
        JOIN role_permissions rp 
            ON rp.user_id = u.user_id
        JOIN roles r 
            ON r.role_id = rp.role_id
        WHERE rp.role_id = 18
          AND u.station_id = :station_id
          AND u.is_deleted = FALSE
    """)

    result = db.execute(query, {"station_id": station_id}).fetchall()

    return {
        "status": "success",
        "data": [dict(row._mapping) for row in result]
    }


@router.post(
    "/handover/request",
    response_model=APIResponse,
    summary="Request shift handover"
)
def handover_request(
    payload: HandoverRequestSchema,
    conn=Depends(get_db)
):
    request_handover(
        conn,
        payload.comment_for_next_incharge,
        payload.station_id,
        payload.shift_id,
        payload.from_user_id,
        payload.to_user_id
    )

    return {
        "status_code": 200,
        "status_message": "Handover requested successfully",
        "data": {
            "comment_for_next_incharge": payload.comment_for_next_incharge,
            "station_id": payload.station_id,
            "shift_id": payload.shift_id,
            "from_user_id": payload.from_user_id,
            "to_user_id": payload.to_user_id
        }
    }


@router.post(
    "/handover/accept",
    response_model=APIResponse,
    summary="Accept shift handover"
)
def handover_accept(
    payload: HandoverAcceptSchema,
    conn=Depends(get_db)
):
    accept_handover(
        conn,
        payload.station_id,
        payload.shift_id,
        payload.user_id
    )

    return {
        "status_code": 200,
        "status_message": "Handover accepted successfully",
        "data": {
            "station_id": payload.station_id,
            "shift_id": payload.shift_id,
            "accepted_by_user_id": payload.user_id
        }
    }



@router.get("/GetALlEngineersDD-digital")
def fetch_all_engineers(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: str = Depends(verify_access_token)
):
    from sqlalchemy.sql import text as sql_text

    try:
        query = sql_text("""
            SELECT DISTINCT
                u.user_id,
                u.username,
                u.first_name,
                u.last_name,
                u.email,
                u.contact_phone,
                r.role_name
            FROM users u
            INNER JOIN role_permissions rp ON rp.user_id = u.user_id
            INNER JOIN roles r ON r.role_id = rp.role_id
            WHERE rp.submenu_id = :submenu_id
              AND rp.role_id = :role_id
              AND u.station_id = (
                  SELECT station_id
                  FROM users
                  WHERE user_id = :current_user_id
              )
        """)

        result = db.execute(
            query,
            {
                "submenu_id": 1,
                "role_id": 1,
                "current_user_id": user_id
            }
        ).fetchall()

        data = [
            {
                "user_id": row.user_id,
                "username": row.username,
                "first_name": row.first_name,
                "last_name": row.last_name,
                "email": row.email,
                "contact_phone": row.contact_phone,
                "role_name": row.role_name
            }
            for row in result
        ]

        return {
            "statusCode": "0000",
            "statusMessage": "Success",
            "data": data
        }

    except Exception as e:
        print("ENGINEER DD ERROR:", str(e))
        raise HTTPException(
            status_code=500,
            detail={
                "statusCode": "9999",
                "statusMessage": str(e),
                "data": []
            }
        )




@router.get(
    "/current-incharge",
    summary="Get current shift in-charge by station"
)


def get_current_shift_incharge(
    station_id: int = Query(...),
    db=Depends(get_db)
):
    query = text("""
        SELECT
            ssi.id AS incharge_id,
            ssi.station_id,
            st.station_name,
            ssi.shift_id,
            sh.shift_name,
            sh.start_time,
            sh.end_time,
            u.user_id,
            u.first_name,
            u.last_name,
            u.designation,
            u.employee_code,
            u.email,
            ssi.responsibility_from,

            -- Admin of that station
            admin_u.user_id      AS admin_user_id,
            admin_u.first_name   AS admin_first_name,
            admin_u.last_name    AS admin_last_name,
            admin_u.email        AS admin_email,
            admin_u.designation  AS admin_designation,
            admin_u.employee_code AS admin_employee_code

        FROM station_shift_incharge ssi
        JOIN users u ON u.user_id = ssi.user_id
        JOIN station st ON st.station_id = ssi.station_id
        JOIN shift sh ON sh.shift_id = ssi.shift_id

        -- Get admin belonging to same station
        LEFT JOIN LATERAL (
            SELECT
                u2.user_id,
                u2.first_name,
                u2.last_name,
                u2.email,
                u2.designation,
                u2.employee_code
            FROM role_permissions rp
            JOIN users u2 ON u2.user_id = rp.user_id
            WHERE rp.role_id = 4
              AND u2.station_id = ssi.station_id
              AND u2.is_deleted = FALSE
            LIMIT 1
        ) admin_u ON TRUE

        WHERE ssi.station_id != :station_id
          AND ssi.responsibility_to IS NULL
        ORDER BY ssi.station_id ASC
    """)

    rows = db.execute(query, {"station_id": station_id}).mappings().all()

    if not rows:
        return {"data": []}

    result = []
    for row in rows:
        result.append({
            "incharge_id": row["incharge_id"],
            "station_id": row["station_id"],
            "station_name": row["station_name"],
            "shift_id": row["shift_id"],
            "shift_name": row["shift_name"],
            "start_time": row["start_time"],
            "end_time": row["end_time"],
            "user_id": row["user_id"],
            "first_name": row["first_name"],
            "last_name": row["last_name"],
            "designation": row["designation"],
            "employee_code": row["employee_code"],
            "email": row["email"],
            "responsibility_from": row["responsibility_from"],
            "admin": {
                "user_id": row["admin_user_id"],
                "first_name": row["admin_first_name"],
                "last_name": row["admin_last_name"],
                "email": row["admin_email"],
                "designation": row["admin_designation"],
                "employee_code": row["admin_employee_code"]
            } if row["admin_user_id"] else None
        })

    return {"data": result}


@router.get(
    "/all-current-incharge",
    summary="Get current shift in-charge for all stations"
)


def get_all_current_incharge(
    db=Depends(get_db)
):
    query = text("""
        SELECT
            ssi.id AS incharge_id,
            ssi.station_id,
            st.station_name,
            ssi.shift_id,
            sh.shift_name,
            sh.start_time,
            sh.end_time,
            u.user_id,
            u.first_name,
            u.last_name,
            u.designation,
            u.employee_code,
            u.email,
            ssi.responsibility_from,

            admin_u.user_id       AS admin_user_id,
            admin_u.first_name    AS admin_first_name,
            admin_u.last_name     AS admin_last_name,
            admin_u.email         AS admin_email,
            admin_u.designation   AS admin_designation,
            admin_u.employee_code AS admin_employee_code

        FROM station_shift_incharge ssi
        JOIN users u ON u.user_id = ssi.user_id
        JOIN station st ON st.station_id = ssi.station_id
        JOIN shift sh ON sh.shift_id = ssi.shift_id

        LEFT JOIN LATERAL (
            SELECT
                u2.user_id,
                u2.first_name,
                u2.last_name,
                u2.email,
                u2.designation,
                u2.employee_code
            FROM role_permissions rp
            JOIN users u2 ON u2.user_id = rp.user_id
            WHERE rp.role_id = 4
              AND u2.station_id = ssi.station_id
              AND u2.is_deleted = FALSE
            LIMIT 1
        ) admin_u ON TRUE

        WHERE ssi.responsibility_to IS NULL
        ORDER BY ssi.station_id ASC
    """)

    rows = db.execute(query).mappings().all()

    if not rows:
        return {"data": []}

    result = []
    for row in rows:
        result.append({
            "incharge_id": row["incharge_id"],
            "station_id": row["station_id"],
            "station_name": row["station_name"],
            "shift_id": row["shift_id"],
            "shift_name": row["shift_name"],
            "start_time": row["start_time"],
            "end_time": row["end_time"],
            "user_id": row["user_id"],
            "first_name": row["first_name"],
            "last_name": row["last_name"],
            "designation": row["designation"],
            "employee_code": row["employee_code"],
            "email": row["email"],
            "responsibility_from": row["responsibility_from"],
            "admin": {
                "user_id": row["admin_user_id"],
                "first_name": row["admin_first_name"],
                "last_name": row["admin_last_name"],
                "email": row["admin_email"],
                "designation": row["admin_designation"],
                "employee_code": row["admin_employee_code"]
            } if row["admin_user_id"] else None
        })

    return {"data": result}




# @router.get("/shift-incharges-by-date")
# def get_shift_incharge_logs(
#     station_id: int = Query(..., description="Station ID"),
#     from_date: date = Query(..., description="From Date (YYYY-MM-DD)"),
#     to_date: date = Query(..., description="To Date (YYYY-MM-DD)"),
#     db: Session = Depends(get_db)
# ):
#     # -------------------------------
#     # VALIDATION
#     # -------------------------------
#     if from_date > to_date:
#         raise HTTPException(status_code=400, detail="from_date cannot be greater than to_date")

#     # -------------------------------
#     # QUERY
#     # -------------------------------
#     query = text("""
#         SELECT
#             shl.shift_id,

#             CASE
#                 WHEN shl.shift_id = 1 THEN 'Shift A'
#                 WHEN shl.shift_id = 2 THEN 'Shift B'
#                 WHEN shl.shift_id = 3 THEN 'Shift C'
#             END AS shift_name,

#             shl.station_id,

#             shl.from_user_id,
#             CONCAT(u1.first_name,' ',u1.last_name) AS handover_by,

#             shl.to_user_id,
#             CONCAT(u2.first_name,' ',u2.last_name) AS takeover_by,

#             shl.event_time

#         FROM shift_handover_log shl

#         LEFT JOIN users u1 
#             ON u1.user_id = shl.from_user_id

#         LEFT JOIN users u2 
#             ON u2.user_id = shl.to_user_id

#         WHERE shl.event_type = 'HANDOVER_ACCEPTED'
#         AND shl.station_id = :station_id

#         AND shl.event_time >= :from_date
#         AND shl.event_time < (:to_date + INTERVAL '1 day')

#         ORDER BY shl.event_time ASC;
#     """)

#     rows = db.execute(
#         query,
#         {
#             "station_id": station_id,
#             "from_date": from_date,
#             "to_date": to_date
#         }
#     ).mappings().all()

#     # -------------------------------
#     # RESPONSE
#     # -------------------------------
#     data: List[Dict[str, Any]] = [
#         {
#             "shift_id": row["shift_id"],
#             "shift_name": row["shift_name"],
#             "station_id": row["station_id"],
#             "from_user_id": row["from_user_id"],
#             "handover_by": row["handover_by"],
#             "to_user_id": row["to_user_id"],
#             "takeover_by": row["takeover_by"],
#             "event_time": row["event_time"]
#         }
#         for row in rows
#     ]

#     return {
#         "station_id": station_id,
#         "from_date": str(from_date),
#         "to_date": str(to_date),
#         "total_records": len(data),
#         "data": data
#     }



# @router.get("/shift-incharge-timeline")
# def get_shift_incharge_timeline(
#     station_id: int = Query(...),
#     from_date: date = Query(...),
#     to_date: date = Query(...),
#     db: Session = Depends(get_db)
# ):
#     if from_date > to_date:
#         raise HTTPException(status_code=400, detail="Invalid date range")

#     query = text("""
#         WITH handovers AS (
#             SELECT
#                 shl.shift_id,
#                 shl.station_id,

#                 shl.from_user_id,
#                 CONCAT(u1.first_name,' ',u1.last_name) AS handover_by,

#                 shl.to_user_id,
#                 CONCAT(u2.first_name,' ',u2.last_name) AS takeover_by,

#                 shl.event_time AS start_time,

#                 LEAD(shl.event_time) OVER (
#                     PARTITION BY shl.shift_id, shl.station_id
#                     ORDER BY shl.event_time
#                 ) AS end_time

#             FROM shift_handover_log shl

#             LEFT JOIN users u1 ON u1.user_id = shl.from_user_id
#             LEFT JOIN users u2 ON u2.user_id = shl.to_user_id

#             WHERE shl.event_type = 'HANDOVER_ACCEPTED'
#             AND shl.station_id = :station_id
#             AND shl.event_time >= :from_date
#             AND shl.event_time < (:to_date + INTERVAL '1 day')
#         ),

#         technicians AS (
#             SELECT
#                 lsm.ms_logbook_id,
#                 lsm.created_at,

#                 (tech.value->>'technician_id')::int AS technician_id,
#                 tech.value->>'from_date' AS tech_from,
#                 tech.value->>'to_date' AS tech_to

#             FROM logbook_shift_master lsm

#             LEFT JOIN LATERAL jsonb_array_elements(
#                 COALESCE(lsm.all_technicians, '[]'::jsonb)
#             ) AS tech(value) ON TRUE
#         )

#         SELECT
#             h.shift_id,
#             h.station_id,

#             h.handover_by,
#             h.takeover_by,

#             h.start_time,
#             h.end_time,

#             t.technician_id,
#             CONCAT(u.first_name, ' ', u.last_name) AS technician_name

#         FROM handovers h

#         LEFT JOIN technicians t
#             ON (
#                 -- 🔥 Overlapping condition
#                 t.tech_from::timestamp <= COALESCE(h.end_time, NOW())
#                 AND (
#                     t.tech_to IS NULL
#                     OR t.tech_to::timestamp >= h.start_time
#                 )
#             )

#         LEFT JOIN users u
#             ON u.user_id = t.technician_id

#         ORDER BY h.start_time;
#     """)

#     rows = db.execute(query, {
#         "station_id": station_id,
#         "from_date": from_date,
#         "to_date": to_date
#     }).mappings().all()

#     # -------------------------------
#     # GROUP INTO TABLE FORMAT
#     # -------------------------------
#     result = []
#     temp_map = {}

#     for row in rows:
#         key = (row["shift_id"], row["start_time"])

#         if key not in temp_map:
#             temp_map[key] = {
#                 "shift_id": row["shift_id"],
#                 "station_id": row["station_id"],
#                 "handover_by": row["handover_by"],
#                 "takeover_by": row["takeover_by"],
#                 "start_time": row["start_time"],
#                 "end_time": row["end_time"],
#                 "technicians": []
#             }

#         if row["technician_id"]:
#             temp_map[key]["technicians"].append({
#                 "technician_id": row["technician_id"],
#                 "technician_name": row["technician_name"]
#             })

#     result = list(temp_map.values())

#     return {
#         "station_id": station_id,
#         "from_date": str(from_date),
#         "to_date": str(to_date),
#         "total_records": len(result),
#         "data": result
#     }



# @router.get("/shift-incharge-timeline")
# def get_shift_incharge_timeline(
#     station_id: int = Query(...),
#     from_date: date = Query(...),
#     to_date: date = Query(...),
#     db: Session = Depends(get_db)
# ):
#     if from_date > to_date:
#         raise HTTPException(status_code=400, detail="Invalid date range")

#     # ------------------------------------
#     # 1️⃣ FETCH HANDOVER EVENTS
#     # ------------------------------------
#     handover_query = text("""
#         SELECT
#             shl.shift_id,
#             shl.station_id,
#             shl.event_type,
#             shl.from_user_id,
#             shl.to_user_id,
#             shl.event_time,

#             CONCAT(u1.first_name,' ',u1.last_name) AS from_user_name,
#             CONCAT(u2.first_name,' ',u2.last_name) AS to_user_name

#         FROM shift_handover_log shl
#         LEFT JOIN users u1 ON u1.user_id = shl.from_user_id
#         LEFT JOIN users u2 ON u2.user_id = shl.to_user_id

#         WHERE shl.station_id = :station_id
#         AND shl.event_time >= :from_date
#         AND shl.event_time < (:to_date + INTERVAL '1 day')

#         ORDER BY shl.shift_id, shl.event_time
#     """)

#     events = db.execute(handover_query, {
#         "station_id": station_id,
#         "from_date": from_date,
#         "to_date": to_date
#     }).mappings().all()

#     # ------------------------------------
#     # 2️⃣ BUILD TIMELINE
#     # ------------------------------------
#     timeline = []

#     for i, event in enumerate(events):

#         if event["event_type"] != "HANDOVER_ACCEPTED":
#             continue

#         start_time = event["event_time"]
#         end_time = None

#         for j in range(i + 1, len(events)):
#             next_event = events[j]

#             if (
#                 next_event["shift_id"] == event["shift_id"]
#                 and next_event["event_type"] == "HANDOVER_REQUESTED"
#             ):
#                 end_time = next_event["event_time"]
#                 break

#         timeline.append({
#             "shift_id": event["shift_id"],
#             "station_id": event["station_id"],

#             "shift_incharge_id": event["to_user_id"],
#             "shift_incharge_name": event["to_user_name"],

#             "handover_by": event["from_user_name"],
#             "handover_to": event["to_user_name"],

#             "start_time": start_time,
#             "end_time": end_time
#         })

#     # ------------------------------------
#     # 3️⃣ FETCH TECHNICIANS (JSONB)
#     # ------------------------------------
#     tech_query = text("""
#         SELECT
#             lsm.created_at,

#             (tech.value->>'technician_id')::int AS technician_id,
#             (tech.value->>'created_by')::int AS created_by,
#             (tech.value->>'from_date')::timestamp AS from_date,
#             (tech.value->>'to_date')::timestamp AS to_date

#         FROM logbook_shift_master lsm

#         LEFT JOIN LATERAL jsonb_array_elements(
#             COALESCE(lsm.all_technicians, '[]'::jsonb)
#         ) AS tech(value) ON TRUE
#     """)

#     tech_rows = db.execute(tech_query).mappings().all()

#     # ------------------------------------
#     # 4️⃣ MAP TECHNICIANS TO SHIFT INCHARGE
#     # ------------------------------------
#     result = []

#     for row in timeline:

#         start = row["start_time"]
#         end = row["end_time"]
#         incharge_id = row["shift_incharge_id"]

#         # normalize timezone
#         if start and start.tzinfo:
#             start = start.replace(tzinfo=None)

#         if end and end.tzinfo:
#             end = end.replace(tzinfo=None)

#         technicians = []

#         for tech in tech_rows:

#             if tech["technician_id"] is None:
#                 continue

#             # ✅ IMPORTANT FILTER
#             if tech["created_by"] != incharge_id:
#                 continue

#             t_start = tech["from_date"]
#             t_end = tech["to_date"]

#             if t_start and t_start.tzinfo:
#                 t_start = t_start.replace(tzinfo=None)

#             if t_end and t_end.tzinfo:
#                 t_end = t_end.replace(tzinfo=None)

#             # ------------------------------------
#             # 🔥 TIME MATCH LOGIC
#             # ------------------------------------
#             overlap = False

#             if end:
#                 if t_end:
#                     overlap = (t_start <= end and t_end >= start)
#                 else:
#                     overlap = (t_start <= end)
#             else:
#                 if t_end:
#                     overlap = (t_end >= start)
#                 else:
#                     overlap = True

#             if overlap:
#                 technicians.append({
#                     "technician_id": tech["technician_id"],
#                     "from_time": str(t_start) if t_start else None,
#                     "to_time": str(t_end) if t_end else None
#                 })

#         row["technicians"] = technicians
#         row["technician_count"] = len(technicians)

#         result.append(row)

#     # ------------------------------------
#     # 5️⃣ FINAL RESPONSE
#     # ------------------------------------
#     return {
#         "station_id": station_id,
#         "from_date": str(from_date),
#         "to_date": str(to_date),
#         "total_records": len(result),
#         "data": result
#     }


@router.get("/shift-incharge-timeline")
def get_shift_incharge_timeline(
    station_id: int = Query(...),
    from_date: date = Query(...),
    to_date: date = Query(...),
    db: Session = Depends(get_db)
):
    if from_date > to_date:
        raise HTTPException(status_code=400, detail="Invalid date range")

    # ------------------------------------
    # 1️⃣ FETCH HANDOVER EVENTS
    # ------------------------------------
    handover_query = text("""
        SELECT
            shl.shift_id,
            shl.station_id,
            shl.event_type,
            shl.from_user_id,
            shl.to_user_id,
            shl.event_time,

            CONCAT(u1.first_name,' ',u1.last_name) AS from_user_name,
            CONCAT(u2.first_name,' ',u2.last_name) AS to_user_name

        FROM shift_handover_log shl
        LEFT JOIN users u1 ON u1.user_id = shl.from_user_id
        LEFT JOIN users u2 ON u2.user_id = shl.to_user_id

        WHERE shl.station_id = :station_id
        AND shl.event_time >= :from_date
        AND shl.event_time < (:to_date + INTERVAL '1 day')

        ORDER BY shl.shift_id, shl.event_time
    """)

    events = db.execute(handover_query, {
        "station_id": station_id,
        "from_date": from_date,
        "to_date": to_date
    }).mappings().all()

    # ------------------------------------
    # 2️⃣ BUILD TIMELINE
    # ------------------------------------
    timeline = []

    for i, event in enumerate(events):

        if event["event_type"] != "HANDOVER_ACCEPTED":
            continue

        start_time = event["event_time"]
        end_time = None

        for j in range(i + 1, len(events)):
            next_event = events[j]

            if (
                next_event["shift_id"] == event["shift_id"]
                and next_event["event_type"] == "HANDOVER_REQUESTED"
            ):
                end_time = next_event["event_time"]
                break

        timeline.append({
            "shift_id": event["shift_id"],
            "station_id": event["station_id"],

            "shift_incharge_id": event["to_user_id"],
            "shift_incharge_name": event["to_user_name"],

            "handover_by": event["from_user_name"],
            "handover_to": event["to_user_name"],

            "start_time": event["event_time"],
            "end_time": end_time
        })

    # ------------------------------------
    # 3️⃣ FETCH TECHNICIANS WITH NAME
    # ------------------------------------
    tech_query = text("""
        SELECT
            (tech.value->>'technician_id')::int AS technician_id,
            (tech.value->>'created_by')::int AS created_by,
            (tech.value->>'from_date')::timestamp AS from_date,
            (tech.value->>'to_date')::timestamp AS to_date,

            CONCAT(u.first_name, ' ', u.last_name) AS technician_name

        FROM logbook_shift_master lsm

        LEFT JOIN LATERAL jsonb_array_elements(
            COALESCE(lsm.all_technicians, '[]'::jsonb)
        ) AS tech(value) ON TRUE

        LEFT JOIN users u
            ON u.user_id = (tech.value->>'technician_id')::int
    """)

    tech_rows = db.execute(tech_query).mappings().all()

    # ------------------------------------
    # 4️⃣ MAP TECHNICIANS
    # ------------------------------------
    result = []

    for row in timeline:

        start = row["start_time"]
        end = row["end_time"]
        incharge_id = row["shift_incharge_id"]

        # normalize timezone
        if start and start.tzinfo:
            start = start.replace(tzinfo=None)

        if end and end.tzinfo:
            end = end.replace(tzinfo=None)

        technicians = []
        seen = set()

        for tech in tech_rows:

            if not tech["technician_id"]:
                continue

            # match shift incharge
            if tech["created_by"] != incharge_id:
                continue

            t_start = tech["from_date"]
            t_end = tech["to_date"]

            if t_start and t_start.tzinfo:
                t_start = t_start.replace(tzinfo=None)

            if t_end and t_end.tzinfo:
                t_end = t_end.replace(tzinfo=None)

            # include logic
            if end:
                include = start <= t_start <= end
            else:
                include = t_start >= start

            if include:
                key = (tech["technician_id"], t_start)

                if key not in seen:
                    seen.add(key)

                    technicians.append({
                        "technician_id": tech["technician_id"],
                        "technician_name": tech["technician_name"],  # ✅ added
                        "from_time": str(t_start) if t_start else None,
                        "to_time": str(t_end) if t_end else None
                    })

        row["technicians"] = technicians
        row["technician_count"] = len(technicians)

        result.append(row)

    # ------------------------------------
    # 5️⃣ FINAL RESPONSE
    # ------------------------------------
    return {
        "station_id": station_id,
        "from_date": str(from_date),
        "to_date": str(to_date),
        "total_records": len(result),
        "data": result
    }


class ShiftCreateSchema(BaseModel):
    shift_name: str
    start_time: time
    end_time: time
class ShiftUpdateSchema(BaseModel):
    shift_name: Optional[str] = None
    start_time: time = None
    end_time: time = None
class ShiftResponseSchema(BaseModel):
    shift_id: int
    shift_name: str
    start_time: time
    end_time: time
    model_config = {
        "from_attributes": True
    }

@router.get("/review-digital-logs")
def get_review_logs(
    user_id: int,
    db: Session = Depends(get_db)
):

    # ✅ 1. Get user + station_name
    user = db.execute(
        text("""
            SELECT u.user_id, s.station_name
            FROM users u
            LEFT JOIN station s 
                ON s.station_id = u.station_id
            WHERE u.user_id = :user_id
        """),
        {"user_id": user_id}
    ).fetchone()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # ✅ 2. Get role_id
    role_data = db.execute(
        text("""
            SELECT role_id
            FROM role_permissions
            WHERE user_id = :user_id
            LIMIT 1
        """),
        {"user_id": user_id}
    ).fetchone()

    if not role_data:
        raise HTTPException(status_code=404, detail="Role not assigned")

    role_id = role_data.role_id
    ADMIN_ROLE_ID = 4

    # ✅ 3. Base query
    query = """
        SELECT 
            rdl.id,
            rdl.date,
            rdl.station,
            rdl.acknowledge_id,
            rdl.acknowledge_date,
            rdl.is_acknowledged,
            rdl.acknowledged_by,
            TRIM(
                COALESCE(u.first_name, '') || ' ' || COALESCE(u.last_name, '')
            ) AS acknowledged_by_name
        FROM review_digital_logs rdl        
        LEFT JOIN users u 
            ON u.user_id = rdl.acknowledged_by
    """

    params = {}

    # ✅ 4. Apply filter only for non-admin
    if role_id != ADMIN_ROLE_ID:
        if not user.station_name:
            raise HTTPException(status_code=400, detail="User station not mapped")

        query += " WHERE rdl.station = :station"
        params["station"] = user.station_name

    query += " ORDER BY rdl.date DESC, rdl.station"

    # ✅ 5. Execute
    result = db.execute(text(query), params).fetchall()

    # ✅ 6. Response
    response = []
    for row in result:
        response.append({
            "id": row.id,
            "date": str(row.date),
            "station": row.station,
            "acknowledge_id": row.acknowledge_id,
            "acknowledge_date": str(row.acknowledge_date) if row.acknowledge_date else None,
            "is_acknowledged": row.is_acknowledged,
            "acknowledged_by": row.acknowledged_by,
            "acknowledged_by_name": row.acknowledged_by_name or "-"
        })

    return response

@router.get(
    "/handover-log",
    summary="Get all station shift incharge records"
)


def get_all_station_shift_incharge(db=Depends(get_db)):
    print("DEBUG: Fetching all station_shift_incharge records")

    query = text("""
        SELECT
            id,
            station_id,
            shift_id,
            user_id,
            responsibility_from,
            responsibility_to,
            handover_requested_at,
            handover_accepted_at,
            handover_to_user_id,
            comment_for_next_incharge,
            created_at
        FROM station_shift_incharge
        ORDER BY id DESC
    """)

    rows = db.execute(query).mappings().all()

    print(f"DEBUG: Rows fetched = {len(rows)}")

    return {
        "status": "success",
        "count": len(rows),
        "data": rows
    }

@router.post(
    "/",
    response_model=ShiftResponseSchema,
    summary="Create shift"
)
def create_shift(
    payload: ShiftCreateSchema,
    db=Depends(get_db)
):
    query = text("""
        INSERT INTO shift (shift_name, start_time, end_time)
        VALUES (:shift_name, :start_time, :end_time)
        RETURNING *
    """)

    result = db.execute(query, payload.model_dump())
    db.commit()
    return result.mappings().first()
@router.get(
    "/",
    response_model=list[ShiftResponseSchema],
    summary="Get all shifts"
)
def get_all_shifts(db=Depends(get_db)):
    query = text("""
        SELECT *
        FROM shift
        ORDER BY shift_id
    """)

    return db.execute(query).mappings().all()
@router.get(
    "/{shift_id}",
    response_model=ShiftResponseSchema,
    summary="Get shift by ID"
)
def get_shift_by_id(
    shift_id: int,
    db=Depends(get_db)
):
    query = text("""
        SELECT *
        FROM shift
        WHERE shift_id = :shift_id
    """)

    row = db.execute(query, {"shift_id": shift_id}).mappings().first()

    if not row:
        raise HTTPException(404, "Shift not found")

    return row
@router.put(
    "/{shift_id}",
    response_model=ShiftResponseSchema,
    summary="Update shift"
)
def update_shift(
    shift_id: int,
    payload: ShiftUpdateSchema,
    db=Depends(get_db)
):
    fields = []
    params = {"shift_id": shift_id}

    for k, v in payload.model_dump(exclude_unset=True).items():
        fields.append(f"{k} = :{k}")
        params[k] = v

    if not fields:
        raise HTTPException(400, "No fields to update")

    query = text(f"""
        UPDATE shift
        SET {", ".join(fields)}
        WHERE shift_id = :shift_id
        RETURNING *
    """)

    row = db.execute(query, params).mappings().first()
    db.commit()

    if not row:
        raise HTTPException(404, "Shift not found")

    return row
@router.delete(
    "/{shift_id}",
    summary="Delete shift"
)
def delete_shift(
    shift_id: int,
    db=Depends(get_db)
):
    query = text("""
        DELETE FROM shift
        WHERE shift_id = :shift_id
        RETURNING shift_id
    """)

    row = db.execute(query, {"shift_id": shift_id}).first()
    db.commit()

    if not row:
        raise HTTPException(404, "Shift not found")

    return {"status": "success", "message": "Shift deleted"}



# =====================================================
# ✅ SHIFT HANDOVER LOG — UPDATE
# =====================================================

class ShiftHandoverLogPatch(BaseModel):
    remarks: Optional[str] = None
    is_acknowledge: Optional[bool] = None


@router.patch(
    "/shift-handover-log/{shift_id}",
    summary="Acknowledge shift handover log"
)
def patch_shift_handover_log(
    shift_id: int,
    payload: ShiftHandoverLogPatch,
    db=Depends(get_db),
    token: str = Query(..., description="Access token")  # ← ADDED
):
    result = db.execute(
        text("""
            UPDATE shift_handover_log
            SET
                remarks = :remarks,
                is_acknowledge = :is_acknowledge
            WHERE shift_id = :shift_id
        """),
        {
            "remarks": payload.remarks,
            "is_acknowledge": payload.is_acknowledge,
            "shift_id": shift_id
        }
    )
    db.commit()

    if result.rowcount == 0:
        raise HTTPException(status_code=404, detail="Shift handover log not found")

    return {"message": "Shift handover log updated successfully"}



# def get_previous_business_date():
#     now = datetime.now()

#     # Your rule: after 6 AM → insert previous day
#     if now.hour < 6:
#         return None  # prevent early execution

#     return (now - timedelta(days=1)).date()


# @router.post("/review-digital-logs/generate")
# def generate_review_log(db: Session = Depends(get_db)):

#     business_date = get_previous_business_date()

#     if not business_date:
#         return {"message": "Too early to generate"}

#     # ✅ Get all stations
#     stations = db.execute(
#         text("SELECT station_name FROM station")
#     ).fetchall()

#     if not stations:
#         return {"message": "No stations found"}

#     inserted_count = 0

#     for station in stations:

#         # ✅ Check if already exists (date + station)
#         exists = db.execute(
#             text("""
#                 SELECT 1 FROM review_digital_logs
#                 WHERE date = :date AND station = :station
#             """),
#             {"date": business_date, "station": station.station_name}
#         ).fetchone()

#         if exists:
#             continue

#         # ✅ Insert per station
#         db.execute(
#             text("""
#                 INSERT INTO review_digital_logs (date, station, is_acknowledged)
#                 VALUES (:date, :station, false)
#             """),
#             {"date": business_date, "station": station.station_name}
#         )

#         inserted_count += 1

#     db.commit()

#     return {
#         "message": "Review logs generated",
#         "date": str(business_date),
#         "rows_inserted": inserted_count
#     }


scheduler = BackgroundScheduler()


def scheduled_generate_review_log():
    db = SessionLocal()
    try:
        generate_review_log_internal(db)
        print("✅ Review logs generated automatically")
    except Exception as e:
        db.rollback()
        print("❌ Error:", str(e))
    finally:
        db.close()


def start_scheduler():
    scheduler.add_job(
        scheduled_generate_review_log,
        trigger='cron',
        hour=6,
        minute=5
    )
    scheduler.start()

def generate_review_log_internal(db):

    # ✅ Always generate previous day (since job runs after 6 AM)
    business_date = (datetime.now() - timedelta(days=1)).date()

    stations = db.execute(
        text("SELECT station_name FROM station")
    ).fetchall()

    if not stations:
        return

    for station in stations:

        exists = db.execute(
            text("""
                SELECT 1 FROM review_digital_logs
                WHERE date = :date AND station = :station
            """),
            {"date": business_date, "station": station.station_name}
        ).fetchone()

        if exists:
            continue

        db.execute(
            text("""
                INSERT INTO review_digital_logs (date, station, is_acknowledged)
                VALUES (:date, :station, false)
            """),
            {"date": business_date, "station": station.station_name}
        )

    db.commit()


TABLES = [
    "tank_10kl_ffe_master",
    "cp_reading_dkn_master",
    "cp_reading_hsn_master",
    "cp_reading_master",
    "cp_reading_mlr_master",
    "cp_reading_ner_master",
    "daily_safety_checklist",
    "daily_sampling_master",
    "dg_250kva_master",
    "erv_logbook_master",
    "fire_engine_test_master",
    "kptcl_dkn_master",
    "kptcl_hsn_master",
    "kptcl_ner_master",
    "dkn_digital_logbook",
    "hsn_digital_logbook",
    "mlr_digital_logbook",
    "ner_digital_logbook",
    "line_walker_master",
    "security_guard_report",
    "mfm_accounting_hsn",
    "mfm_accounting_dkn",
    "npt_report_master",
    "pressure_log_master",
    "tank_dip_memo",
    "vibration_temperature_entry_ner",
    "vibration_temperature_master_mlr",
    "vibration_temperature_master_ner",
    "mfm_log_hsn_master",
    "mfm_log_hsn2_master",
    "mfm_log_master_dkn",
    "mfm_log_mlr_master",
    "mfm_log_mlr_master_two",
    "mfm_log_ner_master",
    "mfm_log_ner_page2_master",
    "mfm_plt_detail_dkn",
    "product_dispatch_category_master"
]

# def generate_ack_id():
#     return "ACK-" + uuid.uuid4().hex[:8].upper()

# @router.put("/review-digital-logs/acknowledge/{log_date}")
# def acknowledge_log(
#     log_date: str,
#     user_id: int,
#     station_name: str,
#     db: Session = Depends(get_db)
# ):

#     ack_id = generate_ack_id()

#     # Convert to datetime
#     log_date_dt = datetime.strptime(log_date, "%Y-%m-%d")

#     start_time = log_date_dt.replace(hour=7, minute=0, second=0)
#     end_time = (log_date_dt + timedelta(days=1)).replace(hour=6, minute=0, second=0)

#     # ✅ 1. Update main table
#     result = db.execute(
#         text("""
#             UPDATE review_digital_logs
#             SET 
#                 is_acknowledged = TRUE,
#                 acknowledge_date = NOW(),
#                 acknowledged_by = :user_id,
#                 acknowledge_id = :ack_id,
#                 updated_at = NOW()
#             WHERE date = :date 
#             AND station = :station_name
#             AND is_acknowledged = FALSE
#             RETURNING id
#         """),
#         {"date": log_date,"station_name": station_name, "user_id": user_id, "ack_id": ack_id}
#     ).fetchone()

#     if not result:
#         raise HTTPException(status_code=404, detail="Already acknowledged or not found")

#     # ✅ 2. Update ALL master tables
#     for table in TABLES:
#         db.execute(
#             text(f"""
#                 UPDATE {table}
#                 SET 
#                     acknowledge_id = :ack_id,
#                     acknowledge_date = NOW(),
#                     acknowledge_by = :user_id
#                 WHERE created_at >= :start_time
#                 AND created_at <= :end_time
#                 AND station = :station_name OR station_name = :station_name
#             """),
#             {
#                 "ack_id": ack_id,
#                 "user_id": user_id,
#                 "start_time": start_time,
#                 "end_time": end_time,
#                 "station_name": station_name
#             }
#         )

#     db.commit()

#     return {
#         "message": "Acknowledged successfully",
#         "acknowledge_id": ack_id,
#         "station": station_name
#     }
  
    

def generate_ack_id():
    return "ACK-" + uuid.uuid4().hex[:8].upper()


def get_station_columns(db, table):
    result = db.execute(
        text("""
            SELECT column_name
            FROM information_schema.columns
            WHERE table_name = :table
            AND column_name IN ('station', 'station_name')
        """),
        {"table": table}
    ).fetchall()

    return [row[0] for row in result]


@router.put("/review-digital-logs/acknowledge/{log_date}")
def acknowledge_log(
    log_date: str,
    user_id: int,
    station_name: str,
    db: Session = Depends(get_db)
):

    ack_id = generate_ack_id()

    # ✅ Date parsing
    try:
        log_date_dt = datetime.strptime(log_date, "%Y-%m-%d")
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format")

    start_time = log_date_dt.replace(hour=7, minute=0, second=0)
    end_time = (log_date_dt + timedelta(days=1)).replace(hour=6, minute=0, second=0)

    # ✅ 1. Update main table
    result = db.execute(
        text("""
            UPDATE review_digital_logs
            SET 
                is_acknowledged = TRUE,
                acknowledge_date = NOW(),
                acknowledged_by = :user_id,
                acknowledge_id = :ack_id,
                updated_at = NOW()
            WHERE date = :date 
            AND station = :station_name
            AND is_acknowledged = FALSE
            RETURNING id
        """),
        {
            "date": log_date,
            "station_name": station_name,
            "user_id": user_id,
            "ack_id": ack_id
        }
    ).fetchone()

    if not result:
        raise HTTPException(status_code=404, detail="Already acknowledged or not found")

    # ✅ 2. Update ALL master tables (SAFE)
    for table in TABLES:

        cols = get_station_columns(db, table)

        if not cols:
            continue  # skip tables without station column

        # Build condition safely
        conditions = []
        if "station" in cols:
            conditions.append("station = :station_name")
        if "station_name" in cols:
            conditions.append("station_name = :station_name")

        station_condition = " OR ".join(conditions)

        db.execute(
            text(f"""
                UPDATE {table}
                SET 
                    acknowledge_id = :ack_id,
                    acknowledge_date = NOW(),
                    acknowledge_by = :user_id
                WHERE created_at BETWEEN :start_time AND :end_time
                AND ({station_condition})
            """),
            {
                "ack_id": ack_id,
                "user_id": user_id,
                "start_time": start_time,
                "end_time": end_time,
                "station_name": station_name
            }
        )

    db.commit()

    return {
        "message": "Acknowledged successfully",
        "acknowledge_id": ack_id,
        "station": station_name
    }