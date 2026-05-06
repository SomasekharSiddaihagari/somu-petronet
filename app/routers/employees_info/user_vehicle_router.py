from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from sqlalchemy import text
from typing import List, Optional
from datetime import datetime, date
import os
import shutil

from starlette import status

from app.database import get_db
from app.models.UserModel import User

from app.crud.employees_info.employee_notifications_crud import (
    get_all_hr_usernames,
    handle_employee_update_notifications,
    notify_employee_on_status_change
)

from app.crud.employees_info.user_vehicle_curd import (
    create_user_vehicle,
    get_user_vehicle_by_id,
    get_user_vehicles,
    update_user_vehicle,
    delete_user_vehicle
)

from app.schemas.employees_info.user_vehicle_schemas import (
    UserVehicleResponse,
    UserVehicleCreate,
    UserVehicleUpdate
)

router = APIRouter(
    prefix="/user-vehicle",
    tags=["User Vehicle"]
)

UPLOAD_DIR = "files/user_vehicle"
os.makedirs(UPLOAD_DIR, exist_ok=True)


# =========================================================
# CREATE VEHICLE
# =========================================================

@router.post("/create", response_model=UserVehicleResponse)
async def create_vehicle(

    user_id: int = Form(...),
    vehicle_type: Optional[str] = Form(None),
    vehicle_make: Optional[str] = Form(None),
    vehicle_model: Optional[str] = Form(None),
    color: Optional[str] = Form(None),
    fuel_type: Optional[str] = Form(None),
    vehicle_registration_no: Optional[str] = Form(None),

    rc_expiry_date: Optional[date] = Form(None),

    insurance_provider: Optional[str] = Form(None),
    insurance_policy_number: Optional[str] = Form(None),
    insurance_expiry_date: Optional[date] = Form(None),

    puc_expiry_date: Optional[date] = Form(None),

    document_upload: List[UploadFile] = File(None),
    status:Optional[str]=Form(None),
    document_details: Optional[str] = Form(None),
    comment: Optional[str] = Form(None),

    active: Optional[bool] = Form(True),

    background_tasks: BackgroundTasks = None,
    db: Session = Depends(get_db)
):

    # ---------- USER CHECK ----------

    user_obj = db.query(User).filter(User.user_id == user_id).first()

    if not user_obj:
        raise HTTPException(404, "User not found")


    # ---------- FILE UPLOAD ----------

    file_paths = []

    if document_upload:

        for file in document_upload:

            if file and file.filename:

                filename = f"{datetime.now().timestamp()}_{file.filename}"

                path = os.path.join(UPLOAD_DIR, filename)

                with open(path, "wb") as f:
                    shutil.copyfileobj(file.file, f)

                file_paths.append(path)


    # ---------- CREATE PAYLOAD ----------

    payload = UserVehicleCreate(

        user_id=user_id,

        vehicle_type=vehicle_type,
        vehicle_make=vehicle_make,
        vehicle_model=vehicle_model,

        color=color,
        fuel_type=fuel_type,

        vehicle_registration_no=vehicle_registration_no,

        rc_expiry_date=rc_expiry_date,

        insurance_provider=insurance_provider,
        insurance_policy_number=insurance_policy_number,
        insurance_expiry_date=insurance_expiry_date,

        puc_expiry_date=puc_expiry_date,

        status=status,

        document_details=document_details,
        comment=comment,

        active=active,

        document_upload=",".join(file_paths) if file_paths else None
    )

    vehicle = create_user_vehicle(db, payload)


    # ---------- NOTIFICATION → HR ----------

    await handle_employee_update_notifications(

        db=db,
        old_status=None,
        new_status="Pending Approval",
        old_comments=None,
        new_comments=None,
        employee_username=user_obj.username,
        changed_sections=["Vehicle"],
        changed_fields = [],
        reference_id=str(user_id),
        redirect_url=f"/profile/profile-info/{str(user_id)}/review",
        bg=background_tasks
    )

    return vehicle


# =========================================================
# UPDATE VEHICLE
# =========================================================

@router.put("/update/{vehicle_id}", response_model=UserVehicleResponse)
async def update_vehicle(

    vehicle_id: int,

    user_id: int = Form(...),

    vehicle_type: Optional[str] = Form(None),
    vehicle_make: Optional[str] = Form(None),
    vehicle_model: Optional[str] = Form(None),

    color: Optional[str] = Form(None),
    fuel_type: Optional[str] = Form(None),

    vehicle_registration_no: Optional[str] = Form(None),

    rc_expiry_date: Optional[date] = Form(None),

    insurance_provider: Optional[str] = Form(None),
    insurance_policy_number: Optional[str] = Form(None),
    insurance_expiry_date: Optional[date] = Form(None),

    puc_expiry_date: Optional[date] = Form(None),
    status:Optional[str]=Form(None),
    document_details: Optional[str] = Form(None),
    comment: Optional[str] = Form(None),

    active: Optional[bool] = Form(None),

    document_upload: List[UploadFile] = File(None),

    background_tasks: BackgroundTasks = None,
    db: Session = Depends(get_db)
):

    user_obj = db.query(User).filter(User.user_id == user_id).first()

    if not user_obj:
        raise HTTPException(404, "User not found")

    old_status = user_obj.status
    old_comments = user_obj.comments

    old_vehicle = get_user_vehicle_by_id(db, vehicle_id)
    if not old_vehicle:
        raise HTTPException(404, "Vehicle not found")
    # ---------- FILE UPLOAD ----------

    file_paths = []

    if document_upload:

        for file in document_upload:

            filename = f"{datetime.now().timestamp()}_{file.filename}"

            path = os.path.join(UPLOAD_DIR, filename)

            with open(path, "wb") as f:
                shutil.copyfileobj(file.file, f)

            file_paths.append(path)


    payload = UserVehicleUpdate(

        vehicle_type=vehicle_type,
        vehicle_make=vehicle_make,
        vehicle_model=vehicle_model,

        color=color,
        fuel_type=fuel_type,

        vehicle_registration_no=vehicle_registration_no,

        rc_expiry_date=rc_expiry_date,

        insurance_provider=insurance_provider,
        insurance_policy_number=insurance_policy_number,
        insurance_expiry_date=insurance_expiry_date,

        puc_expiry_date=puc_expiry_date,

        status=status,

        document_details=document_details,
        comment=comment,

        active=active,

        document_upload=",".join(file_paths) if file_paths else None
    )
    new_data = payload.dict(exclude_unset=True)

    def get_changed_fields(old_obj, new_data: dict):
        changes = []

        IGNORE_FIELDS = ["document_upload", "active"]

        for field, new_value in new_data.items():

            if field in IGNORE_FIELDS:
                continue

            if new_value is None:
                continue

            old_value = getattr(old_obj, field, None)

            # Convert date → string
            if hasattr(old_value, "isoformat"):
                old_value = old_value.isoformat()
            if hasattr(new_value, "isoformat"):
                new_value = new_value.isoformat()

            if str(old_value) != str(new_value):
                changes.append({
                    "field": field,
                    "old": old_value,
                    "new": new_value
                })

        return changes

    changed_fields = get_changed_fields(old_vehicle, new_data)
    #print("Changed fields:", changed_fields)
    # ---------- UPDATE ----------


    vehicle = update_user_vehicle(db, vehicle_id, payload, changed_fields)

    if not vehicle:
        raise HTTPException(404, "Vehicle not found")


    # ---------- NOTIFICATION → HR ----------

    await handle_employee_update_notifications(
        db=db,
        old_status=old_status,
        new_status=status,
        old_comments=old_comments,
        new_comments=None,
        employee_username=user_obj.username,
        changed_sections=["Vehicle"],
        changed_fields = changed_fields,
        reference_id=str(user_id),
        redirect_url=f"/profile/profile-info/{str(user_id)}/review",
        bg=background_tasks
    )

    return vehicle


# =========================================================
# HR REVIEW VEHICLE
# =========================================================
 
@router.put("/hr-review/{vehicle_id}")
async def hr_review_vehicle(
 
    vehicle_id: int,
    status: str = Form(...),
    hr_comment: str | None = Form(None),
 
    background_tasks: BackgroundTasks = None,
    db: Session = Depends(get_db)
 
):
 
    if status not in ["Approved", "Changes Requested"]:
        raise HTTPException(400, "Invalid status")
 
    vehicle = get_user_vehicle_by_id(db, vehicle_id)
 
    if not vehicle:
        raise HTTPException(404, "Vehicle not found")
 
    # Update + fetch updated row
    result = db.execute(
        text("""
            UPDATE user_vehicle
            SET status=:status
            WHERE id=:id
            RETURNING *
        """),
        {"status": status, "id": vehicle_id}
    )
 
    updated_vehicle = result.fetchone()
    user_id = updated_vehicle._mapping["user_id"]
 
    db.commit()
 
    user = db.query(User).filter(User.user_id == updated_vehicle.user_id).first()
 
    # Send notification: HR → Employee (confirmation of review decision)
    hr_usernames = get_all_hr_usernames(db)
    hr_username = hr_usernames[0] if hr_usernames else "HR"
 
    await notify_employee_on_status_change(
        db=db,
        employee_username=user.username,
        hr_username=hr_username,
        new_status=status,
        comments=hr_comment,
        changed_sections="Vehicle Info",
        reference_id=str(user_id),
        redirect_url=f"/profile/{str(user_id)}",
        bg=background_tasks
    )
 
    # Return proper response
    return {
        "message": "Vehicle review completed",
        "data": dict(updated_vehicle._mapping)
    }
 
    

# =========================================================
# LIST USER VEHICLES
# =========================================================

@router.get("/user/{user_id}", response_model=List[UserVehicleResponse])
def list_user_vehicles(

    user_id: int,
    db: Session = Depends(get_db)
):

    vehicles = get_user_vehicles(db, user_id)

    return vehicles


# =========================================================
# GET VEHICLE BY ID
# =========================================================

@router.get("/{vehicle_id}", response_model=UserVehicleResponse)
def get_vehicle_by_id(

    vehicle_id: int,
    db: Session = Depends(get_db)
):

    vehicle = get_user_vehicle_by_id(db, vehicle_id)

    if not vehicle:
        raise HTTPException(404, "Vehicle not found")

    return vehicle


# =========================================================
# DELETE VEHICLE
# =========================================================

@router.delete("/delete/{vehicle_id}")
def remove_vehicle(

    vehicle_id: int,
    db: Session = Depends(get_db)
):

    success = delete_user_vehicle(db, vehicle_id)

    if not success:
        raise HTTPException(404, "Vehicle not found")

    return {"message": "Vehicle deleted successfully"}




























