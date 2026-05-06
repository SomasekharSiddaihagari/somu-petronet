import os
import shutil
import json
from datetime import datetime
from typing import List, Optional

from fastapi import UploadFile
from sqlalchemy.orm import Session

from app.models.claim.vehicle_cm_reimbursement import VehicleCMReimbursement
from app.models.claim.vehicle_cm_reimbursement_history import (
    VehicleCMReimbursementHistory
)
from app.schemas.claim.vehicle_cm_reimbursement_schema import (
    VehicleCMReimbursementCreate,
    VehicleCMReimbursementUpdate
)

UPLOAD_ROOT = "files/vehicle_cm_reimbursement"
os.makedirs(UPLOAD_ROOT, exist_ok=True)


# ---------- FILE SAVE ----------
def _save_documents(files: Optional[List[UploadFile]]):
    if not files:
        return None

    saved_files = []
    for file in files:
        ts = int(datetime.now().timestamp())
        filename = f"{ts}_{file.filename}"
        path = os.path.join(UPLOAD_ROOT, filename)

        with open(path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        saved_files.append(os.path.abspath(path).replace("\\", "/"))

    return json.dumps(saved_files)


# ---------- HISTORY ----------
def create_history(db: Session, record: VehicleCMReimbursement):
    history = VehicleCMReimbursementHistory(
        vehicle_cm_reimbursement_id=record.vehicle_cm_reimbursement_id,
        ra_claim_id=record.ra_claim_id,

        vehicle_name=record.vehicle_name,
        claim_month_year=record.claim_month_year,

        vehicle_no=record.vehicle_no,
        vehicle_type=record.vehicle_type,
        fuel_type=record.fuel_type,

        rc_expiry_date=record.rc_expiry_date,
        insurance_expiry_date=record.insurance_expiry_date,

        fuel_claim_amount=record.fuel_claim_amount,
        applicable_fuel_rate=record.applicable_fuel_rate,
        fuel_claimed_liters=record.fuel_claimed_liters,

        maintenance_claim_amount=record.maintenance_claim_amount,
        fixed_conveyance_claim=record.fixed_conveyance_claim,
        fixed_conveyance_claim_amount=record.fixed_conveyance_claim_amount,

        annual_entitlement_fuel=record.annual_entitlement_fuel,
        annual_entitlement_maintenance=record.annual_entitlement_maintenance,

        monthly_ceiling_fuel=record.monthly_ceiling_fuel,
        monthly_ceiling_maintenance=record.monthly_ceiling_maintenance,

        adjustment_previous_month_fuel=record.adjustment_previous_month_fuel,
        adjustment_previous_month_maintenance=record.adjustment_previous_month_maintenance,

        net_available_balance_fuel=record.net_available_balance_fuel,
        net_available_balance_maintenance=record.net_available_balance_maintenance,

        max_claim_allowed_fuel=record.max_claim_allowed_fuel,
        max_claim_allowed_maintenance=record.max_claim_allowed_maintenance,

        document_names=record.document_names,
        remarks=record.remarks,
        declaration_accepted=record.declaration_accepted,
        status=record.status,

        updated_by_supervisor=record.updated_by_supervisor,
        updated_by_supervisor_name=record.updated_by_supervisor_name,
        supervisor_comment=record.supervisor_comment,

        updated_by_hr=record.updated_by_hr,
        updated_by_hr_name=record.updated_by_hr_name,
        hr_comment=record.hr_comment,

        updated_by_finance=record.updated_by_finance,
        updated_by_finance_name=record.updated_by_finance_name,
        finance_comment=record.finance_comment,

        created_by=record.created_by
    )
    db.add(history)


# ---------- POST ----------
def create_vehicle_cm_reimbursement(
    db: Session,
    payload: VehicleCMReimbursementCreate,
    documents: Optional[List[UploadFile]] = None
):
    doc_paths = _save_documents(documents)

    record = VehicleCMReimbursement(
        **payload.dict(exclude={"document_names"}),
        document_names=doc_paths
    )

    db.add(record)
    db.commit()
    db.refresh(record)

    create_history(db, record)
    db.commit()

    return record


# ---------- PUT ----------
def update_vehicle_cm_reimbursement(
    db: Session,
    reimbursement_id: int,
    payload: VehicleCMReimbursementUpdate,
    documents: Optional[List[UploadFile]] = None
):
    record = (
        db.query(VehicleCMReimbursement)
        .filter(
            VehicleCMReimbursement.vehicle_cm_reimbursement_id
            == reimbursement_id
        )
        .first()
    )

    if not record:
        return None

    create_history(db, record)

    for key, value in payload.dict(exclude_unset=True).items():
        setattr(record, key, value)

    if documents:
        record.document_names = _save_documents(documents)

    db.commit()
    db.refresh(record)
    return record
