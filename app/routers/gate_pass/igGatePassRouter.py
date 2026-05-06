import json
import os
import shutil
from typing import Literal, Optional
from click import File
from typing import Optional, Union
from fastapi import (
    APIRouter, BackgroundTasks, Depends, UploadFile, File as FastAPIFile, Form, HTTPException
)
from fastapi import APIRouter, Depends, Form, HTTPException, HTTPException, Query, UploadFile
from sqlalchemy import text
from sqlalchemy.orm import Session
from app.crud.gate_pass.igGatePassCrud import   create_inward_gate_pass_crud, get_all_inward_gate_passes, get_cardData_crud,  get_gatepass_by_formtype, get_inward_gate_pass_by_id, update_inward_gate_pass_full
from app.database import get_db
from app.dependencies.geofence import geo_fence_dependency
from app.models.gate_pass.inward_gate_pass import InwardGatePass
from app.schemas.gate_pass.GatePass import AllGatePassListResponse,  InwardGatePassData, InwardGatePassUpdate, InwardMaterialDetailSchema
from app.utils.UserAuthUtils import verify_access_token  # check token
from app.crud.gate_pass.GatePassNotificationCrud import (
    notify_inward_approver_on_create,
    notify_inward_initiator_on_status_change,
)

router = APIRouter(prefix="/api/GatePass/IG", 
                    # dependencies=[Depends(geo_fence_dependency)],
                      tags=["IG GatePass"])
UPLOAD_ROOT = "files/gate_pass"
os.makedirs(UPLOAD_ROOT, exist_ok=True)
 


import urllib.parse
import urllib.parse


# def make_download_url(path: str) -> str:
#     if not path:
#         return None

#     base_url = os.getenv("BackEndPath")

#     # Normalize slashes
#     file_path = path.replace("\\", "/")

#     # 🔥 Remove domain if already present
#     file_path = file_path.replace(base_url, "")

#     # 🔥 Remove /app if present
#     file_path = file_path.replace("/app/files", "/files")

#     # 🔥 If absolute system path → convert to /files path
#     if "/files/" in file_path:
#         file_path = file_path[file_path.index("/files/"):]
#     else:
#         # fallback (just filename)
#         file_path = f"/files/gate_pass/{os.path.basename(file_path)}"

#     # Ensure proper format
#     file_path = "/" + file_path.lstrip("/")

#     # Encode special characters (but keep slashes safe)
#     encoded_path = urllib.parse.quote(file_path, safe="/")

#     return f"{base_url}{encoded_path}"



def make_download_url(path: str) -> str:
    if not path:
        return None

    base_url = os.getenv("BackEndPath")

    # Normalize slashes
    file_path = path.replace("\\", "/")

    # 🔥 Remove domain if already present
    file_path = file_path.replace(base_url, "")

    # 🔥 Remove /app if present
    file_path = file_path.replace("/app/files", "/files")

    # 🔥 If absolute system path → convert to /files path
    if "/files/" in file_path:
        file_path = file_path[file_path.index("/files/"):]
    else:
        # fallback (just filename)
        file_path = f"/files/gate_pass/{os.path.basename(file_path)}"

    # Ensure proper format
    file_path = "/" + file_path.lstrip("/")

    # Encode special characters (but keep slashes safe)
    encoded_path = urllib.parse.quote(file_path, safe="/")

    return f"{base_url}{encoded_path}"

@router.get("/IGgetby_id/{inward_id}")
def get_by_id(inward_id: int, db: Session = Depends(get_db)):
    result = get_inward_gate_pass_by_id(db, inward_id)
    if not result:
        raise HTTPException(status_code=404, detail="Gate pass not found")

    # ---- Extract nested data safely ----
    inward_data = result.get("get_inward_gate_pass_by_id", {})

    materials = inward_data.get("materials", [])
    photos = inward_data.get("photos", [])

    # ---- Convert materials goods_photo ----
    for m in materials:
        if m.get("goods_photo"):
            m["goods_photo"] = make_download_url(m["goods_photo"])

    # ---- Convert photos inside 'photos' list ----
    for p in photos:
        for key in [
            "vehicle_photo",
            "delivery_personnel_photo",
            "delivery_personnel_id_photo",
            "goods_photo",
        ]:
            if p.get(key):
                p[key] = make_download_url(p[key])

    return result


@router.get("/IGgetall/{user_id}")
def get_all(user_id: int, db: Session = Depends(get_db)):
    result = get_all_inward_gate_passes(db, user_id)
    if not result:
        raise HTTPException(status_code=404, detail="No records found")
    return result



from fastapi import UploadFile, File

@router.post("/IGgetcreate", summary="Create Inward Gate Pass (No Materials)")
async def create_inward_gate_pass_pg(
    background_tasks: BackgroundTasks,
    data: str = Form(...),
    vehicle_photo: Union[UploadFile, str, None] = File(None),
    delivery_personnel_photo: Union[UploadFile, str, None] = File(None),
    delivery_personnel_id_photo: Union[UploadFile, str, None] = File(None),
    goods_photo: Union[UploadFile, str, None] = File(None),
    db: Session = Depends(get_db),
):
    try:
        inward_json = json.loads(data)
        inward_data = InwardGatePassData(**inward_json).dict()
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid JSON format: {str(e)}")

    def save_file(file_obj: UploadFile | None):
        if not file_obj:
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

    try:
        inward_result = create_inward_gate_pass_crud(db, inward_data, file_paths)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

    # ✅ Extract actual integer ID from response dict
    actual_inward_id = inward_result.get("inward_id") if isinstance(inward_result, dict) else inward_result

    # Send notification to approver
    try:
        await notify_inward_approver_on_create(db, inward_data, actual_inward_id, background_tasks)
    except Exception as e:
        print(f"❌ Inward create notification error: {e}")

    return {
        "status": "success",
        "message": "Inward Gate Pass created successfully",
        "inward_id": inward_result,
    }


@router.put("/{inward_id}", summary="Update Inward Gate Pass")
async def update_inward(
    inward_id: int,
    background_tasks: BackgroundTasks,
    data: str = Form(...),
    vehicle_photo: Union[UploadFile, str, None] = File(None),
    delivery_personnel_photo: Union[UploadFile, str, None] = File(None),
    delivery_personnel_id_photo: Union[UploadFile, str, None] = File(None),
    goods_photo: Union[UploadFile, str, None] = File(None),
    db: Session = Depends(get_db)
):
    try:
        update_json = json.loads(data)
    except:
        raise HTTPException(status_code=400, detail="Invalid JSON input")

    def save(file):
        if file:
            path = os.path.join(UPLOAD_ROOT, file.filename)
            with open(path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
            return path.replace("\\", "/")
        return None

    # Add updated file paths if provided
    if vehicle_photo: update_json["vehicle_photo"] = save(vehicle_photo)
    if delivery_personnel_photo: update_json["delivery_personnel_photo"] = save(delivery_personnel_photo)
    if delivery_personnel_id_photo: update_json["delivery_personnel_id_photo"] = save(delivery_personnel_id_photo)
    if goods_photo: update_json["goods_photo"] = save(goods_photo)

    update_model = InwardGatePassUpdate(**update_json)

    result = update_inward_gate_pass_full(db, inward_id, update_model)

    # ✅ Notify creator when status is Approved or Rejected
    if update_model.status and update_model.status.strip().lower() in ("approved", "rejected"):
        try:
            # ✅ Fetch inward gate pass directly from DB
            inward = db.query(InwardGatePass).filter(
                InwardGatePass.inward_id == inward_id
            ).first()

            if inward:
                await notify_inward_initiator_on_status_change(
                    db=db,
                    inward_id=inward_id,
                    status=update_model.status,
                    gate_pass_no=inward.gate_pass_no or "",
                    created_by=inward.created_by or "",
                    updated_by=update_model.updated_by or "",
                    background_tasks=background_tasks,
                )
            else:
                print(f"⚠️ Inward gate pass {inward_id} not found for notification")

        except Exception as e:
            print(f"❌ Inward update notification error: {e}")

    return result


@router.get("/GetEngineersBySubmenuAndStation")
def get_engineers_by_submenu_and_station(
    station_id: int,
    db: Session = Depends(get_db),
):
    try:
        query = text("""
            SELECT DISTINCT
                u.user_id,
                u.username,
                u.first_name,
                u.last_name,
                u.email,
                u.station_id
            FROM users u
            JOIN role_permissions rp
                ON rp.user_id = u.user_id
            WHERE rp.role_id = 1
              AND rp.submenu_id = 5
              AND u.station_id = :station_id
              AND u.is_deleted = false
            ORDER BY u.first_name
        """)

        result = db.execute(query, {"station_id": station_id}).fetchall()

        data = []

        for row in result:
            f_name = row.first_name
            l_name = row.last_name

            # fallback if name missing
            if not f_name:
                clean_name = row.username.split('@')[0].replace('_', ' ').replace('.', ' ')
                parts = clean_name.split()
                if len(parts) > 0:
                    f_name = parts[0].capitalize()
                if len(parts) > 1:
                    l_name = " ".join(parts[1:]).title()

            data.append({
                "user_id": row.user_id,
                "username": row.username,
                "first_name": f_name,
                "last_name": l_name,
                "email": row.email,
                "station_id": row.station_id
            })

        return {
            "statusCode": "0000",
            "statusMessage": "Success",
            "data": data
        }

    except Exception as e:
        print("GET ENGINEERS BY STATION ERROR:", str(e))
        raise HTTPException(
            status_code=500,
            detail={
                "statusCode": "9999",
                "statusMessage": str(e),
                "data": []
            }
        )




@router.delete("/delete/{material_id}")
def delete_inward_material(material_id: int, db: Session = Depends(get_db)):

    # 🔹 Check if record exists
    check_query = text("""
        SELECT id 
        FROM inward_material_details 
        WHERE id = :material_id
    """)

    result = db.execute(check_query, {"material_id": material_id}).fetchone()

    if not result:
        raise HTTPException(status_code=404, detail="Material not found")

    # 🔹 Delete record
    delete_query = text("""
        DELETE FROM inward_material_details
        WHERE id = :material_id
    """)

    db.execute(delete_query, {"material_id": material_id})
    db.commit()

    return {
        "status_code": 200,
        "status_message": "Material deleted successfully",
        "deleted_id": material_id
    }
