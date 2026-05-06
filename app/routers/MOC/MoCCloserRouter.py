
from sqlalchemy import text   

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.MOC.MoCCloser import MoCClosureCreate, MoCClosureOut, MoCClosureUpdate
from app.crud.MOC.MoCCloserCrud import create_moc_closure, update_moc_closure_by_request_id
from app.utils.UserAuthUtils import verify_access_token
from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, Query
from app.models.MOC.MocRequestModel import MoCRequest
from app.crud.NotificationCrud import notify_closure_completed
from app.models.UserModel import User
from fastapi import Form, File, UploadFile
from typing import List
import os, uuid, json
from datetime import date as Date  # ← alias
 
router = APIRouter(prefix="/moc_closures", tags=["MOC Closures"])
 
UPLOAD_DIR = "files/moc_manuals"
os.makedirs(UPLOAD_DIR, exist_ok=True)
 
 



def parse_manuals(record):
    if not record:
        return record

    if isinstance(record, dict):
        rec = record
    else:
        rec = dict(record)

    if rec.get("relevant_manuals"):
        try:
            rec["relevant_manuals"] = json.loads(rec["relevant_manuals"])
        except:
            rec["relevant_manuals"] = []
    else:
        rec["relevant_manuals"] = []

    return rec









@router.post("/close", response_model=MoCClosureOut)
async def create_moc_closure_api(
    moc_request_id: int = Form(...),
    moc_request_no: str = Form(...),
    title_of_moc: str | None = Form(None),
    brief_description: str | None = Form(None),
    moc_initiator_dept: str | None = Form(None),
    executing_dept: str | None = Form(None),
    moc_execution_details: str | None = Form(None),
    hira_recommendation_status: str | None = Form(None),
    revised_operating_procedure: str | None = Form(None),
    training_completed: str | None = Form(None),
    comments_initiator: str | None = Form(None),
    status: str | None = Form("draft"),

    date: Date | None = Form(None),
    job_start_date: Date | None = Form(None),
    job_completion_date: Date | None = Form(None),

    relevant_manuals: List[UploadFile] | None = File(None),

    db: Session = Depends(get_db),
    background_tasks: BackgroundTasks = None,
    # current_user: dict = Depends(verify_access_token)
):

    # ============================
    # SAVE FILES
    # ============================
    file_paths = []

    if relevant_manuals:
        for doc in relevant_manuals:
            ext = doc.filename.split(".")[-1]
            filename = f"moc_{moc_request_id}_{uuid.uuid4()}.{ext}"
            full_path = os.path.join(UPLOAD_DIR, filename)

            with open(full_path, "wb") as f:
                f.write(doc.file.read())

            file_paths.append(full_path)

    manuals_json = file_paths

    moc_data = MoCClosureCreate(
        moc_request_id=moc_request_id,
        moc_request_no=moc_request_no,
        title_of_moc=title_of_moc,
        brief_description=brief_description,
        moc_initiator_dept=moc_initiator_dept,
        executing_dept=executing_dept,
        moc_execution_details=moc_execution_details,
        hira_recommendation_status=hira_recommendation_status,
        revised_operating_procedure=revised_operating_procedure,
        training_completed=training_completed,
        relevant_manuals=manuals_json,
        comments_initiator=comments_initiator,
        status=status,
        date=date,
        job_start_date=job_start_date,
        job_completion_date=job_completion_date
    )

    result = create_moc_closure(db, moc_data)
    return parse_manuals(result)







@router.put("/request/{moc_request_id}", response_model=MoCClosureOut)
async def update_moc_closure_api(
    moc_request_id: int,
    moc_request_no: str | None = Form(None),
    title_of_moc: str | None = Form(None),
    brief_description: str | None = Form(None),
    moc_initiator_dept: str | None = Form(None),
    executing_dept: str | None = Form(None),
    moc_execution_details: str | None = Form(None),
    hira_recommendation_status: str | None = Form(None),
    revised_operating_procedure: str | None = Form(None),
    training_completed: str | None = Form(None),
    comments_initiator: str | None = Form(None),
    status: str | None = Form(None),
    moc_date: Date | None = Form(None),
    job_start_date: Date | None = Form(None),
    job_completion_date: Date | None = Form(None),
    relevant_manuals: List[UploadFile] | None = File(None),
    db: Session = Depends(get_db),
):
    # Get existing manuals to append to
    existing = db.execute(
        text("SELECT relevant_manuals FROM moc_closures WHERE moc_request_id = :id"),
        {"id": moc_request_id}
    ).fetchone()

    file_paths = json.loads(existing.relevant_manuals) if existing and existing.relevant_manuals else []

    # Save new uploaded files and append
    if relevant_manuals:
        for doc in relevant_manuals:
            ext = doc.filename.split(".")[-1]
            filename = f"moc_{moc_request_id}_{uuid.uuid4()}.{ext}"
            full_path = os.path.join(UPLOAD_DIR, filename)
            with open(full_path, "wb") as f:
                f.write(doc.file.read())
            file_paths.append(full_path)

    moc_data = MoCClosureUpdate(
        moc_request_no=moc_request_no,
        title_of_moc=title_of_moc,
        brief_description=brief_description,
        moc_initiator_dept=moc_initiator_dept,
        executing_dept=executing_dept,
        moc_execution_details=moc_execution_details,
        hira_recommendation_status=hira_recommendation_status,
        revised_operating_procedure=revised_operating_procedure,
        training_completed=training_completed,
        comments_initiator=comments_initiator,
        status=status,
        date=moc_date,
        job_start_date=job_start_date,
        job_completion_date=job_completion_date,
        relevant_manuals=file_paths if file_paths else None
    )

    result = update_moc_closure_by_request_id(db, moc_request_id, moc_data)
    return parse_manuals(result)












