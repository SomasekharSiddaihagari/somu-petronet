# app/routers/digital_logbook/digital_10K_tank/tank_10kl_ffe_entry_router.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import text
from typing import List

from app.database import get_db
from app.utils.access_service import validate_token
from app.schemas.digital_logbook.digital_10K_tank.tank_10kl_ffe_entry_schema import (
    Tank10KLFfeEntryCreate,
    Tank10KLFfeEntryUpdate,
    Tank10KLFfeEntryResponse,
)
from app.crud.digital_logbook.digital_10K_tank.tank_10kl_ffe_entry_crud import (
    create_tank_10kl_ffe_entry,
    update_tank_10kl_ffe_entry,
    delete_tank_10kl_ffe_entry,
    get_tank_10kl_ffe_entry_by_id,
)

router = APIRouter(
    prefix="/tank-10kl-ffe-entry",
    tags=["Tank 10KL FFE Entry"],
    dependencies=[Depends(validate_token)],
)




@router.post("", status_code=status.HTTP_201_CREATED)
def create(
    payload: Tank10KLFfeEntryCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(validate_token),
):
    """Create a new Tank 10KL FFE entry. Requires an existing master_id (tank_ffe_id)."""
    if not payload.master_id:
        raise HTTPException(status_code=400, detail="master_id is required")

    master_exists = db.execute(
        text("SELECT 1 FROM tank_10kl_ffe_master WHERE tank_ffe_id = :id"),
        {"id": payload.master_id},
    ).first()
    if not master_exists:
        raise HTTPException(
            status_code=400,
            detail=f"Master record with ID {payload.master_id} not found",
        )

    new_id = create_tank_10kl_ffe_entry(db, payload, current_user.get("user_id"))
    return {
        "message": "Tank 10KL FFE entry created successfully",
        "tank_ffe_entry_id": new_id,
    }

@router.put("/{tank_ffe_entry_id}")
def update(
    tank_ffe_entry_id: int,
    payload: Tank10KLFfeEntryUpdate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(validate_token),
):
    """Update a Tank 10KL FFE entry and record to history."""
    updated = update_tank_10kl_ffe_entry(
        db, tank_ffe_entry_id, payload, current_user.get("user_id")
    )
    if not updated:
        raise HTTPException(status_code=404, detail="Entry record not found")
    return {"message": "Tank 10KL FFE entry updated successfully"}

@router.delete("/{tank_ffe_entry_id}")
def delete(
    tank_ffe_entry_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(validate_token),
):
    """Delete a Tank 10KL FFE entry and archive it to history."""
    deleted = delete_tank_10kl_ffe_entry(
        db, tank_ffe_entry_id, current_user.get("user_id")
    )
    if not deleted:
        raise HTTPException(status_code=404, detail="Entry record not found")
    return {"message": "Tank 10KL FFE entry deleted successfully"}

@router.get("/{tank_ffe_entry_id}", response_model=Tank10KLFfeEntryResponse)
def fetch_by_id(tank_ffe_entry_id: int, db: Session = Depends(get_db)):
    """Fetch a single entry record by its specific ID."""
    data = get_tank_10kl_ffe_entry_by_id(db, tank_ffe_entry_id)
    if not data:
        raise HTTPException(status_code=404, detail="Entry record not found")
    return data

