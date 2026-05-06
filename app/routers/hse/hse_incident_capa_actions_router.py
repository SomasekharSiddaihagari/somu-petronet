# app/routers/hse/hse_incident_capa_actions_router.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.hse.hse_incident_capa_actions_schema import (
    IncidentCAPACreate,
    IncidentCAPAUpdate
)
from app.crud.hse.hse_incident_capa_actions_crud import (
    create_capa_action,
    update_capa_action,
    get_all_capa_actions
)

router = APIRouter(
    prefix="/hse/incident-capa-actions",
    tags=["HSE - Incident CAPA Actions"]
)


@router.post("/create")
def create_capa(
    data: IncidentCAPACreate,
    db: Session = Depends(get_db)
):
    return create_capa_action(db, data)


@router.put("/update/{capa_id}")
def update_capa(
    capa_id: int,
    data: IncidentCAPAUpdate,
    db: Session = Depends(get_db)
):
    update_capa_action(db, capa_id, data)
    return {"message": "CAPA action updated successfully"}


@router.get("/get-all")
def get_all(db: Session = Depends(get_db)):
    return get_all_capa_actions(db)
