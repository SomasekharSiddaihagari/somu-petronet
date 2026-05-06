from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.crud.permit_management.work_height_permit.work_at_height_toolbox_talk import get_all_work_at_height_toolbox_talks, get_work_at_height_toolbox_talk_by_id
from app.database import get_db
from app.schemas.permit_management.work_height_permit.work_at_height_toolbox_talk import WorkAtHeightToolboxTalkSchema


router = APIRouter(
    prefix="/work-at-height-toolbox-talk",
    tags=["Work At Height Toolbox Talk"]
)


@router.get(
    "",
    response_model=List[WorkAtHeightToolboxTalkSchema]
)
def read_all_work_at_height_toolbox_talks(
    db: Session = Depends(get_db)
):
    """
    Get all work at height toolbox talks (all columns)
    """
    return get_all_work_at_height_toolbox_talks(db)


@router.get(
    "/{whtt_id}",
    response_model=WorkAtHeightToolboxTalkSchema
)
def read_work_at_height_toolbox_talk_by_id(
    whtt_id: int,
    db: Session = Depends(get_db)
):
    """
    Get work at height toolbox talk by whtt_id (all columns)
    """
    data = get_work_at_height_toolbox_talk_by_id(db, whtt_id)

    if not data:
        raise HTTPException(
            status_code=404,
            detail="Work At Height Toolbox Talk not found"
        )

    return data
