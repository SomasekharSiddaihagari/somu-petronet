from datetime import date
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import text
from app.crud.leave.hr_comp_off_crud import bulk_update_comp_off_usage, create_comp_off, get_all_comp_off_all, get_comp_off_by_user, validate_comp_off_leave
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.leave.hr_leave_application import HRLeaveApplication
from app.schemas.leave.leave_comp_off import BulkCompOffUpdate, CompOffApplyRequest, CompOffCreate, MessageResponse
from app.crud.leave.hr_comp_off_crud import (
    create_comp_off,
    get_all_comp_off,
    get_comp_off_by_id
)
router = APIRouter(prefix="/comp-off", tags=["Comp Off"])

@router.get("/check")
def check_comp_off_apply(
    user_id: int,
    leave_date: date,
    db: Session = Depends(get_db)
):
    # 1️⃣ compoff assigned?
    assigned = db.execute(text("""
        SELECT 1
        FROM hr_leave_compof_day_new
        WHERE user_id = :user_id
        AND leave_date = :leave_date
        LIMIT 1
    """), {
        "user_id": user_id,
        "leave_date": leave_date
    }).first()

    if not assigned:
        return {"allowed": False, "message": "Comp-off not assigned"}

    # 2️⃣ already used in leave application?
    used = db.execute(text("""
        SELECT 1
        FROM hr_leave_application
        WHERE user_id = :user_id
        AND leave_type = 'COMP_OFF'
        AND status NOT IN ('Rejected','Cancelled')
        AND :leave_date BETWEEN from_date AND to_date
        LIMIT 1
    """), {
        "user_id": user_id,
        "leave_date": leave_date
    }).first()

    if used:
        return {
            "allowed": False,
            "message": "Comp-off already used for this date"
        }

    return {"allowed": True, "message": "Can apply"}




# 🔵 POST create (multiple dates)
@router.post("/assign", response_model=MessageResponse)
def assign_comp_off(
    payload: CompOffCreate,
    db: Session = Depends(get_db),
    supervisor_id: int = 1   # 🔴 replace from login token
):
    result = create_comp_off(db, supervisor_id, payload)

    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])

    return {
        "success": True,
        "message": f"Comp off created for {len(result['ids'])} days"
    }


# 🔵 GET ALL
@router.get("/all")
def get_all(
    db: Session = Depends(get_db),
    supervisor_id: int = 1  # from token
):
    return get_all_comp_off(db, supervisor_id)



@router.get("/for_all")
def get_all(
    db: Session = Depends(get_db)
):
    return get_all_comp_off_all(db)



# 🔵 GET BY ID
@router.get("/user/{user_id}")
def get_by_user(
    user_id: int,
    db: Session = Depends(get_db)
):
    res = get_comp_off_by_user(db, user_id)

    if not res:
        raise HTTPException(status_code=404, detail="User not found")

    return res

@router.get("/{id}")
def get_by_id(
    id: int,
    db: Session = Depends(get_db),
    supervisor_id: int = 1
):
    res = get_comp_off_by_id(db, id, supervisor_id)

    if not res:
        raise HTTPException(status_code=404, detail="Not found")

    return res



# ---------------------------------------------------------
# VALIDATE API
# ---------------------------------------------------------
@router.post("/leave/comp-off/apply")
def apply_comp_off_leave(
    req: CompOffApplyRequest,
    db: Session = Depends(get_db)
):
    result = validate_comp_off_leave(db, req)
    return result


# @router.put("/comp-off/bulk-update")
# def bulk_update_comp_off(
#     payload: BulkCompOffUpdate,
#     db: Session = Depends(get_db)
# ):

#     ok, msg = bulk_update_comp_off_usage(db, payload)

#     if not ok:
#         raise HTTPException(status_code=400, detail=msg)

#     return {
#         "status": "success",
#         "message": msg
#     }
    
@router.put("/comp-off/bulk-update")
def bulk_update_comp_off(
    payload: BulkCompOffUpdate,
    db: Session = Depends(get_db)
):

    ok, msg = bulk_update_comp_off_usage(db, payload)

    if not ok:
        raise HTTPException(status_code=400, detail=msg)

    return {
        "status": "success",
        "message": msg
    }

# ---------------------------------------------------------
# APPLY COMP-OFF
# ---------------------------------------------------------
# @router.post("/apply-comp-off")
# def apply_comp_off_leave(
#     payload: CompOffValidate,
#     db: Session = Depends(get_db)
#     ):

#     # --------------------------------------------------
#     # 1️⃣ Check comp dates from frontend
#     # --------------------------------------------------
#     if not payload.comp_dates:
#         return {
#             "success": False,
#             "message": "comp_dates required"
#         }

#     # remove duplicate dates if any
#     comp_dates_list = list(set(payload.comp_dates))

#     # --------------------------------------------------
#     # 2️⃣ Count number of days
#     # --------------------------------------------------
#     number_of_days = len(comp_dates_list)

#     if payload.half_day_count:
#         number_of_days -= payload.half_day_count * 0.5

#     # --------------------------------------------------
#     # 3️⃣ Insert into HRLeaveApplication table
#     # --------------------------------------------------
#     new_leave = HRLeaveApplication(
#         user_id=payload.user_id,
#         leave_type="COMP_OFF",
#         from_date=payload.from_date,
#         to_date=payload.to_date,
#         number_of_days=number_of_days,
#         reason=payload.reason,
#         comp_dates=comp_dates_list,
#         status="Pending"
#     )

#     db.add(new_leave)
#     db.commit()
#     db.refresh(new_leave)

#     # --------------------------------------------------
#     # 4️⃣ Response
#     # --------------------------------------------------
#     return {
#         "success": True,
#         "leave_id": new_leave.leave_id,
#         "number_of_days": float(number_of_days),
#         "comp_dates_count": len(comp_dates_list),
#         "message": "Comp-off leave applied successfully"
#     }



