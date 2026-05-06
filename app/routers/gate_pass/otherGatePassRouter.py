import json
import os
import shutil
from typing import Literal, Optional
from click import File
from fastapi import (
    APIRouter, Depends, UploadFile, File as FastAPIFile, Form, HTTPException
)
from fastapi import APIRouter, Depends, Form, HTTPException, HTTPException, Query, UploadFile
from sqlalchemy import text
from sqlalchemy.orm import Session
from app.crud.gate_pass.igGatePassCrud import create_inward_gate_pass_crud, get_all_gate_pass_by_user, get_all_inward_gate_passes, get_cardData_crud,  get_gatepass_by_formtype, get_inward_gate_pass_by_id, update_inward_gate_pass_full
from app.database import get_db
from app.schemas.gate_pass.GatePass import AllGatePassListResponse,  InwardGatePassData, InwardGatePassUpdate
from app.utils.UserAuthUtils import verify_access_token  # check token

router = APIRouter(prefix="/api/GatePass/other", tags=["Other GatePass"])
UPLOAD_ROOT = "files/gate_pass"

os.makedirs(UPLOAD_ROOT, exist_ok=True)
@router.get("/user/{user_id}", response_model=AllGatePassListResponse)
def get_all_gate_passes(user_id: int, db: Session = Depends(get_db)):
    result = get_all_gate_pass_by_user(db, user_id)
    if not result:
        raise HTTPException(status_code=404, detail="No data found")
    return result



@router.get("/details-by-formtype")
def api_get_gatepass_by_formtype(
    formtype: Literal["inward", "outward", "returnable"],
    id: int = Query(..., description="Primary ID of the record"),
    gatepass_no: Optional[str] = Query(None, description="Required only for inward"),
    db: Session = Depends(get_db)
):
    """
    Universal endpoint to fetch:
    - Inward gate pass
    - Outward gate pass
    - Returnable gate pass
    based on formtype + id (+ gatepass_no for inward)
    """

    result = get_gatepass_by_formtype(
        db=db,
        formtype=formtype,
        id=id,
        gatepass_no=gatepass_no
    )

    if not result:
        raise HTTPException(status_code=500, detail="Database returned no result")

    return result




@router.get("/CardData")
def get_gatepass_summary(user_id: int, db: Session = Depends(get_db)):
    return get_cardData_crud(db, user_id)


