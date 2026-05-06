# app/routers/hse/fta_basic_event_router.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.hse.fta_basic_event_schema import (
    FTABasicEventCreate,
    FTABasicEventUpdate
)
from app.crud.hse.fta_basic_event_crud import (
    create_basic_event,
    update_basic_event,
    get_all_basic_events
)

router = APIRouter(
    prefix="/hse/fta-basic-event",
    tags=["HSE - FTA Basic Event"]
)


@router.post("/create")
def create_event(
    data: FTABasicEventCreate,
    db: Session = Depends(get_db)
):
    return create_basic_event(db, data)


@router.put("/update/{fte_basic_id}")
def update_event(
    fte_basic_id: int,
    data: FTABasicEventUpdate,
    db: Session = Depends(get_db)
):
    update_basic_event(db, fte_basic_id, data)
    return {"message": "FTA basic event updated successfully"}


@router.get("/get-all")
def get_all(db: Session = Depends(get_db)):
    return get_all_basic_events(db)
