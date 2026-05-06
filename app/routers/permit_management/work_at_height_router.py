from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from sqlalchemy.sql import text
import os, uuid

from app.database import get_db
from app.schemas.permit_management.work_at_height_schema import (
    WorkAtHeightPermitCreate,
    WorkAtHeightPermitUpdate
)
from app.crud.permit_management.work_at_height_crud import (
    create_work_at_height,
    update_work_at_height
)

router = APIRouter(
    prefix="/work-at-height",
    tags=["Work At Height Permit"]
)

UPLOAD_DIR = "files/work_at_height"


def _save_file(file: UploadFile, whp_id: int, name: str) -> str:
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    ext = os.path.splitext(file.filename)[1]
    fname = f"whp_{whp_id}_{name}_{uuid.uuid4().hex}{ext}"
    path = os.path.join(UPLOAD_DIR, fname)
    with open(path, "wb") as f:
        f.write(file.file.read())
    return f"/files/work_at_height/{fname}"


# =================================================
# GET SERIAL NUMBER (FORM LOAD)
# =================================================
@router.get("/generate-serial/{user_id}", summary="Get Serial Number Before Submit")
def get_serial_number_preview(
    user_id: int,
    db: Session = Depends(get_db)
):
    from app.crud.permit_management.work_at_height_crud import generate_serial_number
    return {"serial_number": generate_serial_number(db, user_id)}


# =================================================
# POST
# =================================================
@router.post("", summary="Create Work At Height Permit")
def create_whp(
    payload: WorkAtHeightPermitCreate = Depends(),

    issuer_signature_file: UploadFile = File(None),
    receiver_signature_file: UploadFile = File(None),

    # NEW
    requestor_signature_file: UploadFile = File(None),

    renewal_issuer_signature_file: UploadFile = File(None),
    renewal_receiver_signature_file: UploadFile = File(None),
    renewal_requestor_signature_file: UploadFile = File(None),   # NEW

    closure_issuer_signature_file: UploadFile = File(None),
    closure_receiver_signature_file: UploadFile = File(None),
    closure_requestor_signature_file: UploadFile = File(None),   # NEW

    db: Session = Depends(get_db)
):
    result = create_work_at_height(db, payload)
    whp_id = result["whp_id"]

    updates = {}

    file_map = {
        "issuer_signature":               issuer_signature_file,
        "receiver_signature":             receiver_signature_file,
        "requestor_signature":            requestor_signature_file,           # NEW
        "renewal_issuer_signature":       renewal_issuer_signature_file,
        "renewal_receiver_signature":     renewal_receiver_signature_file,
        "renewal_requestor_signature":    renewal_requestor_signature_file,   # NEW
        "closure_issuer_signature":       closure_issuer_signature_file,
        "closure_receiver_signature":     closure_receiver_signature_file,
        "closure_requestor_signature":    closure_requestor_signature_file,   # NEW
    }

    for col, file in file_map.items():
        if file:
            updates[col] = _save_file(file, whp_id, col)

    if updates:
        set_clause = ", ".join([f"{k} = :{k}" for k in updates])
        sql = text(f"""
            UPDATE work_at_height_permit
            SET {set_clause}, updated_at = NOW()
            WHERE whp_id = :whp_id
        """)
        updates["whp_id"] = whp_id
        db.execute(sql, updates)
        db.commit()

    return {"whp_id": whp_id, **updates}


# =================================================
# PUT
# =================================================
@router.put("/{whp_id}", summary="Update Work At Height Permit")
def update_whp(
    whp_id: int,
    payload: WorkAtHeightPermitUpdate = Depends(),

    issuer_signature_file: UploadFile = File(None),
    receiver_signature_file: UploadFile = File(None),

    requestor_signature_file: UploadFile = File(None),             # NEW

    renewal_issuer_signature_file: UploadFile = File(None),
    renewal_receiver_signature_file: UploadFile = File(None),
    renewal_requestor_signature_file: UploadFile = File(None),     # NEW

    closure_issuer_signature_file: UploadFile = File(None),
    closure_receiver_signature_file: UploadFile = File(None),
    closure_requestor_signature_file: UploadFile = File(None),     # NEW

    db: Session = Depends(get_db)
):
    update_work_at_height(db, whp_id, payload)

    updates = {}

    file_map = {
        "issuer_signature":               issuer_signature_file,
        "receiver_signature":             receiver_signature_file,
        "requestor_signature":            requestor_signature_file,           # NEW
        "renewal_issuer_signature":       renewal_issuer_signature_file,
        "renewal_receiver_signature":     renewal_receiver_signature_file,
        "renewal_requestor_signature":    renewal_requestor_signature_file,   # NEW
        "closure_issuer_signature":       closure_issuer_signature_file,
        "closure_receiver_signature":     closure_receiver_signature_file,
        "closure_requestor_signature":    closure_requestor_signature_file,   # NEW
    }

    for col, file in file_map.items():
        if file:
            updates[col] = _save_file(file, whp_id, col)

    if updates:
        set_clause = ", ".join([f"{k} = :{k}" for k in updates])
        sql = text(f"""
            UPDATE work_at_height_permit
            SET {set_clause}, updated_at = NOW()
            WHERE whp_id = :whp_id
        """)
        updates["whp_id"] = whp_id
        db.execute(sql, updates)
        db.commit()

    return {"whp_id": whp_id, **updates}
