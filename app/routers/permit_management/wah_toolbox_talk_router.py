from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.permit_management.wah_toolbox_talk_schema import (
    WorkAtHeightToolboxTalkCreate,
    WorkAtHeightToolboxTalkUpdate
)
from app.crud.permit_management.wah_toolbox_talk_crud import (
    create_wah_toolbox_talk,
    update_wah_toolbox_talk
)

router = APIRouter(
    prefix="/work-at-height/toolbox-talk",
    tags=["Work At Height - Toolbox Talk"]
)


# =================================================
# POST — CREATE TOOLBOX TALK
# =================================================
@router.post("", summary="Create Work At Height Toolbox Talk")
def create_toolbox_talk_api(
    payload: WorkAtHeightToolboxTalkCreate,
    db: Session = Depends(get_db)
):
    return create_wah_toolbox_talk(db, payload)


# =================================================
# PUT — UPDATE TOOLBOX TALK
# =================================================
@router.put("/{whtt_id}", summary="Update Work At Height Toolbox Talk")
def update_toolbox_talk_api(
    whtt_id: int,
    payload: WorkAtHeightToolboxTalkUpdate,
    db: Session = Depends(get_db)
):
    success = update_wah_toolbox_talk(db, whtt_id, payload)
    if not success:
        return {"message": "No fields to update"}

    return {"message": "Toolbox Talk updated", "whtt_id": whtt_id}
