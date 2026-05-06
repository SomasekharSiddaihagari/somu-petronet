import asyncio
from datetime import date, datetime
import json
import os
import shutil
from typing import Literal, Optional, Union

from fastapi import (
    APIRouter, BackgroundTasks, Depends, UploadFile, File as FastAPIFile,
    Form, HTTPException, Query
)
 
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
 

from sqlalchemy.orm import Session
from sqlalchemy import text

from app.crud.leave.leave_notifications_crud import notify_supervisor_on_apply
from app.database import get_db
from app.schemas.leave.leave_schema import LeaveApplicationCreate, LeaveApplicationDayCreate, LeaveSummaryResponse
from app.utils.UserAuthUtils import verify_access_token  # token check

from fastapi import APIRouter, Form, File, UploadFile, Depends
from typing import Optional, Union
from sqlalchemy.orm import Session
from datetime import date, datetime
from sqlalchemy import text
import os
import shutil
router = APIRouter(
    prefix="/api/leave",
    tags=["Leave Apply"]
)




UPLOAD_DIR = "files/leave_files"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post("/apply")
def apply_leave(
    user_id: int = Form(...),

    supervisor_id: Optional[int] = Form(None),
    supervisor_name: Optional[str] = Form(None),
    user_name: Optional[str] = Form(None),
    supervisor_remarks: Optional[str] = Form(None),

    leave_type: Optional[str] = Form(None),

    from_date: Optional[date] = Form(None),
    to_date: Optional[date] = Form(None),
    number_of_days: Optional[float] = Form(None),

    reason: Optional[str] = Form(None),

    contact_address: Optional[str] = Form(None),
    phone_number: Optional[str] = Form(None),

    reversal_from_date: Optional[date] = Form(None),
    reversal_to_date: Optional[date] = Form(None),
    reversal_remarks: Optional[str] = Form(None),
    leave_nature: Optional[str] = Form(None),

    status: Optional[str] = Form(None),

    document: Union[UploadFile, str, None] = File(None),
    db: Session = Depends(get_db),
    background_tasks: BackgroundTasks = None
    ):
    try:
        # ------------------------------------------------
        # FILE HANDLING
        # ------------------------------------------------
        document_path = None

        if document and hasattr(document, "file") and document.filename:
            os.makedirs(UPLOAD_DIR, exist_ok=True)

            file_ext = document.filename.split(".")[-1]
            saved_filename = f"leave_{user_id}_{int(datetime.now().timestamp())}.{file_ext}"
            file_path = os.path.join(UPLOAD_DIR, saved_filename)

            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(document.file, buffer)

            document_path = file_path

        # ------------------------------------------------
        # SQL PAYLOAD
        # ------------------------------------------------
        payload = {
            "user_id": user_id,
            "supervisor_id": supervisor_id,
            "supervisor_name": supervisor_name,
            "user_name": user_name,
            "supervisor_remarks": supervisor_remarks,
            "leave_type": leave_type,
            "from_date": from_date,
            "to_date": to_date,
            "number_of_days": number_of_days,
            "reason": reason,
            "document_path": document_path,
            "contact_address": contact_address,
            "phone_number": phone_number,
            "reversal_from_date": reversal_from_date,
            "reversal_to_date": reversal_to_date,
            "reversal_remarks": reversal_remarks,
            "leave_nature": leave_nature,
            "status": status or "PENDING"
        }

        # ------------------------------------------------
        # INSERT QUERY
        # ------------------------------------------------
        query = text("""
            INSERT INTO hr_leave_application (
                user_id,
                supervisor_id,
                supervisor_name,
                user_name,
                supervisor_remarks,
                leave_type,
                from_date,
                to_date,
                number_of_days,
                reason,
                document_path,
                contact_address,
                phone_number,
                reversal_from_date,
                reversal_to_date,
                reversal_remarks,
                leave_nature,
                status
            )
            VALUES (
                :user_id,
                :supervisor_id,
                :supervisor_name,
                :user_name,
                :supervisor_remarks,
                :leave_type,
                :from_date,
                :to_date,
                :number_of_days,
                :reason,
                :document_path,
                :contact_address,
                :phone_number,
                :reversal_from_date,
                :reversal_to_date,
                :reversal_remarks,
                :leave_nature,
                :status
            )
            RETURNING leave_id
        """)

        result = db.execute(query, payload)
        leave_id = result.scalar()
        db.commit()

        # ------------------------------------------------
        # BACKGROUND TASK
        # ------------------------------------------------
        if background_tasks:
            background_tasks.add_task(
                notify_supervisor_on_apply,
                db,
                payload,
                background_tasks
            )

        return {
            "status": True,
            "message": "Leave application created successfully",
            "leave_id": leave_id
        }

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


# ADD INDIVIDUAL LEAVE DAY
# ----------------------------------------------
@router.post("/add")
def add_leave_day(payload: LeaveApplicationDayCreate, db: Session = Depends(get_db)):

    query = text("""
        SELECT insert_leave_application_day(
            :leave_application_id,
            :leave_date,
            :day_type,
            :half_session
        )
    """)

    result = db.execute(query, payload.model_dump())

    leave_day_id = result.scalar()
    db.commit()   # VERY IMPORTANT


    return {
        "status": True,
        "message": "Leave day added successfully",
        "leave_day_id": leave_day_id
    }



def get_el_summary_components(db: Session, user_id: int):
    """
    Returns allocated, used, encashed, balance for EL
    """

    allocated = db.execute(text("""
        SELECT COALESCE(SUM(lb.allocated), 0)
        FROM leave_balances lb
        JOIN leave_types lt ON lt.type_id = lb.type_id
        WHERE lb.user_id = :uid
          AND LOWER(lt.code) IN ('el_e', 'el_ne')
          AND lb.is_usable = TRUE
    """), {"uid": user_id}).scalar() or 0

    used = db.execute(text("""
        SELECT COALESCE(SUM(number_of_days), 0)
        FROM hr_leave_application
        WHERE user_id = :uid
          AND LOWER(leave_type) IN (
              'el', 'el_e', 'el_ne', 'earned leave', 'earned_leave'
          )
          AND LOWER(status) IN (
              'approved',
              'reversal approved',
              'withdraw rejected'
          )
    """), {"uid": user_id}).scalar() or 0

    encashed = db.execute(text("""
        SELECT COALESCE(SUM(le.encash_el), 0)
        FROM leave_encashment le
        LEFT JOIN encashment_main em
               ON em.encashment_main_id = le.encashment_main_id
        WHERE LOWER(le.status) NOT IN ('supervisor rejected','rejected', 'cancelled')
          AND (
                le.created_by = :uid
             OR em.created_by = :uid
          )
    """), {"uid": user_id}).scalar() or 0

    balance = max(allocated - used - encashed, 0)

    return allocated, used, encashed, balance

@router.put("/self-cancel/{leave_id}")
def self_cancel_leave(
    leave_id: int,
    user_id: int,
    db: Session = Depends(get_db)
):
    """
    Allows an employee to cancel their own leave request if it is still PENDING.
    """
    try:
        # 1. Fetch the application
        query = text("""
            SELECT leave_id, user_id, status, leave_type
            FROM hr_leave_application
            WHERE leave_id = :leave_id
        """)
        application = db.execute(query, {"leave_id": leave_id}).mappings().first()
 
        if not application:
            raise HTTPException(status_code=404, detail="Leave application not found")
 
        # 2. Verify ownership
        if application["user_id"] != user_id:
            raise HTTPException(
                status_code=403,
                detail="You can only cancel your own leave applications"
            )
 
        # 3. Verify status (Only allow canceling PENDING, APPLIED, or SUBMITTED)
        current_status = (application["status"] or "").upper()
        allowed_statuses = ["PENDING", "APPLIED", "SUBMITTED"]
 
        if current_status not in allowed_statuses:
            raise HTTPException(
                status_code=400,
                detail=f"Cannot cancel leave with status '{current_status}'. Only pending requests can be cancelled."
            )
 
        # 4. Handle Comp-Off release if necessary
        if (application["leave_type"] or "").lower() == "comp_off":
            from app.crud.leave.hr_comp_off_crud import reset_comp_off_on_reversal
            reset_comp_off_on_reversal(db, leave_id, user_id)
 
        # 5. Update Status
        update_query = text("""
            UPDATE hr_leave_application
            SET status = 'SELF_CANCELLED'
            WHERE leave_id = :leave_id
        """)
        db.execute(update_query, {"leave_id": leave_id})
        db.commit()
 
        return {
            "status": True,
            "message": "Leave application cancelled successfully"
        }
 
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
 
 
def get_el_summary_components(db: Session, user_id: int):
    """
    Returns allocated, used, encashed, balance for EL
    """
 
    allocated = db.execute(text("""
        SELECT COALESCE(SUM(lb.allocated), 0)
        FROM leave_balances lb
        JOIN leave_types lt ON lt.type_id = lb.type_id
        WHERE lb.user_id = :uid
          AND LOWER(lt.code) IN ('el_e', 'el_ne')
          AND lb.is_usable = TRUE
    """), {"uid": user_id}).scalar() or 0
 
    used = db.execute(text("""
        SELECT COALESCE(SUM(number_of_days), 0)
        FROM hr_leave_application
        WHERE user_id = :uid
          AND LOWER(leave_type) IN (
              'el', 'el_e', 'el_ne', 'earned leave', 'earned_leave'
          )
          AND LOWER(status) IN (
              'approved',
              'reversal approved',
              'withdraw rejected'
          )
    """), {"uid": user_id}).scalar() or 0
 
    encashed = db.execute(text("""
        SELECT COALESCE(SUM(le.encash_el), 0)
        FROM leave_encashment le
        LEFT JOIN encashment_main em
               ON em.encashment_main_id = le.encashment_main_id
        WHERE LOWER(le.status) NOT IN ('supervisor rejected','rejected', 'cancelled')
          AND (
                le.created_by = :uid
             OR em.created_by = :uid
          )
    """), {"uid": user_id}).scalar() or 0
 
    balance = max(allocated - used - encashed, 0)
 
    return allocated, used, encashed, balance


# @router.get("/summary/{user_id}")
# def get_leave_summary(user_id: int, db: Session = Depends(get_db)):

#     # ------------------------------------------------------------
#     # 1. Fetch allocated leave balances
#     # ------------------------------------------------------------
#     balances = db.execute(
#         text("""
#             SELECT 
#                 lb.type_id,
#                 lt.name AS leave_type_name,
#                 lt.code AS leave_code,
#                 SUM(lb.allocated) AS allocated
#             FROM leave_balances lb
#             JOIN leave_types lt ON lt.type_id = lb.type_id
#             WHERE lb.user_id = :uid
#               AND lb.is_usable = TRUE
#             GROUP BY lb.type_id, lt.name, lt.code
#         """),
#         {"uid": user_id}
#     ).mappings().all()

#     if not balances:
#         return {
#             "leaves": [],
#             "summary": {
#                 "total_allocated": 0,
#                 "total_taken": 0,
#                 "total_pending": 0
#             }
#         }

#     # ------------------------------------------------------------
#     # 2. Fetch applied leaves
#     # ------------------------------------------------------------
#     applied_rows = db.execute(text("""
#         SELECT 
#             LOWER(leave_type) AS leave_type,
#             SUM(number_of_days) AS days
#         FROM hr_leave_application
#         WHERE user_id = :uid
#           AND LOWER(status) IN (
#               'approved',
#               'pending',
#               'applied',
#               'submitted',
#               'reversal approved',
#               'reversal pending',
#               'reversal rejected',
#               'withdraw pending',
#               'withdraw rejected'
#           )
#         GROUP BY LOWER(leave_type)
#     """), {"uid": user_id}).mappings().all()

#     applied_map = {
#         row["leave_type"]: float(row["days"] or 0)
#         for row in applied_rows
#     }

#     # ------------------------------------------------------------
#     # 3. Fetch encashable rules
#     # ------------------------------------------------------------
#     rules = db.execute(text("""
#         SELECT 
#             leave_type_id,
#             COALESCE((special_rules->>'encashable')::BOOLEAN, FALSE) AS encashable
#         FROM leave_allocation_rules
#     """)).mappings().all()

#     encashable_map = {
#         r["leave_type_id"]: r["encashable"]
#         for r in rules
#     }

#     # ------------------------------------------------------------
#     # 4. Merge leave balances (EL handled later)
#     # ------------------------------------------------------------
#     merged = {}
#     total_allocated = 0

#     for row in balances:

#         raw_name = row["leave_type_name"]
#         leave_code = (row["leave_code"] or "").lower()
#         allocated = float(row["allocated"] or 0)

#         is_el = "earned leave" in raw_name.lower()
#         name = "Earned Leave" if is_el else raw_name

#         applied = applied_map.get(raw_name.lower(), 0)

#         balance = allocated - applied
#         is_encashable = encashable_map.get(row["type_id"], False)

#         if name not in merged:
#             merged[name] = {
#                 "leave_type_id": row["type_id"],
#                 "leave_type_name": name,
#                 "encashable": 0.0,
#                 "non_encashable": 0.0,
#                 "allocated": 0.0,
#                 "applied": 0.0,
#                 "balance": 0.0
#             }

#         merged[name]["allocated"] += allocated
#         merged[name]["applied"] += applied

#         if is_encashable:
#             merged[name]["encashable"] += balance
#         else:
#             merged[name]["non_encashable"] += balance

#         merged[name]["balance"] = (
#             merged[name]["allocated"] - merged[name]["applied"]
#         )

#         total_allocated += allocated

#     # ------------------------------------------------------------
#     # 5. OVERRIDE Earned Leave using authoritative EL logic
#     # ------------------------------------------------------------

#     if "Earned Leave" in merged:

#         alloc = db.execute(text("""
#             SELECT COALESCE(SUM(lb.allocated), 0)
#             FROM leave_balances lb
#             JOIN leave_types lt ON lt.type_id = lb.type_id
#             WHERE lb.user_id = :uid
#             AND LOWER(lt.code) IN ('el_e', 'el_ne')
#             AND lb.is_usable = TRUE
#         """), {"uid": user_id}).scalar() or 0

#         used = db.execute(text("""
#             SELECT COALESCE(SUM(number_of_days), 0)
#             FROM hr_leave_application
#             WHERE user_id = :uid
#             AND LOWER(leave_type) IN (
#                 'el', 'el_e', 'el_ne', 'earned leave', 'earned_leave'
#             )
#             AND LOWER(status) IN (
#                 'approved',
#                 'pending',
#                 'applied',
#                 'submitted',
#                 'reversal approved',
#                 'reversal pending',
#                 'withdraw pending',
#                 'withdraw rejected'
#             )
#         """), {"uid": user_id}).scalar() or 0


#         encashed = db.execute(text("""
#             SELECT COALESCE(SUM(le.encash_el), 0)
#             FROM leave_encashment le
#             LEFT JOIN encashment_main em
#                 ON em.encashment_main_id = le.encashment_main_id
#             WHERE LOWER(le.status) NOT IN ('supervisor rejected','rejected', 'cancelled')
#             AND (
#                     le.created_by = :uid
#                 OR em.created_by = :uid
#             )
#         """), {"uid": user_id}).scalar() or 0

#         # 🔥 FORCE FLOAT ONCE
#         alloc = float(alloc)
#         used = float(used)
#         encashed = float(encashed)

#         balance = max(alloc - used - encashed, 0.0)

#         el = merged["Earned Leave"]
#         el["allocated"] = alloc
#         el["applied"] = used
#         el["balance"] = balance

#         enc = min(float(el["encashable"]), balance)
#         non_enc = balance - enc

#         el["encashable"] = max(enc, 0.0)
#         el["non_encashable"] = max(non_enc, 0.0)


#     # ------------------------------------------------------------
#     # 6. Summary totals
#     # ------------------------------------------------------------
#     total_taken = db.execute(text("""
#         SELECT COALESCE(SUM(number_of_days), 0)
#         FROM hr_leave_application
#         WHERE user_id = :uid
#           AND LOWER(status) NOT IN ('withdraw approved', 'rejected', 'self_cancelled')
#     """), {"uid": user_id}).scalar()

#     total_pending = db.execute(text("""
#         SELECT COALESCE(SUM(number_of_days), 0)
#         FROM hr_leave_application
#         WHERE user_id = :uid
#           AND LOWER(status) IN (
#               'pending',
#               'applied',
#               'submitted',
#               'reversal pending',
#               'withdraw pending'
#           )
#     """), {"uid": user_id}).scalar()

#     # ------------------------------------------------------------
#     # 7. Final response
#     # ------------------------------------------------------------
#     return {
#         "leaves": list(merged.values()),
#         "summary": {
#             "total_allocated": float(total_allocated),
#             "total_taken": float(total_taken or 0),
#             "total_pending": float(total_pending or 0)
#         }
#     }



@router.get("/summary/{user_id}")
def get_leave_summary(user_id: int, db: Session = Depends(get_db)):

    # ------------------------------------------------------------
    # 1. Fetch allocated leave balances
    # ------------------------------------------------------------
    balances = db.execute(
        text("""
            SELECT 
                lb.type_id,
                lt.name AS leave_type_name,
                lt.code AS leave_code,
                SUM(lb.allocated) AS allocated
            FROM leave_balances lb
            JOIN leave_types lt ON lt.type_id = lb.type_id
            WHERE lb.user_id = :uid
              AND lb.is_usable = TRUE
            GROUP BY lb.type_id, lt.name, lt.code
        """),
        {"uid": user_id}
    ).mappings().all()

    if not balances:
        return {
            "leaves": [],
            "summary": {
                "total_allocated": 0,
                "total_taken": 0,
                "total_provisioned": 0,
                "total_pending": 0
            }
        }

    # ------------------------------------------------------------
    # 2. Fetch applied leaves → Taken + Provisioned (Fixed Logic)
    # ------------------------------------------------------------
    applied_rows = db.execute(text("""
        SELECT 
            LOWER(leave_type) AS leave_type,
            SUM(CASE 
                    WHEN LOWER(status) IN ('approved', 'reversal approved') 
                         AND from_date <= CURRENT_DATE 
                    THEN number_of_days 
                    ELSE 0 
                END) AS taken_days,
            SUM(CASE 
                    WHEN LOWER(status) NOT IN ('approved', 'reversal approved', 'rejected', 
                                              'withdraw approved', 'self_cancelled')
                    THEN number_of_days 
                    ELSE 0 
                END) AS provisioned_days
        FROM hr_leave_application
        WHERE user_id = :uid
        GROUP BY LOWER(leave_type)
    """), {"uid": user_id}).mappings().all()

    taken_map = {row["leave_type"]: float(row["taken_days"] or 0) for row in applied_rows}
    provision_map = {row["leave_type"]: float(row["provisioned_days"] or 0) for row in applied_rows}

    # ------------------------------------------------------------
    # 3. Fetch encashable rules
    # ------------------------------------------------------------
    rules = db.execute(text("""
        SELECT 
            leave_type_id,
            COALESCE((special_rules->>'encashable')::BOOLEAN, FALSE) AS encashable
        FROM leave_allocation_rules
    """)).mappings().all()

    encashable_map = {r["leave_type_id"]: r["encashable"] for r in rules}

    # ------------------------------------------------------------
    # 4. Merge leave balances
    # ------------------------------------------------------------
    merged = {}
    total_allocated = 0.0

    for row in balances:
        raw_name = row["leave_type_name"]
        allocated = float(row["allocated"] or 0)

        is_el = "earned leave" in raw_name.lower()
        name = "Earned Leave" if is_el else raw_name

        taken = taken_map.get(raw_name.lower(), 0.0)
        provisioned = provision_map.get(raw_name.lower(), 0.0)
        is_encashable = encashable_map.get(row["type_id"], False)  # ✅ was missing

        if name not in merged:
            merged[name] = {
                "leave_type_id": row["type_id"],
                "leave_type_name": name,
                "encashable": 0.0,
                "non_encashable": 0.0,
                "allocated": 0.0,
                "taken": 0.0,
                "provisioned": 0.0,
                "balance": 0.0
            }

        merged[name]["allocated"] += allocated
        merged[name]["taken"] += taken
        merged[name]["provisioned"] += provisioned
        merged[name]["balance"] = merged[name]["allocated"] - merged[name]["taken"]

        # ✅ Track encashable/non_encashable per row using the rules map
        row_balance = allocated - taken
        if is_encashable:
            merged[name]["encashable"] += row_balance
        else:
            merged[name]["non_encashable"] += row_balance

        total_allocated += allocated

    # ------------------------------------------------------------
    # 5. OVERRIDE Earned Leave
    # ------------------------------------------------------------
    if "Earned Leave" in merged:

        el_e_alloc = float(db.execute(text("""
            SELECT COALESCE(SUM(lb.allocated), 0)
            FROM leave_balances lb
            JOIN leave_types lt ON lt.type_id = lb.type_id
            WHERE lb.user_id = :uid AND LOWER(lt.code) = 'el_e' AND lb.is_usable = TRUE
        """), {"uid": user_id}).scalar() or 0)

        el_ne_alloc = float(db.execute(text("""
            SELECT COALESCE(SUM(lb.allocated), 0)
            FROM leave_balances lb
            JOIN leave_types lt ON lt.type_id = lb.type_id
            WHERE lb.user_id = :uid AND LOWER(lt.code) = 'el_ne' AND lb.is_usable = TRUE
        """), {"uid": user_id}).scalar() or 0)

        used = float(db.execute(text("""
            SELECT COALESCE(SUM(number_of_days), 0)
            FROM hr_leave_application
            WHERE user_id = :uid
            AND LOWER(leave_type) IN ('el', 'el_e', 'el_ne', 'earned leave', 'earned_leave')
            AND LOWER(status) IN ('approved', 'reversal approved')
            AND from_date <= CURRENT_DATE
        """), {"uid": user_id}).scalar() or 0)

        encashed = float(db.execute(text("""
            SELECT COALESCE(SUM(le.encash_el), 0)
            FROM leave_encashment le
            LEFT JOIN encashment_main em ON em.encashment_main_id = le.encashment_main_id
            WHERE LOWER(le.status) IN (
                'encashment approved',
                'payment processed',
                'paid'
            )
            AND (le.created_by = :uid OR em.created_by = :uid)
        """), {"uid": user_id}).scalar() or 0)

        # Leave usage hits NE first, then E
        used_ne = min(used, el_ne_alloc)
        used_e  = max(used - el_ne_alloc, 0)

        # Encashment only reduces EL_E
        encashable     = max(el_e_alloc  - used_e  - encashed, 0.0)
        non_encashable = max(el_ne_alloc - used_ne,            0.0)

        el = merged["Earned Leave"]
        el["allocated"]      = el_e_alloc + el_ne_alloc
        el["taken"]          = used
        el["balance"]        = encashable + non_encashable
        el["encashable"]     = encashable
        el["non_encashable"] = non_encashable

    # ------------------------------------------------------------
    # 6. Summary totals
    # ------------------------------------------------------------
    total_taken = db.execute(text("""
        SELECT COALESCE(SUM(number_of_days), 0)
        FROM hr_leave_application
        WHERE user_id = :uid
          AND LOWER(status) IN ('approved', 'reversal approved')
          AND from_date <= CURRENT_DATE
    """), {"uid": user_id}).scalar() or 0

    total_provisioned = db.execute(text("""
        SELECT COALESCE(SUM(number_of_days), 0)
        FROM hr_leave_application
        WHERE user_id = :uid
          AND LOWER(status) NOT IN ('approved', 'reversal approved', 'rejected', 
                                   'withdraw approved', 'self_cancelled')
    """), {"uid": user_id}).scalar() or 0

    # ------------------------------------------------------------
    # 7. Final response
    # ------------------------------------------------------------
    return {
        "leaves": list(merged.values()),
        "summary": {
            "total_allocated": float(total_allocated),
            "total_taken": float(total_taken),
            "total_provisioned": float(total_provisioned),
            "total_pending": float(total_provisioned)   # pending = provisioned now
        }
    }



@router.get("/summary_card/{user_id}")
def get_leave_summary(user_id: int, db: Session = Depends(get_db)):

    # ------------------------------------------------------------
    # 1. Fetch allocated leave balances
    # ------------------------------------------------------------
    balances = db.execute(
        text("""
            SELECT 
                lb.type_id,
                lt.name AS leave_type_name,
                lt.code AS leave_code,
                SUM(lb.allocated) AS allocated
            FROM leave_balances lb
            JOIN leave_types lt ON lt.type_id = lb.type_id
            WHERE lb.user_id = :uid
              AND lb.is_usable = TRUE
            GROUP BY lb.type_id, lt.name, lt.code
        """),
        {"uid": user_id}
    ).mappings().all()

    if not balances:
        return {
            "leaves": [],
            "summary": {
                "total_allocated": 0,
                "total_taken": 0,
                "total_provisioned": 0,
                "total_pending": 0
            }
        }

    # ------------------------------------------------------------
    # 2. Fetch applied leaves → Taken + Provisioned (Fixed Logic)
    # ------------------------------------------------------------
    applied_rows = db.execute(text("""
        SELECT 
            LOWER(leave_type) AS leave_type,
            SUM(CASE 
                    WHEN LOWER(status) IN ('approved', 'reversal approved') 
                         AND from_date <= CURRENT_DATE 
                    THEN number_of_days 
                    ELSE 0 
                END) AS taken_days,
            SUM(CASE 
                    WHEN LOWER(status) NOT IN ('approved', 'reversal approved', 'rejected', 
                                              'withdraw approved', 'self_cancelled')
                    THEN number_of_days 
                    ELSE 0 
                END) AS provisioned_days
        FROM hr_leave_application
        WHERE user_id = :uid
        GROUP BY LOWER(leave_type)
    """), {"uid": user_id}).mappings().all()

    taken_map = {row["leave_type"]: float(row["taken_days"] or 0) for row in applied_rows}
    provision_map = {row["leave_type"]: float(row["provisioned_days"] or 0) for row in applied_rows}

    # ------------------------------------------------------------
    # 3. Fetch encashable rules
    # ------------------------------------------------------------
    rules = db.execute(text("""
        SELECT 
            leave_type_id,
            COALESCE((special_rules->>'encashable')::BOOLEAN, FALSE) AS encashable
        FROM leave_allocation_rules
    """)).mappings().all()

    encashable_map = {r["leave_type_id"]: r["encashable"] for r in rules}

    # ------------------------------------------------------------
    # 4. Merge leave balances
    # ------------------------------------------------------------
    merged = {}
    total_allocated = 0.0

    for row in balances:
        raw_name = row["leave_type_name"]
        allocated = float(row["allocated"] or 0)

        is_el = "earned leave" in raw_name.lower()
        name = "Earned Leave" if is_el else raw_name

        taken = taken_map.get(raw_name.lower(), 0.0)
        provisioned = provision_map.get(raw_name.lower(), 0.0)
        is_encashable = encashable_map.get(row["type_id"], False)  # ✅ was missing

        if name not in merged:
            merged[name] = {
                "leave_type_id": row["type_id"],
                "leave_type_name": name,
                "encashable": 0.0,
                "non_encashable": 0.0,
                "allocated": 0.0,
                "taken": 0.0,
                "provisioned": 0.0,
                "balance": 0.0
            }

        merged[name]["allocated"] += allocated
        merged[name]["taken"] += taken
        merged[name]["provisioned"] += provisioned
        merged[name]["balance"] = merged[name]["allocated"] - merged[name]["taken"]

        # ✅ Track encashable/non_encashable per row using the rules map
        row_balance = allocated - taken
        if is_encashable:
            merged[name]["encashable"] += row_balance
        else:
            merged[name]["non_encashable"] += row_balance

        total_allocated += allocated

    # ------------------------------------------------------------
    # 5. OVERRIDE Earned Leave
    # ------------------------------------------------------------
    if "Earned Leave" in merged:

        el_e_alloc = float(db.execute(text("""
            SELECT COALESCE(SUM(lb.allocated), 0)
            FROM leave_balances lb
            JOIN leave_types lt ON lt.type_id = lb.type_id
            WHERE lb.user_id = :uid AND LOWER(lt.code) = 'el_e' AND lb.is_usable = TRUE
        """), {"uid": user_id}).scalar() or 0)

        el_ne_alloc = float(db.execute(text("""
            SELECT COALESCE(SUM(lb.allocated), 0)
            FROM leave_balances lb
            JOIN leave_types lt ON lt.type_id = lb.type_id
            WHERE lb.user_id = :uid AND LOWER(lt.code) = 'el_ne' AND lb.is_usable = TRUE
        """), {"uid": user_id}).scalar() or 0)

        used = float(db.execute(text("""
            SELECT COALESCE(SUM(number_of_days), 0)
            FROM hr_leave_application
            WHERE user_id = :uid
            AND LOWER(leave_type) IN ('el', 'el_e', 'el_ne', 'earned leave', 'earned_leave')
            AND LOWER(status) IN ('approved', 'reversal approved')
            AND from_date <= CURRENT_DATE
        """), {"uid": user_id}).scalar() or 0)

        encashed = float(db.execute(text("""
            SELECT COALESCE(SUM(le.encash_el), 0)
            FROM leave_encashment le
            LEFT JOIN encashment_main em ON em.encashment_main_id = le.encashment_main_id
            WHERE LOWER(le.status) NOT IN ('supervisor rejected', 'rejected', 'cancelled')
            AND (le.created_by = :uid OR em.created_by = :uid)
        """), {"uid": user_id}).scalar() or 0)

        # Leave usage hits NE first, then E
        used_ne = min(used, el_ne_alloc)
        used_e  = max(used - el_ne_alloc, 0)

        # Encashment only reduces EL_E
        encashable     = max(el_e_alloc  - used_e  - encashed, 0.0)
        non_encashable = max(el_ne_alloc - used_ne,            0.0)

        el = merged["Earned Leave"]
        el["allocated"]      = el_e_alloc + el_ne_alloc
        el["taken"]          = used
        el["balance"]        = encashable + non_encashable
        el["encashable"]     = encashable
        el["non_encashable"] = non_encashable

    # ------------------------------------------------------------
    # 6. Summary totals
    # ------------------------------------------------------------
    total_taken = db.execute(text("""
        SELECT COALESCE(SUM(number_of_days), 0)
        FROM hr_leave_application
        WHERE user_id = :uid
          AND LOWER(status) IN ('approved', 'reversal approved')
          AND from_date <= CURRENT_DATE
    """), {"uid": user_id}).scalar() or 0

    total_provisioned = db.execute(text("""
        SELECT COALESCE(SUM(number_of_days), 0)
        FROM hr_leave_application
        WHERE user_id = :uid
          AND LOWER(status) NOT IN ('approved', 'reversal approved', 'rejected', 
                                   'withdraw approved', 'self_cancelled')
    """), {"uid": user_id}).scalar() or 0

    # ------------------------------------------------------------
    # 7. Final response
    # ------------------------------------------------------------
    return {
        "leaves": list(merged.values()),
        "summary": {
            "total_allocated": float(total_allocated),
            "total_taken": float(total_taken),
            "total_provisioned": float(total_provisioned),
            "total_pending": float(total_provisioned)   # pending = provisioned now
        }
    }








