import os
import shutil
import json
from datetime import datetime
from typing import List, Optional

from fastapi import UploadFile
from sqlalchemy.orm import Session

from app.models.claim.data_card_reimbursement import DataCardReimbursement
from app.models.claim.data_card_reimbursement_history import (
    DataCardReimbursementHistory
)

from app.schemas.claim.data_card_reimbursement_schema import (
    DataCardReimbursementCreate,
    DataCardReimbursementUpdate
)

# ---------- FILE ROOT ----------
UPLOAD_ROOT = "files/data_card_reimbursement"
os.makedirs(UPLOAD_ROOT, exist_ok=True)


# ---------- SAVE FILES (INLINE) ----------
def _save_documents(files: Optional[List[UploadFile]]):
    if not files:
        return None

    saved_files = []

    for file in files:
        timestamp = int(datetime.now().timestamp())
        filename = f"{timestamp}_{file.filename}"
        file_path = os.path.join(UPLOAD_ROOT, filename)

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        saved_files.append(os.path.abspath(file_path).replace("\\", "/"))

    return json.dumps(saved_files)


# ---------- CREATE HISTORY ----------
def create_history(db: Session, record: DataCardReimbursement):
    history = DataCardReimbursementHistory(
        data_card_reimbursement_id=record.data_card_reimbursement_id,
        ra_claim_id=record.ra_claim_id,
        claim_month=record.claim_month,
        data_card_number=record.data_card_number,
        service_provider=record.service_provider,
        bill_date=record.bill_date,
        bill_amount=record.bill_amount,
        monthly_limit=record.monthly_limit,
        bill_amount_total=record.bill_amount_total,
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

        created_by=record.created_by,
    )
    db.add(history)


# ---------- POST ----------
def create_data_card_reimbursement(
    db: Session,
    payload: DataCardReimbursementCreate,
    documents: Optional[List[UploadFile]] = None
):
    document_paths = _save_documents(documents)

    payload_data = payload.dict(exclude={"document_names"})

    record = DataCardReimbursement(
        **payload_data,
        document_names=document_paths
    )

    db.add(record)
    db.commit()
    db.refresh(record)

    create_history(db, record)
    db.commit()

    return record


# ---------- PUT ----------
def update_data_card_reimbursement(
    db: Session,
    reimbursement_id: int,
    payload: DataCardReimbursementUpdate,
    documents: Optional[List[UploadFile]] = None
):
    record = (
        db.query(DataCardReimbursement)
        .filter(
            DataCardReimbursement.data_card_reimbursement_id == reimbursement_id
        )
        .first()
    )

    if not record:
        return None

    create_history(db, record)

    payload_data = payload.dict(
        exclude_unset=True,
        exclude={"document_names"}
    )

    for key, value in payload_data.items():
        setattr(record, key, value)

    if documents:
        record.document_names = _save_documents(documents)

    db.commit()
    db.refresh(record)
    return record
