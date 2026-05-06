from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Optional
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.database import get_db

router = APIRouter(
    prefix="/shift-takeover",
    tags=["Shift Takeover"]
)

# =====================================================
# SCHEMAS (ALL FIELDS)
# =====================================================

class ShiftTakeoverCreate(BaseModel):
    shift_code: Optional[str]              # Shift A / B / C

    current_incharge_id: Optional[int]

    previous_shift_notes: Optional[str]
    takeover_notes: Optional[str]

    is_emergency: Optional[bool]
    emergency_assigned_to: Optional[int]

    status: Optional[str]                  # TAKEN_OVER / DRAFT
    created_by: Optional[int]


class ShiftTakeoverUpdate(ShiftTakeoverCreate):
    pass


# =====================================================
# POST — CREATE
# =====================================================

@router.post("")
def create_shift_takeover(
    payload: ShiftTakeoverCreate,
    db: Session = Depends(get_db)
):
    query = text("""
        INSERT INTO shift_takeover (
            shift_code,
            current_incharge_id,

            previous_shift_notes,
            takeover_notes,

            is_emergency,
            emergency_assigned_to,

            status,
            created_by
        )
        VALUES (
            :shift_code,
            :current_incharge_id,

            :previous_shift_notes,
            :takeover_notes,

            :is_emergency,
            :emergency_assigned_to,

            :status,
            :created_by
        )
        RETURNING shift_takeover_id
    """)

    result = db.execute(query, payload.dict())
    db.commit()

    return {
        "message": "Shift takeover created successfully",
        "shift_takeover_id": result.scalar()
    }


# =====================================================
# PUT — FULL UPDATE (ALL FIELDS)
# =====================================================

@router.put("/{shift_takeover_id}")
def update_shift_takeover(
    shift_takeover_id: int,
    payload: ShiftTakeoverUpdate,
    db: Session = Depends(get_db)
):
    params = payload.dict()
    params["id"] = shift_takeover_id

    query = text("""
        UPDATE shift_takeover
        SET
            shift_code = :shift_code,
            current_incharge_id = :current_incharge_id,

            previous_shift_notes = :previous_shift_notes,
            takeover_notes = :takeover_notes,

            is_emergency = :is_emergency,
            emergency_assigned_to = :emergency_assigned_to,

            status = :status,
            created_by = :created_by
        WHERE shift_takeover_id = :id
    """)

    result = db.execute(query, params)
    db.commit()

    if result.rowcount == 0:
        raise HTTPException(
            status_code=404,
            detail="Shift takeover record not found"
        )

    return {"message": "Shift takeover updated successfully"}


# =====================================================
# DELETE
# =====================================================

@router.delete("/{shift_takeover_id}")
def delete_shift_takeover(
    shift_takeover_id: int,
    db: Session = Depends(get_db)
):
    result = db.execute(
        text("""
            DELETE FROM shift_takeover
            WHERE shift_takeover_id = :id
        """),
        {"id": shift_takeover_id}
    )
    db.commit()

    if result.rowcount == 0:
        raise HTTPException(
            status_code=404,
            detail="Shift takeover record not found"
        )

    return {"message": "Shift takeover deleted successfully"}
