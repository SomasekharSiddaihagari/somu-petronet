import asyncio
from datetime import datetime
import json
import os
import shutil
from typing import Any, Optional
from fastapi import (
    APIRouter, BackgroundTasks, Depends, UploadFile,
    File as FastAPIFile, Form, HTTPException
)
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.database import get_db
from app.utils.UserAuthUtils import verify_access_token

from app.crud.gate_pass.rgGatePassCrud import (
    create_returnable_gate_pass_from_outward_crud,
    get_all_gate_passes_by_user,
    get_all_gate_passes_crud,
    insert_returnable_materials_and_photos,
    rg_get_by_station,
    track_returnable_gate_pass_crud,
    update_returnable_gate_pass_by_outward_id,
    update_returnable_materials_and_photos
)

# 🔔 Notification Imports
from app.crud.gate_pass.GatePassNotificationCrud import (
    notify_returnable_approver_on_create,
    notify_returnable_on_status_change
)

from app.schemas.gate_pass.GatePass import (
    ReturnableGatePassData,
    ReturnableGatePassRequest,
    ReturnableGatePassResponse,
    UpdateReturnableGatePassRequest
)
import asyncpg  
router = APIRouter(prefix="/api/GatePassRG", tags=["RG GatePass"])

UPLOAD_ROOT = "files/gate_pass"
os.makedirs(UPLOAD_ROOT, exist_ok=True)

# ── router ────────────────────────────────────────────────────────────────────
@router.post("/create", response_model=ReturnableGatePassResponse)
async def create_returnable_gate_pass(
    payload: ReturnableGatePassRequest,
    db: Session = Depends(get_db),
):
    try:
        # 1. Verify outward_id exists
        result = db.execute(
            text("SELECT outward_id FROM outward_gate_pass WHERE outward_id = :outward_id"),
            {"outward_id": payload.outward_id}
        )
        if not result.fetchone():
            raise HTTPException(status_code=404, detail="Outward gate pass not found")

        # 2. Generate gate pass number using DB function
        gate_pass_result = db.execute(
            text("SELECT generate_returnable_gate_pass_no(:outward_id) AS gate_pass_no"),
            {"outward_id": payload.outward_id}
        )
        returnable_gate_pass_no = gate_pass_result.fetchone().gate_pass_no

        # 3. Insert all fields
        insert_result = db.execute(
            text("""
                INSERT INTO returnable_gate_pass (
                    outward_id, returnable_gate_pass_no, approved_by, reviewer_id,
                    date_time, status, created_by, updated_by, created_at, updated_at,
                    gate_pass_no, date_time_ret, station,
                    department_contractor_name, purpose, address,
                    material_taken_by, vehicle_no, driver_phone
                )
                VALUES (
                    :outward_id, :returnable_gate_pass_no, :approved_by, :reviewer_id,
                    NOW(), 'pending', :created_by, :created_by, NOW(), NOW(),
                    :gate_pass_no, NOW(), :station,
                    :department_contractor_name, :purpose, :address,
                    :material_taken_by, :vehicle_no, :driver_phone
                )
                RETURNING
                    returnable_id, outward_id, returnable_gate_pass_no, approved_by,
                    reviewer_id, date_time, status, created_by, updated_by,
                    created_at, updated_at, gate_pass_no, date_time_ret, station,
                    department_contractor_name, purpose, address,
                    material_taken_by, vehicle_no, driver_phone
            """),
            {
                "outward_id":                 payload.outward_id,
                "returnable_gate_pass_no":    returnable_gate_pass_no,  # ← from DB function
                "approved_by":                payload.approver_name,
                "reviewer_id":                payload.reviewer_id,
                "created_by":                 payload.created_by,
                "gate_pass_no":               payload.gate_pass_no,
                "station":                    payload.station,
                "department_contractor_name": payload.department_contractor_name,
                "purpose":                    payload.purpose,
                "address":                    payload.address,
                "material_taken_by":          payload.material_taken_by,
                "vehicle_no":                 payload.vehicle_no,
                "driver_phone":               payload.driver_phone,
            }
        )

        db.commit()
        row = insert_result.fetchone()

        return ReturnableGatePassResponse(
            status="success",
            message="Returnable gate pass created successfully",
            data=ReturnableGatePassData(**row._mapping),
        )

    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")



# ============================================================
# UPDATE RETURNABLE
# ============================================================

# @router.put("/UpdateReturnableGatePass", summary="Update Returnable Gate Pass")
# async def update_returnable_gate_pass(
#     request: UpdateReturnableGatePassRequest,
#     db: Session = Depends(get_db),
#     background_tasks: BackgroundTasks = None,
#     current_user: str = Depends(verify_access_token)
# ):
#     try:
#         result = update_returnable_gate_pass_by_outward_id(
#             db=db,
#             outward_id=request.outward_id,
#             payload=request
#         )

#         # 🔔 Notify on status change
#         await notify_returnable_on_status_change(
#             db=db,
#             outward_id=request.outward_id,
#             status=request.status,
#             updated_by=request.updated_by,
#             background_tasks=background_tasks
#         )

#         return {
#             "status_code": result.status_code,
#             "status_message": result.status_message,
#             "data": result.data
#         }

#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

# ── Router ────────────────────────────────────────────────────────────────────
@router.put("/UpdateReturnableGatePass", summary="Update Returnable Gate Pass")
async def update_returnable_gate_pass(
    request: UpdateReturnableGatePassRequest,
    db: Session = Depends(get_db),
    background_tasks: BackgroundTasks = None,
    current_user: str = Depends(verify_access_token)
):
    try:
        result = update_returnable_gate_pass_by_outward_id(
            db=db,
            outward_id=request.outward_id,
            payload=request
        )

        await notify_returnable_on_status_change(
            db=db,
            outward_id=request.outward_id,
            status=request.status,
            updated_by=request.updated_by,
            background_tasks=background_tasks
        )

        return {
            "status_code":    result.status_code,
            "status_message": result.status_message,
            "data":           result.data
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
# ============================================================
# FILE SAVE HELPER
# ============================================================

def save_upload_file(upload_file: UploadFile, folder: str) -> str:
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    filename = f"{timestamp}_{upload_file.filename}"
    file_path = os.path.join(folder, filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(upload_file.file, buffer)

    return file_path


# ============================================================
# INSERT RETURN MATERIALS
# ============================================================

@router.post("/insert-return")
async def insert_returnable_materials(
    returnable_gate_pass_no: str = Form(...),
    uploaded_by: str = Form(...),
    materials: str = Form(...),
    vehicle_photo: UploadFile = FastAPIFile(...),
    delivery_personnel_photo: UploadFile = FastAPIFile(...),
    delivery_personnel_id_photo: UploadFile = FastAPIFile(...),
    goods_photo: UploadFile = FastAPIFile(...),
    db: Session = Depends(get_db),
    background_tasks: BackgroundTasks = None
):
    try:
        materials_list = json.loads(materials)

        file_paths = {
            "vehicle_photo": save_upload_file(vehicle_photo, UPLOAD_ROOT),
            "delivery_personnel_photo": save_upload_file(delivery_personnel_photo, UPLOAD_ROOT),
            "delivery_personnel_id_photo": save_upload_file(delivery_personnel_id_photo, UPLOAD_ROOT),
            "goods_photo": save_upload_file(goods_photo, UPLOAD_ROOT),
        }

        result = insert_returnable_materials_and_photos(
            db=db,
            gate_pass_no=returnable_gate_pass_no,
            materials=materials_list,
            vehicle_photo=file_paths["vehicle_photo"],
            delivery_personnel_photo=file_paths["delivery_personnel_photo"],
            delivery_personnel_id_photo=file_paths["delivery_personnel_id_photo"],
            goods_photo=file_paths["goods_photo"],
            uploaded_by=uploaded_by
        )

        # 🔔 Notify outward creator that material returned
        outward_row = db.execute(
            text("""
                SELECT outward_id
                FROM returnable_gate_pass
                WHERE returnable_gate_pass_no = :no
            """),
            {"no": returnable_gate_pass_no}
        ).fetchone()

        if outward_row:
            await notify_returnable_on_status_change(
                db=db,
                outward_id=outward_row[0],
                status="Returned",
                updated_by=uploaded_by,
                background_tasks=background_tasks
            )

        return {"success": True, "data": result}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")






@router.put("/update-return")
async def update_returnable_materials(
    returnable_gate_pass_no: str = Form(...),
    uploaded_by: str = Form(...),
    materials: str = Form(...),
    vehicle_photo: Optional[UploadFile] = FastAPIFile(None),
    delivery_personnel_photo: Optional[UploadFile] = FastAPIFile(None),
    delivery_personnel_id_photo: Optional[UploadFile] = FastAPIFile(None),
    goods_photo: Optional[UploadFile] = FastAPIFile(None),
    db: Session = Depends(get_db),
    background_tasks: BackgroundTasks = None
):
    try:
        materials_list = json.loads(materials)

        # Only save files that were actually uploaded
        file_paths = {
            "vehicle_photo": save_upload_file(vehicle_photo, UPLOAD_ROOT) if vehicle_photo else None,
            "delivery_personnel_photo": save_upload_file(delivery_personnel_photo, UPLOAD_ROOT) if delivery_personnel_photo else None,
            "delivery_personnel_id_photo": save_upload_file(delivery_personnel_id_photo, UPLOAD_ROOT) if delivery_personnel_id_photo else None,
            "goods_photo": save_upload_file(goods_photo, UPLOAD_ROOT) if goods_photo else None,
        }

        result = update_returnable_materials_and_photos(
            db=db,
            gate_pass_no=returnable_gate_pass_no,
            materials=materials_list,
            vehicle_photo=file_paths["vehicle_photo"],
            delivery_personnel_photo=file_paths["delivery_personnel_photo"],
            delivery_personnel_id_photo=file_paths["delivery_personnel_id_photo"],
            goods_photo=file_paths["goods_photo"],
            uploaded_by=uploaded_by
        )

        # 🔔 Notify on update
        outward_row = db.execute(
            text("""
                SELECT outward_id
                FROM returnable_gate_pass
                WHERE returnable_gate_pass_no = :no
            """),
            {"no": returnable_gate_pass_no}
        ).fetchone()

        if outward_row:
            await notify_returnable_on_status_change(
                db=db,
                outward_id=outward_row[0],
                status="Updated",
                updated_by=uploaded_by,
                background_tasks=background_tasks
            )

        return {"success": True, "data": result}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
# ============================================================
# CREATE FROM OUTWARD
# ============================================================

@router.post("/create-from-outward")
async def create_returnable_gate_pass_from_outward(
    request: ReturnableGatePassRequest,
    db: Session = Depends(get_db),
    background_tasks: BackgroundTasks = None
):
    try:
        result = create_returnable_gate_pass_from_outward_crud(
            db,
            outward_id=request.outward_id,
            created_by=request.created_by,
            approver_name=request.approver_name,
        )

        # 🔔 Notify Approver
        await notify_returnable_approver_on_create(
            db=db,
            outward_id=request.outward_id,
            approver_name=request.approver_name,
            created_by=request.created_by,
            background_tasks=background_tasks
        )

        return {
            "status": "success",
            "message": "Returnable Gate Pass created successfully",
            "data": result
        }

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


# ============================================================
# TRACK
# ============================================================

@router.get("/track")
def track_returnable_gate_pass(
    outward_id: int,
    db: Session = Depends(get_db)
):
    return track_returnable_gate_pass_crud(db=db, outward_id=outward_id)


# ============================================================
# STATION BASED LIST
# ============================================================

@router.get("/station/{user_id}")
def get_returnable_gate_pass_by_station(
    user_id: int,
    db: Session = Depends(get_db)
):
    return rg_get_by_station(db, user_id)


# ============================================================
# ALL GATE PASS
# ============================================================

@router.get("/ig-og-rt-all/{user_id}")
def get_all_gate_passes(user_id: int, db: Session = Depends(get_db)):
    return get_all_gate_passes_by_user(db=db, user_id=user_id)


@router.get("/gate-passes/all")
def get_all_gate_passes_api(db: Session = Depends(get_db)):
    return get_all_gate_passes_crud(db)





























































