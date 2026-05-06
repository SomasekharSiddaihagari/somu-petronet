# app/routers/hse/fta_intermediate_event_router.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.hse.fta_intermediate_event_schema import (
    FTAIntermediateEventCreate,
    FTAIntermediateEventUpdate
)
from app.crud.hse.fta_intermediate_event_crud import (
    create_intermediate_event,
    update_intermediate_event,
    get_all_intermediate_events
)

router = APIRouter(
    prefix="/hse/fta-intermediate-event",
    tags=["HSE - FTA Intermediate Event"]
)


# =========================
# CREATE
# =========================
@router.post("/create")
def create_event(
    data: FTAIntermediateEventCreate,
    db: Session = Depends(get_db)
):
    return create_intermediate_event(db, data)


# =========================
# UPDATE
# =========================
@router.put("/update/{intermediate_event_id}")
def update_event(
    intermediate_event_id: int,
    data: FTAIntermediateEventUpdate,
    db: Session = Depends(get_db)
):
    update_intermediate_event(db, intermediate_event_id, data)
    return {"message": "FTA intermediate event updated successfully"}


# =========================
# GET ALL
# =========================
@router.get("/get-all")
def get_all(
    top_event_id: int | None = None,
    db: Session = Depends(get_db)
):
    return get_all_intermediate_events(db, top_event_id)
