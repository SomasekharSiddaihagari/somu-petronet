import json
import os
import shutil
from typing import Optional, Union
 
from fastapi import (
    APIRouter, Depends, UploadFile, File, Form, HTTPException, Query
)
from datetime import datetime
from sqlalchemy import text
from sqlalchemy.orm import Session
 
from app.crud.gate_pass.GatePassNotificationCrud_old import notify_initiator_on_rejection
from app.crud.gate_pass.ogGatePassCrud import (
    create_outward_gate_pass, 
    get_outward_gate_pass_by_id, 
    get_outward_gate_pass_by_user_crud, 
    update_outward_gate_pass
)
from app.database import get_db
from app.schemas.gate_pass.GatePass import (
    OutwardGatePassByStationResponse, 
    OutwardGatePassByUserRequest, 
    OutwardGatePassCreate, 
    OutwardGatePassUpdate, 
    OutwardResponse
)
from fastapi import BackgroundTasks
from app.crud.gate_pass.GatePassNotificationCrud import (
    notify_approver_on_create,
    notify_security_on_pending_verification,
    notify_acknowledge_verified
)
from app.utils.UserAuthUtils import verify_access_token
 
router = APIRouter(prefix="/api/GatePass/OG", tags=["OG GatePass"])
UPLOAD_ROOT = "files/gate_pass"
os.makedirs(UPLOAD_ROOT, exist_ok=True)
 
 
@router.post("/create")
async def create_outward_gate_pass_pg(
    background_tasks: BackgroundTasks,
    data: str = Form(...),
    vehicle_photo: Union[UploadFile, str, None] = File(None), 
    delivery_personnel_photo: Union[UploadFile, str, None] = File(None),
    delivery_personnel_id_photo: Union[UploadFile, str, None] = File(None),
    goods_photo: Union[UploadFile, str, None] = File(None),
    db: Session = Depends(get_db)
):
    try:
        outward_json = json.loads(data)
        outward_data = OutwardGatePassCreate(**outward_json).dict()
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid JSON: {e}")

    UPLOAD_DIR = "files/gate_pass"
    os.makedirs(UPLOAD_DIR, exist_ok=True)

    def save_file(file_obj):
        # Skip if no file or it's already a string path
        if not file_obj or isinstance(file_obj, str):
            return None
        if not hasattr(file_obj, 'filename') or not file_obj.filename:
            return None

        # ✅ Unique filename: timestamp + original name
        filename = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{file_obj.filename}"
        file_path = os.path.join(UPLOAD_DIR, filename)

        with open(file_path, "wb") as f:
            f.write(file_obj.file.read())

        # ✅ Return relative path for DB (consistent with material details)
        return f"files/gate_pass/{filename}"

    outward_data.update({
        "vehicle_photo": save_file(vehicle_photo),
        "delivery_personnel_photo": save_file(delivery_personnel_photo),
        "delivery_personnel_id_photo": save_file(delivery_personnel_id_photo),
        "goods_photo": save_file(goods_photo),
    })

    # CREATE GATE PASS
    result = create_outward_gate_pass(db, OutwardGatePassCreate(**outward_data))

    # SEND NOTIFICATION TO APPROVER (IN BACKGROUND)
    await notify_approver_on_create(db, result, background_tasks)

    return {
        "status": "success",
        "message": "Outward Gate Pass created successfully",
        "data": result,
    }


# --- Update API ---
 
@router.put("/{outward_id}", summary="Update Outward Gate Pass (with optional photos)")
async def update_outward(
    outward_id: int,
    background_tasks: BackgroundTasks,    # ⭐ Needed for background email
    data: str = Form(...),
    vehicle_photo: Union[UploadFile, str, None] = File(None),
    delivery_personnel_photo: Union[UploadFile, str, None] = File(None),
    delivery_personnel_id_photo: Union[UploadFile, str, None] = File(None),
    goods_photo: Union[UploadFile, str, None] = File(None),
    db: Session = Depends(get_db)
):
    # 1️⃣ Parse JSON safel
    try:
        outward_json = json.loads(data)
        outward_data = OutwardGatePassUpdate(**outward_json)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid JSON format: {str(e)}")

    # 2️⃣ NEVER allow approver_id to change
    existing = get_outward_gate_pass_by_id(db, outward_id)

    if isinstance(existing, dict) and "data" in existing:
        existing_outward = existing["data"]["outward"]
    else:
        existing_outward = existing

    actual_approver_id = (
        existing_outward["approver_id"]
        if isinstance(existing_outward, dict)
        else existing_outward.approver_id
    )

    # 3️⃣ Save uploaded files
    def save_file(file_obj):
        if isinstance(file_obj, str) or not file_obj:
            return None
        if not getattr(file_obj, "filename", None):
            return None

        file_path = os.path.join(UPLOAD_ROOT, file_obj.filename)

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file_obj.file, buffer)

        return os.path.abspath(file_path).replace("\\", "/")

    file_paths = {
        "vehicle_photo": save_file(vehicle_photo),
        "delivery_personnel_photo": save_file(delivery_personnel_photo),
        "delivery_personnel_id_photo": save_file(delivery_personnel_id_photo),
        "goods_photo": save_file(goods_photo),
    }

    # 4️⃣ UPDATE RECORD (this returns either SQL-JSON or dict)
    updated_outward = update_outward_gate_pass(db, outward_id, outward_data, file_paths)

    # 5️⃣ Extract updated outward safely
    if isinstance(updated_outward, dict) and "data" in updated_outward:
        try:
            outward_obj = updated_outward["data"]["outward"]
        except:
            outward_obj = updated_outward
    else:
        outward_obj = updated_outward

    # 6️⃣ Extract status safely (supports dict + model)
    status_value = (
        outward_obj["status"]
        if isinstance(outward_obj, dict)
        else outward_obj.status
    )

    # 7️⃣ Notification: choose by status
    if status_value == "Pending Verification":
        await notify_security_on_pending_verification(db, updated_outward, background_tasks)

    elif status_value == "Rejected":
        await notify_initiator_on_rejection(db, updated_outward, background_tasks)

    elif status_value == "Verified":
        await notify_acknowledge_verified(db, updated_outward, background_tasks)

    return {
        "status": "success",
        "message": "Outward Gate Pass updated successfully",
        "data": updated_outward,
    }

 



# @router.get(
#     "/GetAllOutwardGatePass/{user_id}",
#     response_model=OutwardGatePassByStationResponse,
#     summary="Fetch outward gate passes using user_id"
# )
# def get_outward_gate_pass(
#     user_id: int,
#     db: Session = Depends(get_db)
# ):
#     try:
#         # Pass integer directly to CRUD
#         result = get_outward_gate_pass_by_user_crud(db, user_id)
 
#         if not result or result.get("status_code") == 500:
#             raise HTTPException(status_code=500, detail=result)
 
#         return result
 
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

  
from fastapi.responses import JSONResponse
from datetime import datetime, date
import json

# ── Custom JSON serializer ───────────────────────────────────────────────────
def serialize(obj):
    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    raise TypeError(f"Type {type(obj)} not serializable")

@router.get(
    "/GetAllOutwardGatePass/{user_id}",
    summary="Fetch outward gate passes using user_id"
)
def get_outward_gate_pass(
    user_id: int,
    db: Session = Depends(get_db)
):
    try:
        result = get_outward_gate_pass_by_user_crud(db, user_id)  # ← correct function

        if not result or result.get("status_code") == 500:
            raise HTTPException(status_code=500, detail=result)

        return JSONResponse(
            content=json.loads(json.dumps(result, default=lambda obj: obj.isoformat() if isinstance(obj, (datetime, date)) else str(obj)))
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
 

import urllib.parse
import urllib.parse
def make_download_url(path: str) -> str:
    if not path:
        return None

    base_url = os.getenv("BackEndPath")

    # Normalize slashes
    file_path = path.replace("\\", "/")

    # Remove Windows drive letter (D:, C:, etc.)
    if ":" in file_path:
        file_path = file_path.split(":", 1)[1]

    # Remove "/Petronet" if it exists
    if file_path.startswith("/Petronet"):
        file_path = file_path.replace("/Petronet", "", 1)

    # Ensure the path starts with a single slash
    file_path = "/" + file_path.lstrip("/")

    # Encode spaces, parentheses, special characters
    encoded_path = urllib.parse.quote(file_path)

    return f"{base_url}{encoded_path}"


@router.get("/{outward_id}", response_model=OutwardResponse)
def get_outward(outward_id: int, db: Session = Depends(get_db)):
    # print("\n\n====== [DEBUG] API CALL: GET OUTWARD", outward_id, "======")

    outward = get_outward_gate_pass_by_id(db, outward_id)

    # print("[DEBUG] Raw outward data from DB:")
    # print(outward)

    if outward is None:
        # print("[DEBUG] Outward not found")
        raise HTTPException(404, f"Outward Gate Pass with ID {outward_id} not found")

    # Get nested fields safely
    data = outward.get("data", {})
    materials = data.get("materials", [])
    photos = data.get("photos", [])

    # --- materials ---
    # print("\n[DEBUG] Processing materials...")
    # print("[DEBUG] Materials count:", len(materials))

    for m in materials:
        # print("[DEBUG] Material item:", m)
        if m.get("goods_photo"):
            # print("[DEBUG] Processing material goods_photo:", m["goods_photo"])
            m["goods_photo"] = make_download_url(m["goods_photo"])

    # --- photos ---
    # print("\n[DEBUG] Processing photos...")
    # print("[DEBUG] Photos count:", len(photos))

    for p in photos:
        # print("[DEBUG] Photo item:", p)
        for key in [
            "vehicle_photo",
            "delivery_personnel_photo",
            "delivery_personnel_id_photo",
            "goods_photo",
        ]:
            if p.get(key):
                # print(f"[DEBUG] Processing photo key '{key}':", p[key])
                p[key] = make_download_url(p[key])

    # print("\n[DEBUG] Final outward response:")
    # print(outward)

    return outward




















