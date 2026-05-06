# app/routers/hse/fta_top_event_router.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.hse.fta_top_event_schema import (
    FTATopEventCreate,
    FTATopEventUpdate
)
from app.crud.hse.fta_top_event_crud import (
    create_fta_top_event,
    update_fta_top_event,
    get_all_fta_top_events
)

router = APIRouter(
    prefix="/hse/fta-top-event",
    tags=["HSE - FTA Top Event"]
)


# =========================
# CREATE (WITH HIIM LINK)
# =========================
@router.post("/create/{hiim_id}")
def create_event(
    hiim_id: int,
    data: FTATopEventCreate,
    db: Session = Depends(get_db)
):
    payload = data.model_dump()
    return create_fta_top_event(db, hiim_id, payload)


# =========================
# UPDATE
# =========================
@router.put("/update/{fta_top_id}")
def update_event(
    fta_top_id: int,
    data: FTATopEventUpdate,
    db: Session = Depends(get_db)
):
    update_fta_top_event(db, fta_top_id, data)
    return {"message": "FTA top event updated successfully"}


# =========================
# GET ALL
# =========================
@router.get("/get-all")
def get_all(db: Session = Depends(get_db)):
    return get_all_fta_top_events(db)
