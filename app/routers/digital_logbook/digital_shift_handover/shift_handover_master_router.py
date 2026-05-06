from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Optional
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.database import get_db

router = APIRouter(
    prefix="/shift-handover-master",
    tags=["Shift Handover Master"]
)

# =====================================================
# SCHEMAS (ALL FIELDS)
# =====================================================

class ShiftHandoverMasterCreate(BaseModel):
    next_incharge_id: Optional[int]
    notes_for_next_shift: Optional[str]


class ShiftHandoverMasterUpdate(ShiftHandoverMasterCreate):
    pass


# =====================================================
# POST — CREATE
# =====================================================

@router.post("")
def create_shift_handover_master(
    payload: ShiftHandoverMasterCreate,
    db: Session = Depends(get_db)
):
    query = text("""
        INSERT INTO shift_handover_master (
            next_incharge_id,
            notes_for_next_shift
        )
        VALUES (
            :next_incharge_id,
            :notes_for_next_shift
        )
        RETURNING handover_master_id
    """)

    result = db.execute(query, payload.dict())
    db.commit()

    return {
        "message": "Shift handover created successfully",
        "handover_master_id": result.scalar()
    }


# =====================================================
# PUT — FULL UPDATE
# =====================================================

@router.put("/{handover_master_id}")
def update_shift_handover_master(
    handover_master_id: int,
    payload: ShiftHandoverMasterUpdate,
    db: Session = Depends(get_db)
):
    params = payload.dict()
    params["id"] = handover_master_id

    query = text("""
        UPDATE shift_handover_master
        SET
            next_incharge_id = :next_incharge_id,
            notes_for_next_shift = :notes_for_next_shift
        WHERE handover_master_id = :id
    """)

    result = db.execute(query, params)
    db.commit()

    if result.rowcount == 0:
        raise HTTPException(
            status_code=404,
            detail="Shift handover record not found"
        )

    return {"message": "Shift handover updated successfully"}


# =====================================================
# DELETE
# =====================================================

@router.delete("/{handover_master_id}")
def delete_shift_handover_master(
    handover_master_id: int,
    db: Session = Depends(get_db)
):
    result = db.execute(
        text("""
            DELETE FROM shift_handover_master
            WHERE handover_master_id = :id
        """),
        {"id": handover_master_id}
    )
    db.commit()

    if result.rowcount == 0:
        raise HTTPException(
            status_code=404,
            detail="Shift handover record not found"
        )

    return {"message": "Shift handover deleted successfully"}
