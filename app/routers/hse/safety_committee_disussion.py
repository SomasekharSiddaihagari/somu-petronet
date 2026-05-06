from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.hse.safety_committee_mintues_discussion import DiscussionCreate, DiscussionUpdate
from app.crud.hse.safety_commitee_disussion_crud import (
    get_all_discussions,
    create_discussion,
    update_discussion,
    get_discussion_by_id 
)

router = APIRouter(prefix="/safety/discussion", tags=["Safety Committee Discussion"])


# ✅ GET ALL
@router.get("/get-all")
def fetch_all(db: Session = Depends(get_db)):
    data = get_all_discussions(db)
    return {
        "status": True,
        "data": data
    }


# ✅ POST
@router.post("/create")
def create(data: DiscussionCreate, db: Session = Depends(get_db)):
    result = create_discussion(db, data)
    return {
        "status": True,
        "message": "Created successfully",
        "data": result
    }


# ✅ PUT
@router.put("/update/{discussion_id}")
def update(discussion_id: int, data: DiscussionUpdate, db: Session = Depends(get_db)):
    result = update_discussion(db, discussion_id, data)
    return {
        "status": True,
        "message": "Updated successfully",
        "data": result
    }
