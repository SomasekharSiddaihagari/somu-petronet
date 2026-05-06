# app/routers/hira_entry_router.py
from fastapi import APIRouter, Depends, BackgroundTasks, HTTPException
from sqlalchemy.orm import Session
from app.crud import NotificationCrud
from app.database import get_db
from app.utils.UserAuthUtils import verify_access_token
from app.crud.MOC.HIRACrud import create_hira, update_hira
from app.schemas.MOC.HIRASchema import HIRACreate, HIRAUpdate

router = APIRouter(prefix="/HIRA", tags=["HIRA"])
# @router.post("/InsertHira")


# @router.put("/UpdateHira")

@router.post("/InsertHira")
def create_hira_entry(
    hira: HIRACreate,
    db: Session = Depends(get_db)
):
    hira_id = create_hira(db, hira)
    return {
        "message": "HIRA entry created successfully",
        "hira_id": hira_id
    }


@router.put("/{hira_id}")
def update_hira_entry(
    hira_id: int,
    hira: HIRAUpdate,
    db: Session = Depends(get_db)
):
    updated = update_hira(db, hira_id, hira)

    if updated == 0:
        raise HTTPException(
            status_code=404,
            detail="HIRA entry not found or no fields to update"
        )

    return {
        "message": "HIRA entry updated successfully"
    }