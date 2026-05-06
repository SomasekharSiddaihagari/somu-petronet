from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.hse.safety_committee_minutes_members_schema import SafetyCommitteeMinutesMemberCreate, SafetyCommitteeMinutesMemberUpdate
from app.crud.hse.safety_committee_minutes_members_crud import (
    create_minutes_member,
    get_all_minutes_members,
    get_minutes_member_by_id,
    update_minutes_member,
    delete_minutes_member
)

router = APIRouter(
    prefix="/api/hse/safety-committee-minutes-members",
    tags=["HSE Safety Committee Minutes Members"]
)

@router.get("/all")
def get_all_sc_minutes_members(db: Session = Depends(get_db)):
    result = get_all_minutes_members(db)
    return {"status": "success", "data": result}

@router.post("/create")
def create_sc_minutes_member(data: SafetyCommitteeMinutesMemberCreate, db: Session = Depends(get_db)):
    result = create_minutes_member(db, data)
    return result



@router.put("/update/{scmm_id}")
def update_sc_minutes_member(scmm_id: int, data: SafetyCommitteeMinutesMemberUpdate, db: Session = Depends(get_db)):
    existing = get_minutes_member_by_id(db, scmm_id)
    if not existing:
        raise HTTPException(status_code=404, detail="Member not found")
    result = update_minutes_member(db, scmm_id, data)
    return {"status": "success", "message": result["message"]}


