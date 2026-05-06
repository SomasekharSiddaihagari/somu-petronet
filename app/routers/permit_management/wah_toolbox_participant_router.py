from fastapi import APIRouter, Depends, UploadFile, File, Form
from sqlalchemy.orm import Session
from sqlalchemy.sql import text
import os, uuid

from app.database import get_db
from app.schemas.permit_management.wah_toolbox_participant_schema import (
    WorkAtHeightToolboxTalkParticipantCreate,
    WorkAtHeightToolboxTalkParticipantUpdate
)
from app.crud.permit_management.wah_toolbox_participant_crud import (
    create_wah_toolbox_participant,
    update_wah_toolbox_participant
)

router = APIRouter(
    prefix="/work-at-height/toolbox-talk-participant",
    tags=["WAH Toolbox Talk Participant"]
)

UPLOAD_DIR = "files/wah/toolbox_participants"


# ================================================
# HELPER — Save signature file
# ================================================
def _save_participant_signature(
    file: UploadFile,
    whttp_id: int
) -> str:
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    ext = os.path.splitext(file.filename)[1]
    fname = f"whttp_{whttp_id}_{uuid.uuid4().hex}{ext}"
    path = os.path.join(UPLOAD_DIR, fname)

    with open(path, "wb") as f:
        f.write(file.file.read())

    return f"/files/wah/toolbox_participants/{fname}"


# ================================================
# POST — CREATE PARTICIPANT + SIGNATURE
# ================================================
@router.post("", summary="Create Toolbox Talk Participant")
def create_participant(
    toolbox_talk_id: int = Form(...),
    participant_name: str = Form(None),
    participant_signature_file: UploadFile = File(None),
    db: Session = Depends(get_db)
):
    payload = {
        "toolbox_talk_id": toolbox_talk_id,
        "participant_name": participant_name,
        "participant_signature": None
    }

    # Create participant first
    obj = WorkAtHeightToolboxTalkParticipantCreate(**payload)
    result = create_wah_toolbox_participant(db, obj)
    whttp_id = result["whttp_id"]

    updates = {}

    # Save signature if uploaded
    if participant_signature_file:
        updates["participant_signature"] = _save_participant_signature(
            participant_signature_file,
            whttp_id
        )

        sql = text("""
            UPDATE work_at_height_toolbox_talk_participant
            SET participant_signature = :path
            WHERE whttp_id = :whttp_id
        """)
        db.execute(sql, {
            "path": updates["participant_signature"],
            "whttp_id": whttp_id
        })
        db.commit()

    return {
        "message": "Participant created",
        "whttp_id": whttp_id,
        **updates
    }


# ================================================
# PUT — UPDATE PARTICIPANT + SIGNATURE
# ================================================
@router.put("/{whttp_id}", summary="Update Toolbox Talk Participant")
def update_participant(
    whttp_id: int,
    participant_name: str = Form(None),
    participant_signature_file: UploadFile = File(None),
    db: Session = Depends(get_db)
):
    payload = {}

    if participant_name is not None:
        payload["participant_name"] = participant_name

    if payload:
        obj = WorkAtHeightToolboxTalkParticipantUpdate(**payload)
        update_wah_toolbox_participant(db, whttp_id, obj)

    updates = {}

    # Update signature ONLY if new file uploaded
    if participant_signature_file:
        updates["participant_signature"] = _save_participant_signature(
            participant_signature_file,
            whttp_id
        )

        sql = text("""
            UPDATE work_at_height_toolbox_talk_participant
            SET participant_signature = :path
            WHERE whttp_id = :whttp_id
        """)
        db.execute(sql, {
            "path": updates["participant_signature"],
            "whttp_id": whttp_id
        })
        db.commit()

    return {
        "message": "Participant updated",
        "whttp_id": whttp_id,
        **updates
    }
