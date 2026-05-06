from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
#from app.crud.hse.hse_notification_crud import notify_discussion_to_members, notify_meeting_creation
# from app.crud.hse.hse_notification_crud import schedule_meeting_notification
from app.database import get_db
from fastapi import BackgroundTasks
# ================= MINUTES IMPORT =================
from app.schemas.hse.safety_committee_minutes_schema import (
    SafetyCommitteeMinutesCreate,
    SafetyCommitteeMinutesUpdate
)
from sqlalchemy import text  
from app.crud.hse.safety_committee_minutes_crud import (
    create_minutes,
    get_all_minutes,
    get_minutes_by_id,
    update_minutes,
    delete_minutes
)

# ================= DISCUSSION IMPORT =================
from app.schemas.hse.safety_committee_mintues_discussion import (
    DiscussionCreate,
    DiscussionUpdate
)

from app.crud.hse.safety_commitee_disussion_crud import (
    get_all_discussions,
    create_discussion,
    update_discussion,
    get_discussion_by_id
)

from app.crud.hse.safety_committee_minutes_crud import generate_meeting_no

# =====================================================
# 🔥 MAIN ROUTER (DO NOT CHANGE NAME)
# =====================================================
router = APIRouter(
    prefix="/api/hse/safety-committee-minutes",
    tags=["HSE Safety Committee Minutes"]
)

# =====================================================
# 🔥 MINUTES ROUTES
# =====================================================

@router.get("/all")
def get_all_sc_minutes(db: Session = Depends(get_db)):
    result = get_all_minutes(db)
    return {"status": "success", "data": result}

@router.post("/create")
def create_sc_minutes(data: SafetyCommitteeMinutesCreate, db: Session = Depends(get_db)):
    result = create_minutes(db, data)
    return result

# @router.post("/create")
# async def create_sc_minutes(data: SafetyCommitteeMinutesCreate, db: Session = Depends(get_db)):

#     result = create_minutes(db, data)

#     # ✅ fetch time from DB (NOT from request)
#     # meeting_row = db.execute(
#     #     text("""
#     #         SELECT meeting_time
#     #         FROM safety_committee_quarterly_meetings
#     #         ORDER BY scm_id DESC
#     #         LIMIT 1
#     #     """)
#     # ).mappings().first()

#     # meeting_time = meeting_row["meeting_time"] if meeting_row else None

#     # ✅ notification
#     # await notify_meeting_creation(
#     #     result["scmm_id"],
#     #     meeting_time,
#     #     db
#     # )

#     # ✅ scheduler
#     # schedule_meeting_notification(
#     #     minutes_id=result["scmm_id"],
#     #     meeting_date=data.meeting_date,
#     #     meeting_time=meeting_time
#     # )

#     return result





@router.put("/update/{scmm_id}")
def update_sc_minutes(scmm_id: int, data: SafetyCommitteeMinutesUpdate, db: Session = Depends(get_db)):
    existing = get_minutes_by_id(db, scmm_id)
    if not existing:
        raise HTTPException(status_code=404, detail="Minutes not found")

    result = update_minutes(db, scmm_id, data)
    return {"status": "success", "message": result["message"]}


@router.get("/get/{scmm_id}")
def get_minutes(scmm_id: int, db: Session = Depends(get_db)):
    result = get_minutes_by_id(db, scmm_id)
    if not result:
        raise HTTPException(status_code=404, detail="Minutes not found")
    return result


# =====================================================
# 🔥 DISCUSSION ROUTES (MERGED SAME ROUTER)
# =====================================================

# GET ALL DISCUSSION WITH CHILDREN
@router.get("/discussion/get-all")
def fetch_all_discussion(db: Session = Depends(get_db)):
    data = get_all_discussions(db)
    return {
        "status": True,
        "data": data
    }


# GET BY ID DISCUSSION WITH CHILDREN
@router.get("/discussion/get/{discussion_id}")
def fetch_discussion_by_id(discussion_id: int, db: Session = Depends(get_db)):
    result = get_discussion_by_id(db, discussion_id)
    if not result:
        raise HTTPException(status_code=404, detail="Discussion not found")
    return {
        "status": True,
        "data": result
    }


# CREATE DISCUSSION
@router.post("/discussion/create")
async def create_discussion_row(data: DiscussionCreate,background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    result = create_discussion(db, data)
    # await notify_discussion_to_members(
    #     db=db,
    #     discussion=result,
    #     background_tasks=background_tasks
    # )
    return {
        "status": True,
        "message": "Created successfully",
        "data": result
    }


# UPDATE DISCUSSION
@router.put("/discussion/update/{discussion_id}")
def update_discussion_row(discussion_id: int, data: DiscussionUpdate, db: Session = Depends(get_db)):
    result = update_discussion(db, discussion_id, data)
    return {
        "status": True,
        "message": "Updated successfully",
        "data": result
    }

# =====================================================
# 🔥 GENERATE MEETING NO (CALL ON FORM OPEN)
# =====================================================
@router.get("/generate-meeting-no")
def generate_meeting_no_route(user_id: int, db: Session = Depends(get_db)):
    meeting_no = generate_meeting_no(db, user_id)
    return {
        "status": "success",
        "meeting_no": meeting_no
    }


