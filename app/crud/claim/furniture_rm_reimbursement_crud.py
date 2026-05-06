import os
import shutil
import json
from datetime import datetime
from typing import List, Optional

from fastapi import UploadFile
from sqlalchemy.orm import Session

from app.models.claim.furniture_rm_reimbursement import FurnitureRMReimbursement
from app.models.claim.furniture_rm_reimbursement_history import (
    FurnitureRMReimbursementHistory
)
from app.schemas.claim.furniture_rm_reimbursement_schema import (
    FurnitureRMReimbursementCreate,
    FurnitureRMReimbursementUpdate
)

UPLOAD_ROOT = "files/furniture_rm_reimbursement"
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
def create_history(db: Session, record: FurnitureRMReimbursement):
    history = FurnitureRMReimbursementHistory(
        furniture_rm_reimbursement_id=record.furniture_rm_reimbursement_id,
        ra_claim_id=record.ra_claim_id,

        furniture_name=record.furniture_name,
        claim_month_year=record.claim_month_year,

        total_cost_under_policy=record.total_cost_under_policy,
        expenditure_claimed=record.expenditure_claimed,
        maximum_eligible_amount=record.maximum_eligible_amount,
        amount_claimed=record.amount_claimed,
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
def create_furniture_rm_reimbursement(
    db: Session,
    payload: FurnitureRMReimbursementCreate,
    documents: Optional[List[UploadFile]] = None
):
    doc_paths = _save_documents(documents)

    record = FurnitureRMReimbursement(
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
def update_furniture_rm_reimbursement(
    db: Session,
    reimbursement_id: int,
    payload: FurnitureRMReimbursementUpdate,
    documents: Optional[List[UploadFile]] = None
):
    record = (
        db.query(FurnitureRMReimbursement)
        .filter(
            FurnitureRMReimbursement.furniture_rm_reimbursement_id
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
