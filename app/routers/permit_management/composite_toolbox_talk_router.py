from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.permit_management.composite_toolbox_talk_schema import (
    CompositeToolboxTalkCreate,
    CompositeToolboxTalkUpdate
)
from app.crud.permit_management.composite_toolbox_talk_crud import (
    create_composite_toolbox_talk,
    update_composite_toolbox_talk
)

router = APIRouter(
    prefix="/composite-toolbox-talk",
    tags=["Composite Toolbox Talk"]
)


# =================================================
# POST — CREATE TOOLBOX TALK
# =================================================
@router.post("", summary="Create Composite Toolbox Talk")
def create_toolbox_talk(
    payload: CompositeToolboxTalkCreate,
    db: Session = Depends(get_db)
):
    result = create_composite_toolbox_talk(db, payload)

    return {
        "message": "Composite Toolbox Talk created",
        "ctt_id": result["ctt_id"]
    }


# =================================================
# PUT — UPDATE TOOLBOX TALK
# =================================================
@router.put("/{ctt_id}", summary="Update Composite Toolbox Talk")
def update_toolbox_talk(
    ctt_id: int,
    payload: CompositeToolboxTalkUpdate,
    db: Session = Depends(get_db)
):
    success = update_composite_toolbox_talk(db, ctt_id, payload)

    if not success:
        return {"message": "No fields to update"}

    return {
        "message": "Composite Toolbox Talk updated",
        "ctt_id": ctt_id
    }
