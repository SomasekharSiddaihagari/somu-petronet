# ==========================================================
# ROUTER FILE
# app/router/permit_management/wah_electrical_energization_router.py
# ==========================================================

from fastapi import APIRouter, Depends, UploadFile, File
from sqlalchemy.orm import Session
from sqlalchemy.sql import text
import os
import uuid

from app.database import get_db

from app.schemas.permit_management.wah_electrical_energization_schema import (
    WorkAtHeightElectricalEnergizationCreate,
    WorkAtHeightElectricalEnergizationUpdate
)

from app.crud.permit_management.wah_electrical_energization_crud import (
    create_wah_electrical_energization,
    update_wah_electrical_energization,
    generate_wah_eep_serial_number
)

router = APIRouter(
    prefix="/wah-electrical-energization",
    tags=["Work At Height - Electrical Energization"]
)

UPLOAD_DIR = "files/work_at_height/electrical_energization"


# =================================================
# FILE SAVE
# =================================================
def _save_signature(
    file: UploadFile,
    whpep_id: int
):
    os.makedirs(UPLOAD_DIR, exist_ok=True)

    ext = os.path.splitext(file.filename)[1]
    fname = f"whpep_{whpep_id}_{uuid.uuid4().hex}{ext}"

    path = os.path.join(UPLOAD_DIR, fname)

    with open(path, "wb") as f:
        f.write(file.file.read())

    return f"/files/work_at_height/electrical_energization/{fname}"


# =================================================
# SERIAL PREVIEW
# =================================================
@router.get("/generate-serial/{user_id}")
def get_wah_eep_serial_preview(
    user_id: int,
    db: Session = Depends(get_db)
):
    serial = generate_wah_eep_serial_number(db, user_id)

    return {"work_permit_number": serial}


# =================================================
# CREATE
# =================================================
@router.post("")
def create_wah_electrical_energization_api(
    payload: WorkAtHeightElectricalEnergizationCreate = Depends(),
    issuer_signature_file: UploadFile = File(None),
    db: Session = Depends(get_db)
):
    result = create_wah_electrical_energization(db, payload)

    whpep_id = result["whpep_id"]

    updates = {}

    if issuer_signature_file:
        updates["issuer_signature"] = _save_signature(
            issuer_signature_file,
            whpep_id
        )

    if updates:
        set_clause = ", ".join(
            [f"{k}=:{k}" for k in updates]
        )

        sql = text(f"""
            UPDATE work_at_height_electrical_energization_permit
            SET {set_clause},
                updated_at = NOW()
            WHERE whpep_id = :whpep_id
        """)

        updates["whpep_id"] = whpep_id

        db.execute(sql, updates)
        db.commit()

    return {
        "message": "Created Successfully",
        **result
    }


# =================================================
# UPDATE
# =================================================
@router.put("/{whpep_id}")
def update_wah_electrical_energization_api(
    whpep_id: int,
    payload: WorkAtHeightElectricalEnergizationUpdate = Depends(),
    issuer_signature_file: UploadFile = File(None),
    db: Session = Depends(get_db)
):
    update_wah_electrical_energization(
        db,
        whpep_id,
        payload
    )

    updates = {}

    if issuer_signature_file:
        updates["issuer_signature"] = _save_signature(
            issuer_signature_file,
            whpep_id
        )

    if updates:
        set_clause = ", ".join(
            [f"{k}=:{k}" for k in updates]
        )

        sql = text(f"""
            UPDATE work_at_height_electrical_energization_permit
            SET {set_clause},
                updated_at = NOW()
            WHERE whpep_id = :whpep_id
        """)

        updates["whpep_id"] = whpep_id

        db.execute(sql, updates)
        db.commit()

    return {
        "message": "Updated Successfully",
        "whpep_id": whpep_id
    }