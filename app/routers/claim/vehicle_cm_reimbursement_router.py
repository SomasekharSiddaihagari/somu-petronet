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
from app.schemas.claim.vehicle_cm_reimbursement_schema import (
    VehicleCMReimbursementCreate,
    VehicleCMReimbursementUpdate,
    VehicleCMReimbursementResponse
)
from app.crud.claim.vehicle_cm_reimbursement_crud import (
    create_vehicle_cm_reimbursement,
    update_vehicle_cm_reimbursement
)

router = APIRouter(
    prefix="/api/vehicle-cm-reimbursement",
    tags=["Vehicle CM Reimbursement"]
)


# ---------- POST ----------
@router.post("/create", response_model=VehicleCMReimbursementResponse)
async def create_reimbursement(
    ra_claim_id: int = Form(...),

    vehicle_name: Optional[str] = Form(None),
    claim_month_year: Optional[str] = Form(None),

    vehicle_no: Optional[str] = Form(None),
    vehicle_type: Optional[str] = Form(None),
    fuel_type: Optional[str] = Form(None),

    rc_expiry_date: Optional[date] = Form(None),
    insurance_expiry_date: Optional[date] = Form(None),

    fuel_claim_amount: Optional[float] = Form(None),
    applicable_fuel_rate: Optional[float] = Form(None),
    fuel_claimed_liters: Optional[float] = Form(None),

    maintenance_claim_amount: Optional[float] = Form(None),
    fixed_conveyance_claim: Optional[bool] = Form(None),
    fixed_conveyance_claim_amount: Optional[float] = Form(None),

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
    remarks: Optional[str] = Form(None),
    declaration_accepted: Optional[bool] = Form(None),
    status: Optional[str] = Form(None),
    created_by: Optional[int] = Form(None),

    documents: List[UploadFile] = File(None),
    background_tasks: BackgroundTasks = BackgroundTasks(),

    db: Session = Depends(get_db)
):
    payload = VehicleCMReimbursementCreate(
        ra_claim_id=ra_claim_id,
        vehicle_name=vehicle_name,
        claim_month_year=claim_month_year,
        vehicle_no=vehicle_no,
        vehicle_type=vehicle_type,
        fuel_type=fuel_type,
        rc_expiry_date=rc_expiry_date,
        insurance_expiry_date=insurance_expiry_date,
        fuel_claim_amount=fuel_claim_amount,
        applicable_fuel_rate=applicable_fuel_rate,
        fuel_claimed_liters=fuel_claimed_liters,
        maintenance_claim_amount=maintenance_claim_amount,
        fixed_conveyance_claim=fixed_conveyance_claim,
        fixed_conveyance_claim_amount=fixed_conveyance_claim_amount,
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

    record= create_vehicle_cm_reimbursement(
        db=db,
        payload=payload,
        documents=documents
    )


# =====================================================
    # 🔔 NOTIFICATION (CREATE)
    # =====================================================
    print("🔔 [VEHICLE CREATE] Notification Trigger Check")
    print("STATUS:", status)
    print("CREATED_BY:", created_by)
    print("RA_CLAIM_ID:", ra_claim_id)

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

                # ---- VEHICLE DATA ----
                self.vehicle_name = vehicle_name
                self.maintenance_claim_amount = maintenance_claim_amount
                self.fuel_claim_amount = fuel_claim_amount
                self.vehicle_no = vehicle_no
                self.vehicle_type = vehicle_type
                self.remarks = remarks

                # ---- ROLE COMMENTS (None for new submission) ----
                self.supervisor_comment = supervisor_comment
                self.updated_by_supervisor = updated_by_supervisor
                self.updated_by_supervisor_name = updated_by_supervisor_name

                self.hr_comment = hr_comment
                self.updated_by_hr = updated_by_hr
                self.updated_by_hr_name = updated_by_hr_name

                self.finance_comment = finance_comment
                self.updated_by_finance = updated_by_finance
                self.updated_by_finance_name = updated_by_finance_name

        print("📤 Calling handle_claim_notification()")

        await handle_claim_notification(
            db=db,
            module_key="vehicle",
            sheet=DummySheet(),
            background_tasks=background_tasks
        )

        print("✅ handle_claim_notification() COMPLETED")
    else:
        print("⚠️ Notification NOT triggered - missing status or created_by")

    return record


# ---------- PUT ----------
@router.put("/{reimbursement_id}", response_model=VehicleCMReimbursementResponse)
async def update_reimbursement(
    reimbursement_id: int,

    vehicle_name: Optional[str] = Form(None),
    claim_month_year: Optional[str] = Form(None),

    vehicle_no: Optional[str] = Form(None),
    vehicle_type: Optional[str] = Form(None),
    fuel_type: Optional[str] = Form(None),

    rc_expiry_date: Optional[date] = Form(None),
    insurance_expiry_date: Optional[date] = Form(None),

    fuel_claim_amount: Optional[float] = Form(None),
    applicable_fuel_rate: Optional[float] = Form(None),
    fuel_claimed_liters: Optional[float] = Form(None),

    maintenance_claim_amount: Optional[float] = Form(None),
    fixed_conveyance_claim: Optional[bool] = Form(None),
    fixed_conveyance_claim_amount: Optional[float] = Form(None),

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
    payload = VehicleCMReimbursementUpdate(
        vehicle_name=vehicle_name,
        claim_month_year=claim_month_year,
        vehicle_no=vehicle_no,
        vehicle_type=vehicle_type,
        fuel_type=fuel_type,
        rc_expiry_date=rc_expiry_date,
        insurance_expiry_date=insurance_expiry_date,
        fuel_claim_amount=fuel_claim_amount,
        applicable_fuel_rate=applicable_fuel_rate,
        fuel_claimed_liters=fuel_claimed_liters,
        maintenance_claim_amount=maintenance_claim_amount,
        fixed_conveyance_claim=fixed_conveyance_claim,
        fixed_conveyance_claim_amount=fixed_conveyance_claim_amount,
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
    print("payload",payload)

    record = update_vehicle_cm_reimbursement(
        db=db,
        reimbursement_id=reimbursement_id,
        payload=payload,
        documents=documents
    )

    if not record:
        raise HTTPException(
            status_code=404,
            detail="Vehicle CM Reimbursement not found"
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

                # ---- VEHICLE DATA ----
                self.vehicle_name = record.vehicle_name
                self.maintenance_claim_amount = record.maintenance_claim_amount
                self.fuel_claim_amount = record.fuel_claim_amount
                self.vehicle_no = record.vehicle_no
                self.vehicle_type = record.vehicle_type
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
            module_key="vehicle",
            sheet=DummySheet(),
            background_tasks=background_tasks
        )

        print(" handle_claim_notification() COMPLETED")
    else:
        print("⚠️ Notification NOT triggered - status is None")

    return record
