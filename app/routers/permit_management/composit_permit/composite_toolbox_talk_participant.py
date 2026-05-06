from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.crud.permit_management.composit_permit.composite_toolbox_talk_participant import get_all_composite_toolbox_talk_participants, get_composite_toolbox_talk_participant_by_id
from app.database import get_db
from app.schemas.permit_management.composit_permit.composite_toolbox_talk_participant import CompositeToolboxTalkParticipantSchema


router = APIRouter(
    prefix="/composite-toolbox-talk-participant",
    tags=["Composite Toolbox Talk Participant"]
)


@router.get(
    "",
    response_model=List[CompositeToolboxTalkParticipantSchema]
)
def read_all_composite_toolbox_talk_participants(
    db: Session = Depends(get_db)
):
    return get_all_composite_toolbox_talk_participants(db)


@router.get(
    "/{cttp_id}",
    response_model=CompositeToolboxTalkParticipantSchema
)
def read_composite_toolbox_talk_participant_by_id(
    cttp_id: int,
    db: Session = Depends(get_db)
):
    data = get_composite_toolbox_talk_participant_by_id(db, cttp_id)

    if not data:
        raise HTTPException(
            status_code=404,
            detail="Composite Toolbox Talk Participant not found"
        )

    return data
