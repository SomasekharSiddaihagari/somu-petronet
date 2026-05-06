# ================================
# ROUTER FILE
# wah_electrical_isolation_router.py
# ================================

from fastapi import APIRouter, Depends, UploadFile, File, Form
from sqlalchemy.orm import Session
from sqlalchemy.sql import text
import os, uuid

from app.database import get_db
from app.schemas.permit_management.wah_electrical_isolation_schema import (
    WorkAtHeightElectricalIsolationCreate,
    WorkAtHeightElectricalIsolationUpdate
)

from app.crud.permit_management.wah_electrical_isolation_crud import (
    create_wah_electrical_isolation,
    update_wah_electrical_isolation,
    generate_eip_serial_number
)

router = APIRouter(
    prefix="/work-at-height/electrical-isolation",
    tags=["WAH Electrical Isolation Permit"]
)

UPLOAD_DIR = "files/wah/electrical_isolation"


def _save_file(file: UploadFile, whpis_id: int):
    os.makedirs(UPLOAD_DIR, exist_ok=True)

    ext = os.path.splitext(file.filename)[1]
    fname = f"{whpis_id}_{uuid.uuid4().hex}{ext}"

    path = os.path.join(UPLOAD_DIR, fname)

    with open(path, "wb") as f:
        f.write(file.file.read())

    return f"/files/wah/electrical_isolation/{fname}"


# ==========================================
# SERIAL PREVIEW API FIX
# wah_electrical_isolation_router.py
# ==========================================

@router.get("/generate-serial/{user_id}")
def get_wah_ei_serial_preview(
    user_id: int,
    db: Session = Depends(get_db)
):
    serial = generate_eip_serial_number(
        db,
        user_id,
        "work_at_height_electrical_isolation_permit"
    )

    return {
        "work_permit_number": serial
    }

# ==========================================
# CREATE
# ==========================================
@router.post("")
def create_api(
    whp_id: int = Form(...),
    work_clearance_time: str = Form(None),
    work_clearance_date: str = Form(None),
    cross_reference_of_other_permit: str = Form(None),
    department_section_area: str = Form(None),
    equipment_number_to_be_isolated: str = Form(None),
    name_of_equipment_circuit: str = Form(None),
    description_of_work: str = Form(None),

    equipment_circuit_no: str = Form(None),
    plant: str = Form(None),
    work_clearance_from_time: str = Form(None),
    work_clearance_from_date: str = Form(None),
    loto_tag_device_no: str = Form(None),
    authorized_person_name: str = Form(None),
    designation: str = Form(None),
    signature: str = Form(None),
    isolation_method: str = Form(None),

    issuer_name: str = Form(None),
    issuer_designation: str = Form(None),
    created_by: int = Form(...),

    issuer_signature_file: UploadFile = File(None),

    db: Session = Depends(get_db)
):
    payload = {
        "whp_id": whp_id,
        "work_clearance_time": work_clearance_time,
        "work_clearance_date": work_clearance_date,
        "cross_reference_of_other_permit": cross_reference_of_other_permit,
        "department_section_area": department_section_area,
        "equipment_number_to_be_isolated": equipment_number_to_be_isolated,
        "name_of_equipment_circuit": name_of_equipment_circuit,
        "description_of_work": description_of_work,

        "equipment_circuit_no": equipment_circuit_no,
        "plant": plant,
        "work_clearance_from_time": work_clearance_from_time,
        "work_clearance_from_date": work_clearance_from_date,
        "loto_tag_device_no": loto_tag_device_no,
        "authorized_person_name": authorized_person_name,
        "designation": designation,
        "signature": signature,
        "isolation_method": isolation_method,

        "issuer_name": issuer_name,
        "issuer_designation": issuer_designation,
        "issuer_signature": None,
        "created_by": created_by
    }

    obj = WorkAtHeightElectricalIsolationCreate(**payload)

    result = create_wah_electrical_isolation(db, obj)

    whpis_id = result["whpis_id"]

    if issuer_signature_file:
        file_path = _save_file(
            issuer_signature_file,
            whpis_id
        )

        db.execute(text("""
            UPDATE work_at_height_electrical_isolation_permit
            SET issuer_signature = :path
            WHERE whpis_id = :id
        """), {
            "path": file_path,
            "id": whpis_id
        })

        db.commit()

    return {
        "message": "Created Successfully",
        **result
    }


# ==========================================
# UPDATE
# ==========================================
# ==========================================
# UPDATE
# ==========================================
@router.put("/{whpis_id}")
def update_api(
    whpis_id: int,

    equipment_circuit_no: str = Form(None),
    plant: str = Form(None),

    work_clearance_from_time: str = Form(None),
    work_clearance_from_date: str = Form(None),

    loto_tag_device_no: str = Form(None),
    authorized_person_name: str = Form(None),
    designation: str = Form(None),
    signature: str = Form(None),
    isolation_method: str = Form(None),

    issuer_name: str = Form(None),
    issuer_designation: str = Form(None),

    issuer_signature_file: UploadFile = File(None),

    db: Session = Depends(get_db)
):
    payload = {}

    for k, v in {
        "equipment_circuit_no": equipment_circuit_no,
        "plant": plant,
        "work_clearance_from_time": work_clearance_from_time,
        "work_clearance_from_date": work_clearance_from_date,
        "loto_tag_device_no": loto_tag_device_no,
        "authorized_person_name": authorized_person_name,
        "designation": designation,
        "signature": signature,
        "isolation_method": isolation_method,
        "issuer_name": issuer_name,
        "issuer_designation": issuer_designation
    }.items():
        if v is not None:
            payload[k] = v

    if payload:
        obj = WorkAtHeightElectricalIsolationUpdate(**payload)

        update_wah_electrical_isolation(
            db,
            whpis_id,
            obj
        )

    if issuer_signature_file:
        file_path = _save_file(
            issuer_signature_file,
            whpis_id
        )

        db.execute(text("""
            UPDATE work_at_height_electrical_isolation_permit
            SET issuer_signature = :path
            WHERE whpis_id = :id
        """), {
            "path": file_path,
            "id": whpis_id
        })

        db.commit()

    return {
        "message": "Updated Successfully",
        "whpis_id": whpis_id
    }