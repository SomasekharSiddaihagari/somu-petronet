import os
import shutil
import json
from datetime import datetime
from typing import List, Optional

from fastapi import UploadFile
from sqlalchemy.orm import Session

from app.models.claim.out_of_pocket_claim import OutOfPocketClaim
from app.models.claim.out_of_pocket_claim_history import OutOfPocketClaimHistory
from app.schemas.claim.out_of_pocket_claim_schema import OutOfPocketClaimCreate, OutOfPocketClaimUpdate



UPLOAD_ROOT = "files/out_of_pocket_claim"
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
def create_history(db: Session, record: OutOfPocketClaim):
    history = OutOfPocketClaimHistory(
        out_of_pocket_claim_id=record.out_of_pocket_claim_id,
        ra_claim_id=record.ra_claim_id,

        claim_month_year=record.claim_month_year,
        total_claims=record.total_claims,
        total_amount=record.total_amount,

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

        updated_by_hop=record.updated_by_hop,
        updated_by_hop_name=record.updated_by_hop_name,
        hop_comment=record.hop_comment,
        
        updated_by_finance=record.updated_by_finance,
        updated_by_finance_name=record.updated_by_finance_name,
        finance_comment=record.finance_comment,
    )
    db.add(history)


# ---------- POST ----------
def create_out_of_pocket_claim(
    db: Session,
    payload: OutOfPocketClaimCreate,
    documents: Optional[List[UploadFile]] = None
):
    doc_paths = _save_documents(documents)

    record = OutOfPocketClaim(
        **payload.dict(exclude={"document_names"}),
        document_names=doc_paths
    )

    db.add(record)
    db.commit()
    db.refresh(record)

    create_history(db, record)
    db.commit()

    return record

