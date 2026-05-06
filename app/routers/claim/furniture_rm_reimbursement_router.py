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
from app.schemas.claim.furniture_rm_reimbursement_schema import (
    FurnitureRMReimbursementCreate,
    FurnitureRMReimbursementUpdate,
    FurnitureRMReimbursementResponse
)
from app.crud.claim.furniture_rm_reimbursement_crud import (
    create_furniture_rm_reimbursement,
    update_furniture_rm_reimbursement
)

router = APIRouter(
    prefix="/api/furniture-rm-reimbursement",
    tags=["Furniture RM Reimbursement"]
)


# ---------- POST ----------
@router.post("/create", response_model=FurnitureRMReimbursementResponse)
async def create_reimbursement(
    ra_claim_id: int = Form(...),
    furniture_name: Optional[str] = Form(None),
    claim_month_year: Optional[str] = Form(None),

    total_cost_under_policy: Optional[float] = Form(None),
    expenditure_claimed: Optional[float] = Form(None),
    maximum_eligible_amount: Optional[float] = Form(None),
    amount_claimed: Optional[float] = Form(None),
    eligible_amount: Optional[float] = Form(None),

    remarks: Optional[str] = Form(None),
    declaration_accepted: Optional[bool] = Form(None),
    status: Optional[str] = Form(None),
    created_by: Optional[int] = Form(None),

    documents: List[UploadFile] = File(None),
    background_tasks: BackgroundTasks = BackgroundTasks(),
    db: Session = Depends(get_db)
):
    payload = FurnitureRMReimbursementCreate(
        ra_claim_id=ra_claim_id,
        furniture_name=furniture_name,
        claim_month_year=claim_month_year,
        total_cost_under_policy=total_cost_under_policy,
        expenditure_claimed=expenditure_claimed,
        maximum_eligible_amount=maximum_eligible_amount,
        amount_claimed=amount_claimed,
        eligible_amount=eligible_amount,
        remarks=remarks,
        declaration_accepted=declaration_accepted,
        status=status,
        created_by=created_by
    )

    record = create_furniture_rm_reimbursement(
        db=db,
        payload=payload,
        documents=documents
    )
# =====================================================
    # 🔔 NOTIFICATION (CREATE)
    # =====================================================
    print("🔔 [FURNITURE CREATE] Notification Trigger Check")
    print("STATUS:", status)
    print("CREATED_BY:", created_by)
    print("RA_CLAIM_ID:", ra_claim_id)

    # ⚠️ FIX: Trigger notification for ANY status, not just "Pending Supervisor Approval"
    if status and created_by:
        ra_claim = db.query(RAClaim).filter(
            RAClaim.ra_claim_id == ra_claim_id
        ).first()

        if not ra_claim:
            print("❌ RA Claim not found!")
            return record

        ra_claim_ref_id = ra_claim.ra_claim_ref_id
        print("RA CLAIM REF ID:", ra_claim_ref_id)

        if not ra_claim_ref_id:
            print("❌ RA Claim Ref ID is None!")
            return record

        class DummySheet:
            def __init__(self):
                self.status = status
                self.user_id = created_by
                self.requisition_number = ra_claim_ref_id

                # ---- FURNITURE DATA ----
                self.furniture_name = furniture_name
                self.amount_claimed = amount_claimed
                self.eligible_amount = eligible_amount
                self.remarks = remarks

                # ---- ROLE COMMENTS (None for new submission) ----
                self.supervisor_comment = None
                self.updated_by_supervisor = None
                self.updated_by_supervisor_name = None

                self.hr_comment = None
                self.updated_by_hr = None
                self.updated_by_hr_name = None

                self.finance_comment = None
                self.updated_by_finance = None
                self.updated_by_finance_name = None

        print("📤 Calling handle_claim_notification()")

        await handle_claim_notification(
            db=db,
            module_key="furniture",
            sheet=DummySheet(),
            background_tasks=background_tasks
        )

        print("✅ handle_claim_notification() COMPLETED")
    else:
        print("⚠️ Notification NOT triggered - missing status or created_by")

    return record


# ---------- PUT ----------
@router.put("/{reimbursement_id}", response_model=FurnitureRMReimbursementResponse)
async def update_reimbursement(
    reimbursement_id: int,

    furniture_name: Optional[str] = Form(None),
    claim_month_year: Optional[str] = Form(None),

    total_cost_under_policy: Optional[float] = Form(None),
    expenditure_claimed: Optional[float] = Form(None),
    maximum_eligible_amount: Optional[float] = Form(None),
    amount_claimed: Optional[float] = Form(None),
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
    payload = FurnitureRMReimbursementUpdate(
        furniture_name=furniture_name,
        claim_month_year=claim_month_year,
        total_cost_under_policy=total_cost_under_policy,
        expenditure_claimed=expenditure_claimed,
        maximum_eligible_amount=maximum_eligible_amount,
        amount_claimed=amount_claimed,
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

    record = update_furniture_rm_reimbursement(
        db=db,
        reimbursement_id=reimbursement_id,
        payload=payload,
        documents=documents
    )

    if not record:
        raise HTTPException(
            status_code=404,
            detail="Furniture RM Reimbursement not found"
        )

# =====================================================
    # 🔔 NOTIFICATION (UPDATE)
    # =====================================================
    if status:
        ra_claim = db.query(RAClaim).filter(
            RAClaim.ra_claim_id == record.ra_claim_id
        ).first()

        if not ra_claim:
            print("❌ RA Claim not found for notification!")
            return record

        ra_claim_ref_id = ra_claim.ra_claim_ref_id
        print("RA CLAIM REF ID:", ra_claim_ref_id)

        if not ra_claim_ref_id:
            print("❌ RA Claim Ref ID is None!")
            return record

        class DummySheet:
            def __init__(self):
                self.status = status
                self.user_id = record.created_by
                self.requisition_number = ra_claim_ref_id

                self.furniture_name = record.furniture_name
                self.amount_claimed = record.amount_claimed
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

        print("📤 Calling handle_claim_notification()")

        await handle_claim_notification(
            db=db,
            module_key="furniture",
            sheet=DummySheet(),
            background_tasks=background_tasks
        )

        print("✅ handle_claim_notification() COMPLETED")
    else:
        print("⚠️ Notification NOT triggered - status is None")

    return record
