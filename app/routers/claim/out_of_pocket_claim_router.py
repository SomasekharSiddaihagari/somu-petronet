from datetime import date
import os
from pydoc import text
import shutil
from typing import List, Optional
from sqlalchemy.sql import text as sql_text

from fastapi import (
    APIRouter, BackgroundTasks, Depends, HTTPException,
    UploadFile, File, Form
)
from sqlalchemy.orm import Session

from app.crud.claim.claim_notifications_crud import handle_claim_notification
from app.crud.claim.laptop_maintenance_reimbursement_crud import _save_documents
from app.crud.claim.out_of_packet_crud_ import create_out_of_pocket_entry, update_out_of_pocket_entry
from app.database import get_db
from app.models.claim.ra_claim import RAClaim
from app.schemas.claim.out_of_pocket_claim_entry_schema import OutOfPocketClaimEntryCreate, OutOfPocketClaimEntryResponse, OutOfPocketClaimEntryUpdate
from app.schemas.claim.out_of_pocket_claim_schema import (
    OutOfPocketClaimCreate,
    OutOfPocketClaimUpdate,
    OutOfPocketClaimResponse
)
from app.crud.claim.out_of_pocket_claim_crud import (
    create_out_of_pocket_claim,
    
)


router = APIRouter(
    prefix="/api/out-of-pocket-claim",
    tags=["Out Of Pocket Claim"]
)


UPLOAD_BASE = "files"

def save_file(upload: UploadFile, folder: str) -> str:
    os.makedirs(f"{UPLOAD_BASE}/{folder}", exist_ok=True)
    file_path = f"{UPLOAD_BASE}/{folder}/{upload.filename}"

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(upload.file, buffer)

    return file_path



# =================================================
# CREATE ENTRY
# =================================================
@router.post("/entry",
    response_model=OutOfPocketClaimEntryResponse
)
def create_entry(
    data: OutOfPocketClaimEntryCreate,
    db: Session = Depends(get_db)
):
    entry_id = create_out_of_pocket_entry(db, data)

    result = db.execute(
        sql_text("""
            SELECT *
            FROM out_of_pocket_claim_entry
            WHERE out_of_pocket_claim_entry_id = :id
        """),
        {"id": entry_id}
    ).mappings().first()

    return result


# =================================================
# UPDATE ENTRY
# =================================================
@router.put(
    "/entry/{out_of_pocket_claim_entry_id}",
    response_model=OutOfPocketClaimEntryResponse
)
def update_entry(
    out_of_pocket_claim_entry_id: int,
    data: OutOfPocketClaimEntryUpdate,
    db: Session = Depends(get_db)
):
    updated = update_out_of_pocket_entry(
        db,
        out_of_pocket_claim_entry_id,
        data
    )

    if not updated:
        raise HTTPException(
            status_code=404,
            detail="Out of pocket claim entry not found"
        )

    result = db.execute(
        sql_text("""
            SELECT *
            FROM out_of_pocket_claim_entry
            WHERE out_of_pocket_claim_entry_id = :id
        """),
        {"id": out_of_pocket_claim_entry_id}
    ).mappings().first()

    return result





# ---------- POST ----------
@router.post("/claim", response_model=OutOfPocketClaimResponse)
async def create_claim(
    ra_claim_id: int = Form(...),

    claim_month_year: Optional[str] = Form(None),
    total_claims: Optional[int] = Form(None),
    total_amount: Optional[float] = Form(None),

    remarks: Optional[str] = Form(None),
    updated_by_supervisor: Optional[date] = Form(None),
    updated_by_supervisor_name: Optional[str] = Form(None),
    supervisor_comment: Optional[str] = Form(None),

    # -------- HR --------
    updated_by_hr: Optional[date] = Form(None),
    updated_by_hr_name: Optional[str] = Form(None),
    hr_comment: Optional[str] = Form(None),

    updated_by_hop: Optional[date] = Form(None),
    updated_by_hop_name: Optional[str] = Form(None),
    hop_comment: Optional[str] = Form(None),
    # -------- Finance --------
    updated_by_finance: Optional[date] = Form(None),
    updated_by_finance_name: Optional[str] = Form(None),
    finance_comment: Optional[str] = Form(None),
    declaration_accepted: Optional[bool] = Form(None),
    status: Optional[str] = Form(None),
    created_by: Optional[int] = Form(None),

    documents: List[UploadFile] = File(None),
    background_tasks: BackgroundTasks = BackgroundTasks(),
    db: Session = Depends(get_db)
):
    payload = OutOfPocketClaimCreate(
        ra_claim_id=ra_claim_id,
        claim_month_year=claim_month_year,
        total_claims=total_claims,
        total_amount=total_amount,
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
        
        updated_by_hop=updated_by_hop,
        updated_by_hop_name=updated_by_hop_name,
        hop_comment=hop_comment,
        
        declaration_accepted=declaration_accepted,
        status=status,
        created_by=created_by
    )

    record=create_out_of_pocket_claim(
        db=db,
        payload=payload,
        documents=documents
    )

# =====================================================
    # 🔔 NOTIFICATION (CREATE)
    # =====================================================
    print("🔔 [OUT OF POCKET CREATE] Notification Trigger Check")
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

                # ---- OUT OF POCKET DATA ----
                self.total_claims = total_claims
                self.total_amount = total_amount
                self.claim_month_year = claim_month_year
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
            module_key="out_of_pocket",
            sheet=DummySheet(),
            background_tasks=background_tasks
        )

        print("✅ handle_claim_notification() COMPLETED")
    else:
        print("⚠️ Notification NOT triggered - missing status or created_by")

    return record


@router.put(
    "/claim/{out_of_pocket_claim_id}",
    response_model=OutOfPocketClaimResponse
)
async def update_claim(  # ⚠️ Changed to async
    out_of_pocket_claim_id: int,
    claim_month_year: Optional[str] = Form(None),
    total_claims: Optional[int] = Form(None),
    total_amount: Optional[float] = Form(None),
    remarks: Optional[str] = Form(None),
    
    # ---------- Supervisor ----------
    updated_by_supervisor: Optional[date] = Form(None),
    updated_by_supervisor_name: Optional[str] = Form(None),
    supervisor_comment: Optional[str] = Form(None),
    
    # ---------- HR ----------
    updated_by_hr: Optional[date] = Form(None),
    updated_by_hr_name: Optional[str] = Form(None),
    hr_comment: Optional[str] = Form(None),
    
    # ---------- Finance ----------
    updated_by_finance: Optional[date] = Form(None),
    updated_by_finance_name: Optional[str] = Form(None),
    finance_comment: Optional[str] = Form(None),
    
    updated_by_hop: Optional[date] = Form(None),
    updated_by_hop_name: Optional[str] = Form(None),
    hop_comment: Optional[str] = Form(None),
    
    declaration_accepted: Optional[bool] = Form(None),
    status: Optional[str] = Form(None),
    updated_by: Optional[int] = Form(None),
    
    documents: Optional[List[UploadFile]] = File(None),
    background_tasks: BackgroundTasks = BackgroundTasks(),
    db: Session = Depends(get_db)
):
    print("🔔 [OUT OF POCKET UPDATE] Notification Trigger Check")
    print("OUT_OF_POCKET_CLAIM_ID:", out_of_pocket_claim_id)
    print("STATUS:", status)
    print("UPDATED_BY:", updated_by)
    
    # -------------------------------------------------- 
    # 1️⃣ Fetch existing claim
    # -------------------------------------------------- 
    existing = db.execute(
        sql_text("""
            SELECT * FROM out_of_pocket_claim 
            WHERE out_of_pocket_claim_id = :id
        """),
        {"id": out_of_pocket_claim_id}
    ).mappings().first()
    
    if not existing:
        raise HTTPException(
            status_code=404,
            detail="Out Of Pocket Claim not found"
        )
    
    # -------------------------------------------------- 
    # 2️⃣ Save history BEFORE update
    # -------------------------------------------------- 
    # Add your history logic here if needed
    
    # -------------------------------------------------- 
    # 3️⃣ Prepare update payload (NULL-safe)
    # -------------------------------------------------- 
    update_data = {
        "claim_month_year": claim_month_year,
        "total_claims": total_claims,
        "total_amount": total_amount,
        "remarks": remarks,
        
        "updated_by_supervisor": updated_by_supervisor,
        "updated_by_supervisor_name": updated_by_supervisor_name,
        "supervisor_comment": supervisor_comment,
        
        "updated_by_hr": updated_by_hr,
        "updated_by_hr_name": updated_by_hr_name,
        "hr_comment": hr_comment,
        
        "updated_by_finance": updated_by_finance,
        "updated_by_finance_name": updated_by_finance_name,
        "finance_comment": finance_comment,
        
        "updated_by_hop": updated_by_hop,
        "updated_by_hop_name": updated_by_hop_name,
        "hop_comment": hop_comment,
        
        "declaration_accepted": declaration_accepted,
        "status": status,
        "updated_by": updated_by,
    }
    
    # Remove None values (VERY IMPORTANT)
    update_data = {k: v for k, v in update_data.items() if v is not None}
    
    # -------------------------------------------------- 
    # 4️⃣ Handle documents
    # -------------------------------------------------- 
    if documents:
        update_data["document_names"] = _save_documents(documents)
    
    # -------------------------------------------------- 
    # 5️⃣ Update main table
    # -------------------------------------------------- 
    if update_data:
        set_clause = ", ".join(f"{k} = :{k}" for k in update_data.keys())
        db.execute(
            sql_text(f"""
                UPDATE out_of_pocket_claim 
                SET {set_clause}, updated_at = NOW()
                WHERE out_of_pocket_claim_id = :claim_id
            """),
            {**update_data, "claim_id": out_of_pocket_claim_id}
        )
    
    # -------------------------------------------------- 
    # 6️⃣ Optional: sync remarks to entries
    # -------------------------------------------------- 
    # if "remarks" in update_data:
    #     db.execute(
    #         sql_text("""
    #             UPDATE out_of_pocket_claim_entry 
    #             SET justification = :remarks
    #             WHERE out_of_pocket_claim_id = :claim_id
    #         """),
    #         {
    #             "remarks": update_data["remarks"],
    #             "claim_id": out_of_pocket_claim_id
    #         }
    #     )
    


    # -------------------------------------------------- 
    # 7️⃣ Commit
    # -------------------------------------------------- 
    db.commit()
    
    # -------------------------------------------------- 
    # 8️⃣ Fetch updated record
    # -------------------------------------------------- 
    updated_record = db.execute(
        sql_text("""
            SELECT * FROM out_of_pocket_claim 
            WHERE out_of_pocket_claim_id = :id
        """),
        {"id": out_of_pocket_claim_id}
    ).mappings().first()
    
    # =====================================================
    # 🔔 NOTIFICATION (UPDATE)
    # =====================================================
    if status:
        # Fetch RA Claim for reference ID
        ra_claim = db.query(RAClaim).filter(
            RAClaim.ra_claim_id == updated_record["ra_claim_id"]
        ).first()
        
        if not ra_claim:
            print("❌ RA Claim not found for notification!")
            return updated_record
        
        ra_claim_ref_id = ra_claim.ra_claim_ref_id
        print("RA CLAIM REF ID:", ra_claim_ref_id)
        
        if not ra_claim_ref_id:
            print("❌ RA Claim Ref ID is None!")
            return updated_record
        
        # Create dummy sheet object for notification
        class DummySheet:
            def __init__(self):
                self.status = status
                self.user_id = updated_record["created_by"]
                self.requisition_number = ra_claim_ref_id
                
                # ---- OUT OF POCKET DATA ----
                self.total_claims = updated_record["total_claims"]
                self.total_amount = updated_record["total_amount"]
                self.claim_month_year = updated_record["claim_month_year"]
                self.remarks = updated_record["remarks"]
                
                # ---- SUPERVISOR ----
                self.supervisor_comment = updated_record["supervisor_comment"]
                self.updated_by_supervisor = updated_record["updated_by_supervisor"]
                self.updated_by_supervisor_name = updated_record["updated_by_supervisor_name"]
                
                # ---- HR ----
                self.hr_comment = updated_record["hr_comment"]
                self.updated_by_hr = updated_record["updated_by_hr"]
                self.updated_by_hr_name = updated_record["updated_by_hr_name"]
                
                # ---- FINANCE ----
                self.finance_comment = updated_record["finance_comment"]
                self.updated_by_finance = updated_record["updated_by_finance"]
                self.updated_by_finance_name = updated_record["updated_by_finance_name"]
        
        print("📤 Calling handle_claim_notification()")
        
        await handle_claim_notification(
            db=db,
            module_key="out_of_pocket",
            sheet=DummySheet(),
            background_tasks=background_tasks
        )
        
        print("✅ handle_claim_notification() COMPLETED")
    else:
        print("⚠️ Notification NOT triggered - status is None")
    
    return updated_record











