from datetime import date
from fastapi import APIRouter, BackgroundTasks, Depends, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import List, Optional
import os, uuid

from app.crud.claim.claim_notifications_crud import handle_claim_notification
from app.database import get_db
from app.models.claim.ra_claim import RAClaim
from app.schemas.claim.mobile_bill_reimbursement_schema import (
    MobileBillReimbursementCreate,
    MobileBillReimbursementUpdate
)
from app.crud.claim.mobile_bill_reimbursement_crud import (
    create_mobile_bill_reimbursement,
    update_mobile_bill_reimbursement,
)

UPLOAD_DIR = "files/mobile_bill_reimbursement_docs"
os.makedirs(UPLOAD_DIR, exist_ok=True)

router = APIRouter(
    prefix="/api/mobile-bill-reimbursement",
    tags=["Mobile Bill Reimbursement"]
)


# -------------------------------------------------
# Utility: clean empty form values
# -------------------------------------------------


def clean_form_value(value):
    if value in ("", "null"):
        return None
    return value


# =================================================
# CREATE
# =================================================
@router.post("/create")
async def create_reimbursement(
    ra_claim_id: int = Form(...),
    declaration_accepted: bool = Form(...),

    bill_month_year: Optional[str] = Form(None),

    mobile_number_1: Optional[str] = Form(None),
    bill_amount_1: Optional[float] = Form(None),

    mobile_number_2: Optional[str] = Form(None),
    bill_amount_2: Optional[float] = Form(None),

    total_claimed_amount: Optional[float] = Form(None),
    monthly_limit: Optional[float] = Form(None),

    remarks: Optional[str] = Form(None),
    status: Optional[str] = Form(None),

    # -------- Supervisor --------
    updated_by_supervisor: Optional[date] = Form(None),
    updated_by_supervisor_name: Optional[str] = Form(None),
    supervisor_comment: Optional[str] = Form(None),

    # -------- HR --------
    updated_by_hr: Optional[date] = Form(None),
    updated_by_hr_name: Optional[str] = Form(None),
    hr_comment: Optional[str] = Form(None),

    # -------- Finance --------
    updated_by_finance: Optional[date] = Form(None),
    updated_by_finance_name: Optional[str] = Form(None),
    finance_comment: Optional[str] = Form(None),

    created_by: Optional[int] = Form(None),

    documents: Optional[List[UploadFile]] = File(None),
    background_tasks: BackgroundTasks = BackgroundTasks(),

    db: Session = Depends(get_db),
):
    saved_files = []


    if documents:
        for doc in documents:
            ext = os.path.splitext(doc.filename)[1]
            filename = f"{uuid.uuid4()}{ext}"

            # ✅ FULL RELATIVE PATH
            relative_path = os.path.join(UPLOAD_DIR, filename)

            with open(relative_path, "wb") as f:
                f.write(await doc.read())

            saved_files.append(relative_path)


    payload = MobileBillReimbursementCreate(
    ra_claim_id=ra_claim_id,
    bill_month_year=bill_month_year,

    mobile_number_1=mobile_number_1,
    bill_amount_1=bill_amount_1,
    mobile_number_2=mobile_number_2,
    bill_amount_2=bill_amount_2,

    total_claimed_amount=total_claimed_amount,
    monthly_limit=monthly_limit,

    document_names=",".join(saved_files) if saved_files else None,
    remarks=remarks,
    declaration_accepted=declaration_accepted,
    status=status,

    updated_by_supervisor=updated_by_supervisor,
    updated_by_supervisor_name=updated_by_supervisor_name,
    supervisor_comment=supervisor_comment,

    updated_by_hr=updated_by_hr,
    updated_by_hr_name=updated_by_hr_name,
    hr_comment=hr_comment,

    updated_by_finance=updated_by_finance,
    updated_by_finance_name=updated_by_finance_name,
    finance_comment=finance_comment,

    created_by=created_by
)

    reimbursement_id = create_mobile_bill_reimbursement(db, payload)
# =====================================================
    # 🔔 NOTIFICATION (CREATE)
    # =====================================================
    if status == "Pending Supervisor Approval":

        ra_claim = db.query(RAClaim).filter(
            RAClaim.ra_claim_id == ra_claim_id
        ).first()

        ra_claim_ref_id = ra_claim.ra_claim_ref_id if ra_claim else None

        class DummySheet:
            def __init__(self):
                self.status = status
                self.user_id = created_by
                self.requisition_number = ra_claim_ref_id  

                # ---- MOBILE BILL DATA ----
                self.bill_month_year = bill_month_year
                self.mobile_number_1 = mobile_number_1
                self.bill_amount_1 = bill_amount_1
                self.mobile_number_2 = mobile_number_2
                self.bill_amount_2 = bill_amount_2
                self.total_claimed_amount = total_claimed_amount
                self.monthy_limit = monthly_limit

      

        await handle_claim_notification(
            db=db,
            module_key="mobile_reimbursement",
            sheet=DummySheet(),
            background_tasks=background_tasks
        )
    return {
        "status": "success",
        "mobile_bill_reimbursement_id": reimbursement_id,
        "documents": saved_files
    }


# =================================================
# UPDATE
# =================================================
@router.put("/update/{mobile_bill_reimbursement_id}")
async def update_reimbursement(
    mobile_bill_reimbursement_id: int,

    bill_month_year: Optional[str] = Form(None),

    mobile_number_1: Optional[str] = Form(None),
    bill_amount_1: Optional[float] = Form(None),

    mobile_number_2: Optional[str] = Form(None),
    bill_amount_2: Optional[float] = Form(None),

    total_claimed_amount: Optional[float] = Form(None),
    monthly_limit: Optional[float] = Form(None),

    remarks: Optional[str] = Form(None),
    declaration_accepted: Optional[bool] = Form(None),
    status: Optional[str] = Form(None),

    # -------- Supervisor --------
    updated_by_supervisor: Optional[date] = Form(None),
    updated_by_supervisor_name: Optional[str] = Form(None),
    supervisor_comment: Optional[str] = Form(None),

    # -------- HR --------
    updated_by_hr: Optional[date] = Form(None),
    updated_by_hr_name: Optional[str] = Form(None),
    hr_comment: Optional[str] = Form(None),

    # -------- Finance --------
    updated_by_finance: Optional[date] = Form(None),
    updated_by_finance_name: Optional[str] = Form(None),
    finance_comment: Optional[str] = Form(None),

    updated_by: Optional[int] = Form(None),

    documents: Optional[List[UploadFile]] = File(None),
    db: Session = Depends(get_db),
):
    saved_files = []

    if documents:
        for doc in documents:
            ext = os.path.splitext(doc.filename)[1]
            unique_name = f"{uuid.uuid4()}{ext}"
            with open(os.path.join(UPLOAD_DIR, unique_name), "wb") as f:
                f.write(await doc.read())
            saved_files.append(unique_name)

    raw_payload = {
        "bill_month_year": bill_month_year,
        "mobile_number_1": mobile_number_1,
        "bill_amount_1": bill_amount_1,
        "mobile_number_2": mobile_number_2,
        "bill_amount_2": bill_amount_2,
        "total_claimed_amount": total_claimed_amount,
        "monthly_limit": monthly_limit,
        "remarks": remarks,
        "declaration_accepted": declaration_accepted,
        "status": status,

        "updated_by_supervisor": updated_by_supervisor,
        "updated_by_supervisor_name": updated_by_supervisor_name,
        "supervisor_comment": supervisor_comment,

        "updated_by_hr": updated_by_hr,
        "updated_by_hr_name": updated_by_hr_name,
        "hr_comment": hr_comment,

        "updated_by_finance": updated_by_finance,
        "updated_by_finance_name": updated_by_finance_name,
        "finance_comment": finance_comment,

        "updated_by": updated_by,
    }

    payload = {
        k: clean_form_value(v)
        for k, v in raw_payload.items()
        if clean_form_value(v) is not None
    }

    if saved_files:
        payload["document_names"] = ",".join(saved_files)

    update_mobile_bill_reimbursement(
        db,
        mobile_bill_reimbursement_id,
        MobileBillReimbursementUpdate(**payload)
    )

    return {
        "status": "success",
        "message": "Mobile bill reimbursement updated successfully",
        "documents": saved_files
    }

