from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException
from sqlalchemy.orm import Session

from app.crud.hse.hse_major_notification import notify_investigation_team_member, send_incident_notification
from app.database import get_db
from app.models.UserModel import User
from app.schemas.hse.incident_investigation_team_schema import (
    IncidentInvestigationTeamCreate,
    IncidentInvestigationTeamUpdate
)
from app.models.hse.incident_prevention import IncidentPrevention
from app.crud.hse.incident_investigation_team_crud import (
    create_investigation_team,
    update_investigation_team,
    get_all_investigation_teams,
    get_investigation_team_by_prevention_id,
    get_investigation_team_by_id
)

router = APIRouter(
    prefix="/hse/incident-investigation-team",
    tags=["HSE - Incident Investigation Team"]
)




@router.post("/create")
async def create_team_member(
    data: IncidentInvestigationTeamCreate,
    db: Session = Depends(get_db),
    background_tasks: BackgroundTasks = BackgroundTasks()
):

    # ✅ CREATE RECORD
    result = create_investigation_team(db, data)

    # ===============================
    # FETCH USER
    # ===============================
    user = db.query(User).filter(User.user_id == data.user_id).first()

    if not user:
        print("❌ User not found")
        return result

    # ===============================
    # FETCH PREVENTION RECORD
    # ===============================
    prevention_obj = db.query(IncidentPrevention).filter(
        IncidentPrevention.ip_id == data.prevention_id
    ).first()

 

    # ===============================
    # MESSAGE BASED ON ROLE
    # ===============================
    if data.is_leader:
        title = "Investigation Team Leader Assigned"
        description = "You have been assigned as Investigation Team Leader."
    else:
        title = "Added to Investigation Team"
        description = "You have been selected as an investigation team member."

    print("📢 Sending notification to:", user.username)

    # ===============================
    # SEND NOTIFICATION WITH CONTEXT
    # ===============================
    await send_incident_notification(
        db=db,
        title=title,
        description=description,
        from_user="system",
        to_user=user.username,
        module_status="Investigation Team",
        background_tasks=background_tasks,
        prevention=prevention_obj   # ⭐ THIS WAS MISSING
    )

    return result




@router.put("/update/{iit_id}")
async def update_team(
    iit_id: int,
    data: IncidentInvestigationTeamUpdate,
    db: Session = Depends(get_db),
    background_tasks: BackgroundTasks = BackgroundTasks()
):

    result = update_investigation_team(db, iit_id, data)

    user_id = data.user_id

    user = db.query(User).filter(User.user_id == user_id).first()

    # ===============================
    # FETCH PREVENTION RECORD
    # ===============================
    prevention_obj = db.query(IncidentPrevention).filter(
        IncidentPrevention.ip_id == data.prevention_id
    ).first()
    
    if user:

        if data.is_leader:
            title = "Investigation Team Leader Assigned"
            description = "You have been assigned as Investigation Team Leader."

        else:
            title = "Added to Investigation Team"
            description = "You have been selected as an investigation team member."

        print("📢 Sending notification to:", user.username)

        await send_incident_notification(
            db=db,
            title=title,
            description=description,
            from_user="system",
            to_user=user.username,
            module_status="Investigation Team",
            background_tasks=background_tasks,
            prevention=prevention_obj
        )
            
    return result



@router.get("/list")
def list_investigation_team(db: Session = Depends(get_db)):
    return get_all_investigation_teams(db)


@router.get("/by-prevention/{prevention_id}")
def get_team_by_prevention(prevention_id: int, db: Session = Depends(get_db)):
    return get_investigation_team_by_prevention_id(db, prevention_id)


@router.get("/{iit_id}")
def get_team_member_by_id(iit_id: int, db: Session = Depends(get_db)):
    data = get_investigation_team_by_id(db, iit_id)
    if not data:
        raise HTTPException(status_code=404, detail="Team member not found")
    return data
