import os
import shutil
import json
from datetime import datetime
from typing import List, Optional

from fastapi import UploadFile
from sqlalchemy.orm import Session

from app.models.claim.laptop_maintenance_reimbursement import (
    LaptopMaintenanceReimbursement
)
from app.models.claim.laptop_maintenance_reimbursement_history import (
    LaptopMaintenanceReimbursementHistory
)
from app.schemas.claim.laptop_maintenance_reimbursement_schema import (
    LaptopMaintenanceReimbursementCreate,
    LaptopMaintenanceReimbursementUpdate
)

UPLOAD_ROOT = "files/laptop_maintenance_reimbursement"
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
def create_history(db: Session, record: LaptopMaintenanceReimbursement):
    history = LaptopMaintenanceReimbursementHistory(
        laptop_maintenance_reimbursement_id=record.laptop_maintenance_reimbursement_id,
        ra_claim_id=record.ra_claim_id,

        date_of_purchase=record.date_of_purchase,
        date_of_claim=record.date_of_claim,
        date_of_previous_claim=record.date_of_previous_claim,

        amount_claimed=record.amount_claimed,
        annual_limit=record.annual_limit,
        eligible_amount=record.eligible_amount,

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
def create_laptop_maintenance_reimbursement(
    db: Session,
    payload: LaptopMaintenanceReimbursementCreate,
    documents: Optional[List[UploadFile]] = None
):
    doc_paths = _save_documents(documents)

    record = LaptopMaintenanceReimbursement(
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
def update_laptop_maintenance_reimbursement(
    db: Session,
    reimbursement_id: int,
    payload: LaptopMaintenanceReimbursementUpdate,
    documents: Optional[List[UploadFile]] = None
):
    record = (
        db.query(LaptopMaintenanceReimbursement)
        .filter(
            LaptopMaintenanceReimbursement.laptop_maintenance_reimbursement_id
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
