from fastapi import APIRouter, Depends, UploadFile, File
from sqlalchemy.orm import Session
from sqlalchemy.sql import text
import os, uuid

from app.database import get_db
from app.schemas.permit_management.cwp_schema_master import (
    CompositeWorkPermitCreate,
    CompositeWorkPermitUpdate,
)
from app.crud.permit_management.cwp_crud_master import create_cwp, update_cwp

router = APIRouter(prefix="/cwp", tags=["Composite Work Permit"])

UPLOAD_DIR = "files/cwp/signatures"


def _save_signature(file: UploadFile, cwp_id: int, name: str) -> str:
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    ext = os.path.splitext(file.filename)[1]
    fname = f"cwp_{cwp_id}_{name}_{uuid.uuid4().hex}{ext}"
    path = os.path.join(UPLOAD_DIR, fname)

    with open(path, "wb") as f:
        f.write(file.file.read())

    return f"/files/cwp/signatures/{fname}"


# =================================================
# GET SERIAL NUMBER (FORM LOAD - PREVIEW)
# =================================================
@router.get("/generate-serial/{user_id}", summary="Get CWP Serial Number Before Submit")
def get_cwp_serial_preview(user_id: int, db: Session = Depends(get_db)):
    from app.crud.permit_management.cwp_crud_master import generate_cwp_serial_number

    serial_number = generate_cwp_serial_number(db, user_id)

    return {"serial_number": serial_number}


# =================================================
# POST (STEP 1: DATA ONLY)
# =================================================
@router.post("", summary="Create CWP (Data Only)")
def create_cwp_api(
    payload: CompositeWorkPermitCreate,
    db: Session = Depends(get_db),
):
    result = create_cwp(db, payload)
    return result


# =================================================
# PUT (STEP 1: UPDATE DATA ONLY)
# =================================================
@router.put("/{cwp_id}", summary="Update CWP (Data Only)")
def update_cwp_api(
    cwp_id: int,
    payload: CompositeWorkPermitUpdate,
    db: Session = Depends(get_db),
):
    update_cwp(db, cwp_id, payload)
    return {"message": "CWP data updated successfully", "cwp_id": cwp_id}


# =================================================
# POST (STEP 2: UPLOAD SIGNATURES)
# =================================================
@router.post("/{cwp_id}/signatures", summary="Upload CWP Signatures")
def upload_cwp_signatures(
    cwp_id: int,
    requestor_signature_file: UploadFile = File(None),
    issuer_signature_file: UploadFile = File(None),
    receiver_signature_file: UploadFile = File(None),
    gas_requestor_signature_file: UploadFile = File(None),
    gas_issuer_signature_file: UploadFile = File(None),
    gas_receiver_signature_file: UploadFile = File(None),
    closure_requestor_signature_file: UploadFile = File(None),
    closure_issuer_signature_file: UploadFile = File(None),
    closure_receiver_signature_file: UploadFile = File(None),
    db: Session = Depends(get_db),
):
    from app.crud.permit_management.cwp_crud_master import insert_cwp_history

    updates = {}
    file_map = {
        "requestor_signature": requestor_signature_file,
        "issuer_signature": issuer_signature_file,
        "receiver_signature": receiver_signature_file,
        "gas_requestor_signature": gas_requestor_signature_file,
        "gas_issuer_signature": gas_issuer_signature_file,
        "gas_receiver_signature": gas_receiver_signature_file,
        "closure_requestor_signature": closure_requestor_signature_file,
        "closure_issuer_signature": closure_issuer_signature_file,
        "closure_receiver_signature": closure_receiver_signature_file,
    }

    for col, file in file_map.items():
        if file:
            updates[col] = _save_signature(file, cwp_id, col)

    if updates:
        set_clause = ", ".join([f"{k} = :{k}" for k in updates])
        sql = text(
            f"""
            UPDATE composite_work_permit
            SET {set_clause},
                updated_at = NOW()
            WHERE cwp_id = :cwp_id
        """
        )
        updates["cwp_id"] = cwp_id
        db.execute(sql, updates)
        
        # ✅ Take a history snapshot AFTER signatures are saved
        insert_cwp_history(db, cwp_id)
        db.commit()

    return {"cwp_id": cwp_id, "signatures": updates}
