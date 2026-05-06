# app/routers/hse/hse_incident_investigation_team_router.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.hse.hse_incident_investigation_team_schema import (
    InvestigationTeamCreate,
    InvestigationTeamUpdate
)
from app.crud.hse.hse_incident_investigation_team_crud import (
    create_team_member,
    update_team_member,
    get_all_team_members
)

router = APIRouter(
    prefix="/hse/incident-investigation-master-team",  # ✅ DIFFERENT
    tags=["HSE - Investigation Master Team"]            # ✅ DIFFERENT
)


# @router.post("/create")
# def create_team(
#     data: InvestigationTeamCreate,
#     db: Session = Depends(get_db)
# ):
#     return create_team_member(db, data)


# @router.put("/update/{invest_team_id}")
# def update_team(
#     invest_team_id: int,
#     data: InvestigationTeamUpdate,
#     db: Session = Depends(get_db)
# ):
#     update_team_member(db, invest_team_id, data)
#     return {"message": "Investigation master team member updated successfully"}


# @router.get("/get-all")
# def get_all(db: Session = Depends(get_db)):
#     return get_all_team_members(db)

