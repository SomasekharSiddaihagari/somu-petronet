import json
import os
import shutil
from typing import List, Optional
from fastapi import File
from fastapi import (
    APIRouter, Depends, UploadFile, File as FastAPIFile, Form, HTTPException
)
from fastapi import APIRouter, Depends, Form, HTTPException, HTTPException, Query, UploadFile
from sqlalchemy import text
from sqlalchemy.orm import Session
from app.crud.gate_pass import materialigGatePassCrud
from app.database import get_db
from app.schemas.gate_pass.GatePass import InwardMaterialDetailsRequest, InwardMaterialDetailsResponse, OutwardMaterialDetailsRequest, OutwardMaterialDetailsResponse, ReturnableMaterialDetailCreate, ReturnableMaterialDetailUpdate
from app.utils.UserAuthUtils import verify_access_token  # check token



router = APIRouter(prefix="/api/GatePass/MG", tags=["MATERIAL GatePass"])
UPLOAD_ROOT = "files/gate_pass"
os.makedirs(UPLOAD_ROOT, exist_ok=True)



@router.post("/CreateIGPMaterial", response_model=InwardMaterialDetailsResponse)
async def create_inward_material(
    request: str = Form(...),
    goods_photo: List[UploadFile] = File(...),
    db: Session = Depends(get_db),
):
    try:
        data = json.loads(request)
        data_list = data if isinstance(data, list) else [data]

        if len(data_list) != len(goods_photo):
            raise HTTPException(status_code=400, detail="Number of materials and photos must match")

        results = []
        for i, photo in enumerate(goods_photo):
            req = InwardMaterialDetailsRequest(**data_list[i])
            result = materialigGatePassCrud.insert_invert_material_details_crud(db, req, photo)
            if "error" in result:
                raise HTTPException(status_code=400, detail=result["error"])
            results.append(result["message"])

        # ✅ Return a single dict with list inside
        return {
            "status_code": 200,
            "status_message": "Materials added successfully",
            "data": {"inserted": results}  # wrap list in a dict
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/CreateOGPMaterial", response_model=OutwardMaterialDetailsResponse)
async def create_outward_material(
    request: str = Form(...),  # JSON string
    goods_photo: UploadFile = File(...),
    db: Session = Depends(get_db),
    # current_user: str = Depends(verify_access_token)
):
    """
    ```json
    {
        "outward_id": number_id,
        "description": "string",
        "quantity": decimal,
        "unit": "string",
        "returnable": boolean,
        "returnable_date": returnable ? date : null,
        "remarks": "string"
    }
    request -> All text fields
    goods_photo -> upload a photo
    """
    try:
        # 1️ Parse JSON string into Python dict
        data = json.loads(request)
        req = OutwardMaterialDetailsRequest(**data)
 
        # 2️ Call CRUD
        result = materialigGatePassCrud.insert_outward_material_details_crud(db, req, goods_photo)
 
        if "error" in result:
            raise HTTPException(status_code=400, detail=result["error"])
 
        return result["message"]
 
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))






@router.post("/CreateReturnableRGPMaterial", summary="Create a new Returnable Material Detail")
def create_detail(
    payload: ReturnableMaterialDetailCreate,
    db: Session = Depends(get_db),
    # current_user: dict = Depends(verify_access_token)
):
    return materialigGatePassCrud.create_returnable_material_detail(db, payload.dict())
 
 
@router.get("/GetReturnableRGPMaterial", summary="Get all or single Returnable Material Details")
def get_details(
    id: Optional[int] = None,
    db: Session = Depends(get_db),
    #current_user: dict = Depends(verify_access_token)
):
    return materialigGatePassCrud.get_returnable_material_details(db, id)
 
 
@router.put("/UpdateReturnableRGPMaterial{id}", summary="Update Returnable Material Detail")
def update_detail(
    id: int,
    payload: ReturnableMaterialDetailUpdate,
    db: Session = Depends(get_db),
    # current_user: dict = Depends(verify_access_token)
):
    return materialigGatePassCrud.update_returnable_material_detail(db, id, payload.dict())
 