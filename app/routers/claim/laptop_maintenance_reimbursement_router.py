from datetime import date
from typing import List, Optional

from fastapi import (
    APIRouter, BackgroundTasks, Depends, HTTPException,
    UploadFile, File, Form
)
from sqlalchemy.orm import Session

from app.crud.claim.claim_notifications_crud import handle_claim_notification
from app.database import get_db
from app.models.claim.ra_claim import RAClaim
from app.schemas.claim.laptop_maintenance_reimbursement_schema import (
    LaptopMaintenanceReimbursementCreate,
    LaptopMaintenanceReimbursementUpdate,
    LaptopMaintenanceReimbursementResponse
)
from app.crud.claim.laptop_maintenance_reimbursement_crud import (
    create_laptop_maintenance_reimbursement,
    update_laptop_maintenance_reimbursement
)

router = APIRouter(
    prefix="/api/laptop-maintenance-reimbursement",
    tags=["Laptop Maintenance Reimbursement"]
)


# ---------- POST ----------
@router.post("/create", response_model=LaptopMaintenanceReimbursementResponse)
async def create_reimbursement(
    ra_claim_id: int = Form(...),

    date_of_purchase: Optional[str] = Form(None),
    date_of_claim: Optional[str] = Form(None),
    date_of_previous_claim: Optional[str] = Form(None),

    amount_claimed: Optional[float] = Form(None),
    annual_limit: Optional[float] = Form(None),
    eligible_amount: Optional[float] = Form(None),

    remarks: Optional[str] = Form(None),
    declaration_accepted: Optional[bool] = Form(None),
    status: Optional[str] = Form(None),
    created_by: Optional[int] = Form(None),

    documents: List[UploadFile] = File(None),
    background_tasks: BackgroundTasks = BackgroundTasks(),
    db: Session = Depends(get_db)
):
    payload = LaptopMaintenanceReimbursementCreate(
        ra_claim_id=ra_claim_id,
        date_of_purchase=date_of_purchase,
        date_of_claim=date_of_claim,
        date_of_previous_claim=date_of_previous_claim,
        amount_claimed=amount_claimed,
        annual_limit=annual_limit,
        eligible_amount=eligible_amount,
        remarks=remarks,
        declaration_accepted=declaration_accepted,
        status=status,
        created_by=created_by
    )

    record= create_laptop_maintenance_reimbursement(
        db=db,
        payload=payload,
        documents=documents
    )
# =====================================================
    # 🔔 NOTIFICATION (CREATE)
    # =====================================================
    if status:
        ra_claim = db.query(RAClaim).filter(
            RAClaim.ra_claim_id == ra_claim_id
        ).first()

        ra_claim_ref_id = (
            ra_claim.ra_claim_ref_id
            if ra_claim and ra_claim.ra_claim_ref_id
            else f"LM-{record.laptop_maintenance_reimbursement_id}"
        )

        class DummySheet:
            def __init__(self):
                self.status = status
                self.user_id = created_by
                self.requisition_number = ra_claim_ref_id

                # Laptop details (email body)
                self.date_of_purchase = date_of_purchase
                self.date_of_claim = date_of_claim
                self.date_of_previous_claim = date_of_previous_claim
                self.amount_claimed = amount_claimed
                self.annual_limit = annual_limit
                self.eligible_amount = eligible_amount
                self.remarks = record.remarks
                # Role fields (safe defaults)
                self.supervisor_comment = None
                self.updated_by_supervisor = None
                self.updated_by_supervisor_name = None

                self.hr_comment = None
                self.updated_by_hr = None
                self.updated_by_hr_name = None

                self.finance_comment = None
                self.updated_by_finance = None
                self.updated_by_finance_name = None

        await handle_claim_notification(
            db=db,
            module_key="laptop",
            sheet=DummySheet(),
            background_tasks=background_tasks
        )

    return record


# ---------- PUT ----------
@router.put("/{reimbursement_id}", response_model=LaptopMaintenanceReimbursementResponse)
async def update_reimbursement(
    reimbursement_id: int,

    date_of_purchase: Optional[str] = Form(None),
    date_of_claim: Optional[str] = Form(None),
    date_of_previous_claim: Optional[str] = Form(None),

    amount_claimed: Optional[float] = Form(None),
    annual_limit: Optional[float] = Form(None),
    eligible_amount: Optional[float] = Form(None),

    remarks: Optional[str] = Form(None),

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

    declaration_accepted: Optional[bool] = Form(None),
    status: Optional[str] = Form(None),
    updated_by: Optional[int] = Form(None),

    documents: List[UploadFile] = File(None),
    background_tasks: BackgroundTasks = BackgroundTasks(),
    db: Session = Depends(get_db)
):
    payload = LaptopMaintenanceReimbursementUpdate(
        date_of_purchase=date_of_purchase,
        date_of_claim=date_of_claim,
        date_of_previous_claim=date_of_previous_claim,
        amount_claimed=amount_claimed,
        annual_limit=annual_limit,
        eligible_amount=eligible_amount,
        remarks=remarks,
        updated_by_supervisor=updated_by_supervisor,
        updated_by_supervisor_name=updated_by_supervisor_name,
        supervisor_comment=supervisor_comment,

        updated_by_hr=updated_by_hr,
        updated_by_hr_name=updated_by_hr_name,
        hr_comment=hr_comment,

        updated_by_finance=updated_by_finance,
        updated_by_finance_name=updated_by_finance_name,
        finance_comment=finance_comment,
        declaration_accepted=declaration_accepted,
        status=status,
        updated_by=updated_by
    )

    record = update_laptop_maintenance_reimbursement(
        db=db,
        reimbursement_id=reimbursement_id,
        payload=payload,
        documents=documents
    )

    if not record:
        raise HTTPException(
            status_code=404,
            detail="Laptop Maintenance Reimbursement not found"
        )

# =====================================================
    # 🔔 NOTIFICATION (UPDATE)
    # =====================================================
    if status:
        ra_claim = db.query(RAClaim).filter(
            RAClaim.ra_claim_id == record.ra_claim_id
        ).first()

        ra_claim_ref_id = (
            ra_claim.ra_claim_ref_id
            if ra_claim and ra_claim.ra_claim_ref_id
            else f"LM-{record.laptop_maintenance_reimbursement_id}"
        )

        class DummySheet:
            def __init__(self, record):
                self.status = record.status
                self.user_id = record.created_by   # ✅ correct user
                self.requisition_number = ra_claim_ref_id

                # ---- CLAIM DATA ----
                self.amount_claimed = record.amount_claimed
                self.annual_limit = record.annual_limit
                self.eligible_amount = record.eligible_amount
                self.remarks = record.remarks

                # ---- SUPERVISOR ----
                self.supervisor_comment = record.supervisor_comment
                self.updated_by_supervisor = record.updated_by_supervisor
                self.updated_by_supervisor_name = record.updated_by_supervisor_name

                # ---- HR ----
                self.hr_comment = record.hr_comment
                self.updated_by_hr = record.updated_by_hr
                self.updated_by_hr_name = record.updated_by_hr_name

                # ---- FINANCE ----
                self.finance_comment = record.finance_comment
                self.updated_by_finance = record.updated_by_finance
                self.updated_by_finance_name = record.updated_by_finance_name

        await handle_claim_notification(
            db=db,
            module_key="laptop",
            sheet=DummySheet(record),
            background_tasks=background_tasks
        )

    return record
