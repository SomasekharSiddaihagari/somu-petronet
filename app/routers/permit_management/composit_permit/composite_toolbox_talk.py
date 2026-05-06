from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.crud.permit_management.composit_permit.composite_toolbox_talk import get_all_composite_toolbox_talks, get_composite_toolbox_talk_by_id
from app.database import get_db


router = APIRouter(
    prefix="/composite-toolbox-talk",
    tags=["Composite Toolbox Talk"]
)


@router.get("")
def read_all_composite_toolbox_talks(
    db: Session = Depends(get_db)
):
    """
    Get all composite toolbox talks (all columns)
    """
    return get_all_composite_toolbox_talks(db)


@router.get("/{ctt_id}")
def read_composite_toolbox_talk_by_id(
    ctt_id: int,
    db: Session = Depends(get_db)
):
    """
    Get composite toolbox talk by ctt_id (all columns)
    """
    data = get_composite_toolbox_talk_by_id(db, ctt_id)

    if not data:
        raise HTTPException(
            status_code=404,
            detail="Composite Toolbox Talk not found"
        )

    return data
