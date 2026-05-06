# app/routers/asset_claim_router.py
from datetime import date
from fastapi import APIRouter, BackgroundTasks, Depends
from sqlalchemy.orm import Session
from app.crud.claim.claim_notifications_crud import handle_claim_notification
from app.database import get_db
from app.models.claim.asset_claim import AssetClaim
from app.models.claim.asset_claim_submission import AssetClaimSubmission
from app.schemas.claim.asset_claim_schema import (
    AssetClaimCreate,
    AssetClaimUpdate
)
from app.crud.claim.asset_claim_crud import (
    create_asset_claim,
    update_asset_claim
)
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.claim.asset_claim_submission_schema import (
    AssetClaimSubmissionCreate,
    AssetClaimSubmissionUpdate
)
from app.crud.claim.asset_claim_submission_crud import (
    create_asset_claim_submission,
    update_asset_claim_submission
)
from fastapi import APIRouter, Depends, UploadFile, File, Form
import uuid
import os
from typing import List, Optional



from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.claim.asset_claim_disbursement_schema import (
    AssetClaimDisbursementCreate,
    AssetClaimDisbursementUpdate
)
from app.crud.claim.asset_claim_disbursement_crud import (
    create_asset_claim_disbursement,
    update_asset_claim_disbursement
)


router = APIRouter(
    prefix="/api/asset-claim",
    tags=["Asset Claim,Submission And Disbursement"]
)


# -----------------------------
# CREATE
# -----------------------------
@router.post("/create")
def create_claim(
    data: AssetClaimCreate,
    db: Session = Depends(get_db)
):
    result = create_asset_claim(db, data)

    return {
        "status": "success",
        "asset_claim_id": result["asset_claim_id"],
        "claim_ref_id": result["claim_ref_id"]
    }



# -----------------------------
# UPDATE
# role = SUPERVISOR | HR | FINANCE
# -----------------------------
@router.put("/update/{asset_claim_id}")
def update_claim(
    asset_claim_id: int,
    data: AssetClaimUpdate,
    db: Session = Depends(get_db)
):
    update_asset_claim(db, asset_claim_id, data)
    return {
        "status": "success",
        "message": "Asset claim updated successfully"
    }



## asset claim submission is starting from here --------------------------------->


UPLOAD_DIR = "files/asset_claim_submission_docs"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post("/submission/create")
async def create_submission(
    asset_claim_id: int = Form(...),
    item_type: Optional[str] = Form(None),
    item_name: Optional[str] = Form(None),
    claim_amount: Optional[float] = Form(None),

    vendor_name: Optional[str] = Form(None),
    vendor_gstin: Optional[str] = Form(None),
    vendor_address: Optional[str] = Form(None),
    vendor_contact_no: Optional[str] = Form(None),
    invoice_date: Optional[str] = Form(None),
    invoice_no: Optional[str] = Form(None),

    declaration_accepted: Optional[bool] = Form(None),
    status: Optional[str] = Form(None),
    created_by: Optional[int] = Form(None),

    document_names: Optional[List[UploadFile]] = File(None),
    owned_by: Optional[str] = Form(None),
    db: Session = Depends(get_db),
    background_tasks: BackgroundTasks = BackgroundTasks(),
):
    saved_files = []

    if document_names:
        for doc in document_names:
            ext = os.path.splitext(doc.filename)[1]
            unique_name = f"{uuid.uuid4()}{ext}"

            # absolute path
            file_path = os.path.abspath(os.path.join(UPLOAD_DIR, unique_name))

            with open(file_path, "wb") as f:
                f.write(await doc.read())

            saved_files.append(file_path)

    # store as comma-separated string or JSON (your choice)
    document_names = ",".join(saved_files) if saved_files else None


    payload = {
        "asset_claim_id": asset_claim_id,
        "item_type": item_type,
        "item_name": item_name,
        "claim_amount": claim_amount,
        "vendor_name": vendor_name,
        "vendor_gstin": vendor_gstin,
        "vendor_address": vendor_address,
        "vendor_contact_no": vendor_contact_no,
        "invoice_date": invoice_date,
        "invoice_no": invoice_no,
        "document_names": document_names,
        "owned_by": owned_by,
        "declaration_accepted": declaration_accepted,
        "status": status,
        "created_by": created_by,
    }

    submission_id = create_asset_claim_submission(
        db,
        AssetClaimSubmissionCreate(**payload)
    )

    # =====================================================
    # 🔔 FIRST NOTIFICATION (Pending Supervisor Approval)
    # =====================================================
    # 🔔 FIRST NOTIFICATION TRIGGER
    if status and status.strip() == "Pending Supervisor Approval":

        asset_claim = (
            db.query(
                AssetClaim.claim_ref_id,
                AssetClaim.category,
                AssetClaim.bought_back
            )
            .filter(AssetClaim.asset_claim_id == asset_claim_id)
            .first()
        )


    

        class DummySheet:
            def __init__(
                self,
                status,
                user_id,
                requisition_number,
                item_type,
                item_name,
                claim_amount,
                owned_by,
                category,
            ):
                self.status = status
                self.user_id = user_id
                self.requisition_number = requisition_number
                self.item_type = item_type
                self.item_name = item_name
                self.claim_amount = claim_amount
                self.owned_by = owned_by
                self.category = category

        sheet = DummySheet(
            status=status.strip(),
            user_id=created_by,
            requisition_number=asset_claim.claim_ref_id,  # ✅ DIRECT FROM DB
            item_type=item_type,
            item_name=item_name,
            claim_amount=claim_amount,
            owned_by=owned_by,
            category=asset_claim.category,
        )

        await handle_claim_notification(
            db=db,
            module_key="asset",
            sheet=sheet,
            background_tasks=background_tasks
        )

    
    return {
        "status": "success",
        "asset_claim_submission_id": submission_id,
        "documents": saved_files
    }





@router.put("/submission/update/{asset_claim_submission_id}")
async def update_submission(
    asset_claim_submission_id: int,

    item_type: Optional[str] = Form(None),
    item_name: Optional[str] = Form(None),
    claim_amount: Optional[float] = Form(None),

    vendor_name: Optional[str] = Form(None),
    vendor_gstin: Optional[str] = Form(None),
    vendor_address: Optional[str] = Form(None),
    vendor_contact_no: Optional[str] = Form(None),
    invoice_date: Optional[str] = Form(None),
    invoice_no: Optional[str] = Form(None),

    residual_value_percent: Optional[float] = Form(None),
    residual_value_amount: Optional[float] = Form(None),
    amount_to_be_disbursed: Optional[float] = Form(None),
    owned_by: Optional[str] = Form(None),
    declaration_accepted: Optional[bool] = Form(None),
    status: Optional[str] = Form(None),
    updated_by: Optional[int] = Form(None),
    sap_assets_no: Optional[int] = Form(None),
    # document_names: Optional[List[UploadFile]] = File(None),
    hr_comment: Optional[str] =Form(None),
    finance_comment: Optional[str] =Form(None),
    supervisor_comment: Optional[str] =Form(None),
    updated_by_supervisor: Optional[date] =Form(None),
    updated_by_supervisor_name: Optional[str] =Form(None),
    updated_by_hr: Optional[date] =Form(None),
    updated_by_hr_name: Optional[str] =Form(None),
    updated_by_finance: Optional[date] =Form(None),
    updated_by_finance_name: Optional[str] =Form(None),
    db: Session = Depends(get_db),
    background_tasks: BackgroundTasks = BackgroundTasks(),
):
    saved_files = []


    payload = AssetClaimSubmissionUpdate(
        item_type=item_type,
        item_name=item_name,
        claim_amount=claim_amount,
        vendor_name=vendor_name,
        vendor_gstin=vendor_gstin,
        vendor_address=vendor_address,
        vendor_contact_no=vendor_contact_no,
        invoice_date=invoice_date,
        invoice_no=invoice_no,
        owned_by=owned_by,
        # document_names=document_names,
        declaration_accepted=declaration_accepted,

        residual_value_percent=residual_value_percent,
        residual_value_amount=residual_value_amount,
        amount_to_be_disbursed=amount_to_be_disbursed,

        status=status,
        updated_by=updated_by,
        updated_by_supervisor=updated_by_supervisor,
        updated_by_supervisor_name=updated_by_supervisor_name,
        supervisor_comment=supervisor_comment,
        updated_by_hr=updated_by_hr,
        updated_by_hr_name=updated_by_hr_name,
        hr_comment=hr_comment,
        updated_by_finance=updated_by_finance,
        updated_by_finance_name=updated_by_finance_name,
        finance_comment=finance_comment,
    )

    update_asset_claim_submission(
        db,
        asset_claim_submission_id,
        payload
    )

    # =====================================================
# 🔔 NOTIFICATION TRIGGER (UPDATE FLOW)
# =====================================================
    if status:

        submission = db.query(AssetClaimSubmission).filter(
            AssetClaimSubmission.asset_claim_submission_id == asset_claim_submission_id
        ).first()

        if not submission:
            print("❌ Submission not found, skipping notification")
            return

        asset_claim = (
            db.query(
                AssetClaim.claim_ref_id,
                AssetClaim.category,
                AssetClaim.bought_back,
                AssetClaim.created_by
            )
            .filter(AssetClaim.asset_claim_id == submission.asset_claim_id)
            .first()
        )

        if not asset_claim:
            print("❌ AssetClaim not found, skipping notification")
            return

        owned_by = "Employee" if asset_claim.bought_back else "Company"

        class DummySheet:
            def __init__(
                self,
                status,
                user_id,
                requisition_number,
                item_type,
                item_name,
                claim_amount,
                owned_by,
                category,
                supervisor_comment,
                hr_comment,
                finance_comment,
                updated_by_supervisor_name,
                updated_by_hr_name,
                updated_by_finance_name,
                updated_by_supervisor,
                updated_by_hr,
                updated_by_finance,
            ):
                self.status = status
                self.user_id = user_id                 # ✅ INITIATOR
                self.requisition_number = requisition_number
                self.item_type = item_type
                self.item_name = item_name
                self.claim_amount = claim_amount
                self.owned_by = owned_by
                self.category = category

                self.supervisor_comment = supervisor_comment
                self.hr_comment = hr_comment
                self.finance_comment = finance_comment

                self.updated_by_supervisor_name = updated_by_supervisor_name
                self.updated_by_hr_name = updated_by_hr_name
                self.updated_by_finance_name = updated_by_finance_name

                self.updated_by_supervisor = updated_by_supervisor
                self.updated_by_hr = updated_by_hr
                self.updated_by_finance = updated_by_finance

        sheet = DummySheet(
            status=status.strip(),
            user_id=submission.created_by,   # ✅ FIXED
            requisition_number=asset_claim.claim_ref_id,
            item_type=item_type,
            item_name=item_name,
            claim_amount=claim_amount,
            owned_by=owned_by,
            category=asset_claim.category,

            supervisor_comment=supervisor_comment,
            hr_comment=hr_comment,
            finance_comment=finance_comment,

            updated_by_supervisor_name=updated_by_supervisor_name,
            updated_by_hr_name=updated_by_hr_name,
            updated_by_finance_name=updated_by_finance_name,

            updated_by_supervisor=updated_by_supervisor,
            updated_by_hr=updated_by_hr,
            updated_by_finance=updated_by_finance,
        )

        await handle_claim_notification(
            db=db,
            module_key="asset",
            sheet=sheet,
            background_tasks=background_tasks
        )

    return {
        "message": "Asset claim submission updated successfully",
        "item_type":item_type,
        "item_name":item_name,
        "claim_amount":claim_amount,
        "vendor_name":vendor_name,
        "vendor_gstin":vendor_gstin,
        "vendor_address":vendor_address,
        "vendor_contact_no":vendor_contact_no,
        "invoice_date":invoice_date,
        "invoice_no":invoice_no,
        "owned_by": owned_by,
        # "document_names":document_names,
        "declaration_accepted":declaration_accepted,
        "status":status,
        "updated_by":updated_by,
        "updated_by_supervisor":updated_by_supervisor,
        "updated_by_supervisor_name":updated_by_supervisor_name,
        "supervisor_comment":supervisor_comment,
        "updated_by_hr":updated_by_hr,
        "updated_by_hr_name":updated_by_hr_name,
        "hr_comment":hr_comment,
        "updated_by_finance":updated_by_finance,
        "finance_comment":finance_comment,
        "updated_by_finance_name":updated_by_finance_name,
       
    }






#<---------- Here asset claim disbursement is starting ----------->



@router.post("/disbursement/create")
def create_disbursement(
    data: AssetClaimDisbursementCreate,
    db: Session = Depends(get_db)
):
    disbursement_id = create_asset_claim_disbursement(db, data)
    return {
        "status": "success",
        "asset_claim_disbursement_id": disbursement_id
    }


@router.put("/disbursement/update/{asset_claim_disbursement_id}")
def update_disbursement(
    asset_claim_disbursement_id: int,
    data: AssetClaimDisbursementUpdate,
    db: Session = Depends(get_db)
):
    update_asset_claim_disbursement(
        db,
        asset_claim_disbursement_id,
        data
    )
    return {
        "status": "success",
        "message": "Asset claim disbursement updated successfully"
    }


