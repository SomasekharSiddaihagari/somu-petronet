from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.hse.safety_committee_meeting_schema import SafetyCommitteeMeetingCreate, SafetyCommitteeMeetingUpdate
from app.crud.hse.safety_committee_meeting_crud import (
    create_meeting,
    get_all_meetings,
    get_meeting_by_id,
    update_meeting,
    delete_meeting
)
    
router = APIRouter(
    prefix="/api/hse/safety-committee-meetings",
    tags=["HSE Safety Committee Meetings"]
)


@router.get("/all")
def get_all_sc_meetings(db: Session = Depends(get_db)):
    result = get_all_meetings(db)
    return {"status": "success", "data": result}


@router.post("/create")
def create_sc_meeting(data: SafetyCommitteeMeetingCreate, db: Session = Depends(get_db)):
    result = create_meeting(db, data)
    return result




@router.put("/update/{scm_id}")
def update_sc_meeting(scm_id: int, data: SafetyCommitteeMeetingUpdate, db: Session = Depends(get_db)):
    existing = get_meeting_by_id(db, scm_id)
    if not existing:
        raise HTTPException(status_code=404, detail="Meeting not found")
    result = update_meeting(db, scm_id, data)
    return {"status": "success", "message": result["message"]}

