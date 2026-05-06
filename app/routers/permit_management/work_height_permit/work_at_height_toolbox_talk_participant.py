from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.crud.permit_management.work_height_permit.work_at_height_toolbox_talk_participant import get_all_work_at_height_toolbox_talk_participants, get_work_at_height_toolbox_talk_participant_by_id
from app.database import get_db
from app.schemas.permit_management.work_height_permit.work_at_height_toolbox_talk_participant import WorkAtHeightToolboxTalkParticipantSchema


router = APIRouter(
    prefix="/work-at-height-toolbox-talk-participant",
    tags=["Work At Height Toolbox Talk Participant"]
)


@router.get(
    "",
    response_model=List[WorkAtHeightToolboxTalkParticipantSchema]
)
def read_all_work_at_height_toolbox_talk_participants(
    db: Session = Depends(get_db)
):
    """
    Get all work at height toolbox talk participants (all columns)
    """
    return get_all_work_at_height_toolbox_talk_participants(db)


@router.get(
    "/{whttp_id}",
    response_model=WorkAtHeightToolboxTalkParticipantSchema
)
def read_work_at_height_toolbox_talk_participant_by_id(
    whttp_id: int,
    db: Session = Depends(get_db)
):
    """
    Get work at height toolbox talk participant by whttp_id (all columns)
    """
    data = get_work_at_height_toolbox_talk_participant_by_id(db, whttp_id)

    if not data:
        raise HTTPException(
            status_code=404,
            detail="Work At Height Toolbox Talk Participant not found"
        )

    return data
