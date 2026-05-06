from typing import List, Optional
from datetime import date, datetime

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    UploadFile,
    File,
    Form
)
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.claim.data_card_reimbursement_schema import (
    DataCardReimbursementCreate,
    DataCardReimbursementUpdate,
    DataCardReimbursementResponse
)
from app.crud.claim.data_card_reimbursement_crud import (
    create_data_card_reimbursement,
    update_data_card_reimbursement
)

router = APIRouter(
    prefix="/api/data-card-reimbursement",
    tags=["Data Card Reimbursement"]
)


# ---------- DATE PARSER ----------
def parse_date(date_str: Optional[str]):
    if not date_str or date_str.lower() == "string":
        return None
    try:
        return datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail="bill_date must be in YYYY-MM-DD format"
        )


# ---------- POST ----------
@router.post(
    "/create",
    response_model=DataCardReimbursementResponse
)
def create_reimbursement(
    ra_claim_id: int = Form(...),
    claim_month: Optional[str] = Form(None),
    data_card_number: Optional[str] = Form(None),
    service_provider: Optional[str] = Form(None),
    bill_date: Optional[str] = Form(None),
    bill_amount: Optional[float] = Form(None),
    monthly_limit: Optional[float] = Form(None),
    bill_amount_total: Optional[float] = Form(None),
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
    created_by: Optional[int] = Form(None),

    documents: List[UploadFile] = File(None),
    db: Session = Depends(get_db)
):
    payload = DataCardReimbursementCreate(
        ra_claim_id=ra_claim_id,
        claim_month=claim_month,
        data_card_number=data_card_number,
        service_provider=service_provider,
        bill_date=parse_date(bill_date),
        bill_amount=bill_amount,
        monthly_limit=monthly_limit,
        bill_amount_total=bill_amount_total,
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
        created_by=created_by
    )

    return create_data_card_reimbursement(
        db=db,
        payload=payload,
        documents=documents
    )


# ---------- PUT ----------
@router.put(
    "/{reimbursement_id}",
    response_model=DataCardReimbursementResponse
)
def update_reimbursement(
    reimbursement_id: int,

    claim_month: Optional[str] = Form(None),
    data_card_number: Optional[str] = Form(None),
    service_provider: Optional[str] = Form(None),
    bill_date: Optional[str] = Form(None),
    bill_amount: Optional[float] = Form(None),
    monthly_limit: Optional[float] = Form(None),
    bill_amount_total: Optional[float] = Form(None),
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
    db: Session = Depends(get_db)
):
    payload = DataCardReimbursementUpdate(
        claim_month=claim_month,
        data_card_number=data_card_number,
        service_provider=service_provider,
        bill_date=parse_date(bill_date),
        bill_amount=bill_amount,
        monthly_limit=monthly_limit,
        bill_amount_total=bill_amount_total,
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

    record = update_data_card_reimbursement(
        db=db,
        reimbursement_id=reimbursement_id,
        payload=payload,
        documents=documents
    )

    if not record:
        raise HTTPException(
            status_code=404,
            detail="Data Card Reimbursement not found"
        )

    return record
