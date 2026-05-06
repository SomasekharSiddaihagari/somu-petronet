from fastapi import APIRouter, Depends, UploadFile, File, Form
from sqlalchemy.orm import Session
from sqlalchemy.sql import text
import os, uuid

from app.database import get_db
from app.schemas.permit_management.composite_toolbox_talk_participant_schema import (
    CompositeToolboxTalkParticipantCreate,
    CompositeToolboxTalkParticipantUpdate
)
from app.crud.permit_management.composite_toolbox_talk_participant_crud import (
    create_toolbox_talk_participant,
    update_toolbox_talk_participant
)

router = APIRouter(
    prefix="/composite-toolbox-talk-participant",
    tags=["Composite Toolbox Talk Participant"]
)

UPLOAD_DIR = "files/cwp/toolbox_participants"


# =================================================
# HELPER — SAVE SIGNATURE FILE
# =================================================
def _save_participant_signature(file: UploadFile, cttp_id: int) -> str:
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    ext = os.path.splitext(file.filename)[1]
    fname = f"participant_{cttp_id}_{uuid.uuid4().hex}{ext}"
    path = os.path.join(UPLOAD_DIR, fname)

    with open(path, "wb") as f:
        f.write(file.file.read())

    return f"/files/cwp/toolbox_participants/{fname}"


# =================================================
# POST — CREATE PARTICIPANT + SIGNATURE
# =================================================
@router.post("", summary="Create Toolbox Talk Participant")
def create_participant(
    toolbox_talk_id: int = Form(...),
    participant_name: str = Form(None),
    participant_signature_file: UploadFile = File(None),
    db: Session = Depends(get_db)
):
    payload = CompositeToolboxTalkParticipantCreate(
        toolbox_talk_id=toolbox_talk_id,
        participant_name=participant_name
    )

    # Create DB record first
    result = create_toolbox_talk_participant(db, payload)
    cttp_id = result["cttp_id"]

    updates = {}

    # Save signature if uploaded
    if participant_signature_file:
        updates["participant_signature"] = _save_participant_signature(
            participant_signature_file, cttp_id
        )

        sql = text("""
            UPDATE composite_toolbox_talk_participant
            SET participant_signature = :participant_signature
            WHERE cttp_id = :cttp_id
        """)

        db.execute(sql, {
            "participant_signature": updates["participant_signature"],
            "cttp_id": cttp_id
        })
        db.commit()

    return {
        "message": "Participant created",
        "cttp_id": cttp_id,
        **updates
    }


# =================================================
# PUT — UPDATE PARTICIPANT + SIGNATURE
# =================================================
@router.put("/{cttp_id}", summary="Update Toolbox Talk Participant")
def update_participant(
    cttp_id: int,
    participant_name: str = Form(None),
    participant_signature_file: UploadFile = File(None),
    db: Session = Depends(get_db)
):
    payload = CompositeToolboxTalkParticipantUpdate(
        participant_name=participant_name
    )

    # Update normal fields
    update_toolbox_talk_participant(db, cttp_id, payload)

    updates = {}

    # Update signature ONLY if new file uploaded
    if participant_signature_file:
        updates["participant_signature"] = _save_participant_signature(
            participant_signature_file, cttp_id
        )

        sql = text("""
            UPDATE composite_toolbox_talk_participant
            SET participant_signature = :participant_signature
            WHERE cttp_id = :cttp_id
        """)

        db.execute(sql, {
            "participant_signature": updates["participant_signature"],
            "cttp_id": cttp_id
        })
        db.commit()

    return {
        "message": "Participant updated",
        "cttp_id": cttp_id,
        **updates
    }
