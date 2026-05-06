from fastapi import APIRouter, Depends, UploadFile, File, Form
from sqlalchemy.orm import Session
from sqlalchemy.sql import text
import os, uuid

from app.database import get_db
from app.schemas.permit_management.composite_electrical_energization_schema import (
    CompositeElectricalEnergizationPermitCreate,
    CompositeElectricalEnergizationPermitUpdate
)
from app.crud.permit_management.composite_electrical_energization_crud import (
    create_electrical_energization,
    update_electrical_energization
)

router = APIRouter(
    prefix="/composite-electrical-energization",
    tags=["Composite Electrical Energization Permit"]
)

UPLOAD_DIR = "files/cwp/electrical_energization"


# =================================================
# HELPER — SAVE SIGNATURE
# =================================================
def _save_issuer_signature(file: UploadFile, ceep_id: int) -> str:
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    ext = os.path.splitext(file.filename)[1]
    fname = f"ceep_{ceep_id}_{uuid.uuid4().hex}{ext}"
    path = os.path.join(UPLOAD_DIR, fname)

    with open(path, "wb") as f:
        f.write(file.file.read())

    return f"/files/cwp/electrical_energization/{fname}"

# =================================================
# GET SERIAL NUMBER (FORM LOAD - PREVIEW)
# =================================================
@router.get("/generate-serial/{user_id}", summary="Get CEEP Serial Number Before Submit")
def get_ceep_serial_preview(
    user_id: int,
    db: Session = Depends(get_db)
):
    from app.crud.permit_management.composite_electrical_energization_crud import generate_composite_eep_serial_number

    serial_number = generate_composite_eep_serial_number(db, user_id)

    return {
        "work_permit_number": serial_number
    }


# =================================================
# POST — CREATE + SIGNATURE
# =================================================
@router.post("", summary="Create Electrical Energization Permit")
def create_ceep(
    composite_work_permit_id: int = Form(...),

    work_permit_number: str = Form(None),
    work_clearance_time: str = Form(None),
    work_clearance_date: str = Form(None),

    name_of_equipment_circuit: str = Form(None),
    department_section_area: str = Form(None),
    equipment_number_to_be_energized: str = Form(None),
    cross_reference_of_other_permit: str = Form(None),

    issuer_name: str = Form(None),
    issuer_designation: str = Form(None),
    status: str = Form(None),
    created_by: str = Form(None),

    # ELECTRICAL certificate fields
    equipment_circuit_no: str = Form(None),
    plant: str = Form(None),
    work_clearance_from_time: str = Form(None),
    work_clearance_from_date: str = Form(None),
    energization_method: str = Form(None),
    loto_tag_device_no: str = Form(None),
    authorized_person_name: str = Form(None),
    designation: str = Form(None),

    issuer_signature_file: UploadFile = File(None),
    signature_file: UploadFile = File(None),

    db: Session = Depends(get_db)
):
    payload = CompositeElectricalEnergizationPermitCreate(
        composite_work_permit_id=composite_work_permit_id,
        work_permit_number=work_permit_number,
        work_clearance_time=work_clearance_time,
        work_clearance_date=work_clearance_date,
        name_of_equipment_circuit=name_of_equipment_circuit,
        department_section_area=department_section_area,
        equipment_number_to_be_energized=equipment_number_to_be_energized,
        cross_reference_of_other_permit=cross_reference_of_other_permit,
        issuer_name=issuer_name,
        issuer_designation=issuer_designation,
        status=status,
        created_by=created_by,

        equipment_circuit_no=equipment_circuit_no,
        plant=plant,
        work_clearance_from_time=work_clearance_from_time,
        work_clearance_from_date=work_clearance_from_date,
        energization_method=energization_method,
        loto_tag_device_no=loto_tag_device_no,
        authorized_person_name=authorized_person_name,
        designation=designation,
    )

    result = create_electrical_energization(db, payload)
    ceep_id = result["ceep_id"]

    updates = {}

    if issuer_signature_file:
        updates["issuer_signature"] = _save_issuer_signature(
            issuer_signature_file, ceep_id
        )
    
    if signature_file:
        updates["signature"] = _save_issuer_signature(
            signature_file, ceep_id
        )

    if updates:
        set_clause = ", ".join([f"{k} = :{k}" for k in updates])
        sql = text(f"""
            UPDATE composite_electrical_energization_permit
            SET {set_clause}
            WHERE ceep_id = :ceep_id
        """)
        params = {**updates, "ceep_id": ceep_id}
        db.execute(sql, params)
        db.commit()

    return {
        "message": "Electrical Energization Permit created",
        "ceep_id": ceep_id,
        **updates
    }


# =================================================
# PUT — UPDATE + SIGNATURE
# =================================================
@router.put("/{ceep_id}", summary="Update Electrical Energization Permit")
def update_ceep(
    ceep_id: int,

    work_permit_number: str = Form(None),
    work_clearance_time: str = Form(None),
    work_clearance_date: str = Form(None),

    name_of_equipment_circuit: str = Form(None),
    department_section_area: str = Form(None),
    equipment_number_to_be_energized: str = Form(None),
    cross_reference_of_other_permit: str = Form(None),

    issuer_name: str = Form(None),
    issuer_designation: str = Form(None),
    status: str = Form(None),

    # ELECTRICAL certificate fields
    equipment_circuit_no: str = Form(None),
    plant: str = Form(None),
    work_clearance_from_time: str = Form(None),
    work_clearance_from_date: str = Form(None),
    energization_method: str = Form(None),
    loto_tag_device_no: str = Form(None),
    authorized_person_name: str = Form(None),
    designation: str = Form(None),

    issuer_signature_file: UploadFile = File(None),
    signature_file: UploadFile = File(None),

    db: Session = Depends(get_db)
):
    payload = CompositeElectricalEnergizationPermitUpdate(
        work_permit_number=work_permit_number,
        work_clearance_time=work_clearance_time,
        work_clearance_date=work_clearance_date,
        name_of_equipment_circuit=name_of_equipment_circuit,
        department_section_area=department_section_area,
        equipment_number_to_be_energized=equipment_number_to_be_energized,
        cross_reference_of_other_permit=cross_reference_of_other_permit,
        issuer_name=issuer_name,
        issuer_designation=issuer_designation,
        status=status,

        equipment_circuit_no=equipment_circuit_no,
        plant=plant,
        work_clearance_from_time=work_clearance_from_time,
        work_clearance_from_date=work_clearance_from_date,
        energization_method=energization_method,
        loto_tag_device_no=loto_tag_device_no,
        authorized_person_name=authorized_person_name,
        designation=designation,
    )

    update_electrical_energization(db, ceep_id, payload)

    updates = {}

    if issuer_signature_file:
        updates["issuer_signature"] = _save_issuer_signature(
            issuer_signature_file, ceep_id
        )

    if signature_file:
        updates["signature"] = _save_issuer_signature(
            signature_file, ceep_id
        )

    if updates:
        set_clause = ", ".join([f"{k} = :{k}" for k in updates])
        sql = text(f"""
            UPDATE composite_electrical_energization_permit
            SET {set_clause}
            WHERE ceep_id = :ceep_id
        """)
        params = {**updates, "ceep_id": ceep_id}
        db.execute(sql, params)
        db.commit()

    return {
        "message": "Electrical Energization Permit updated",
        "ceep_id": ceep_id,
        **updates
    }
