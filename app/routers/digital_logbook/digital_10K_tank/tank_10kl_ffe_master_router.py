# app/routers/digital_logbook/digital_10K_tank/tank_10kl_ffe_master_router.py
from datetime import date
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional

from app.database import get_db
from app.utils.access_service import validate_token
from app.schemas.digital_logbook.digital_10K_tank.tank_10kl_ffe_master_schema import (
    Tank10KLFfeResponse,
    Tank10KLFfeCreate,
    Tank10KLFfeUpdate,
)
from app.crud.digital_logbook.digital_10K_tank.tank_10kl_ffe_master_crud import (
    get_tank_10kl_ffe_by_id,
    get_combined_tank_ffe_by_date,
    create_tank_10kl_ffe,
    update_tank_10kl_ffe,
    delete_tank_10kl_ffe,
)

router = APIRouter(
    prefix="/tank-10kl-ffe-master",
    tags=["Tank 10KL FFE Master"],
    dependencies=[Depends(validate_token)],
)



@router.post("", status_code=status.HTTP_201_CREATED)
def create_master(
    payload: Tank10KLFfeCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(validate_token),
):
    """Create a new Tank 10KL FFE Master record."""
    tank_ffe_id = create_tank_10kl_ffe(db, payload, current_user.get("user_id"))
    return {"message": "Master record created successfully", "tank_ffe_id": tank_ffe_id}

@router.put("/{tank_ffe_id}")
def update_master(
    tank_ffe_id: int,
    payload: Tank10KLFfeUpdate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(validate_token),
):
    """Update a Tank 10KL FFE Master record and recorded to history."""
    updated = update_tank_10kl_ffe(
        db, tank_ffe_id, payload, current_user.get("user_id")
    )
    if not updated:
        raise HTTPException(status_code=404, detail="Master record not found")
    return {"message": "Master record updated successfully"}

@router.delete("/{tank_ffe_id}")
def delete_master(
    tank_ffe_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(validate_token),
):
    """Delete a Tank 10KL FFE Master record and archive it to history."""
    deleted = delete_tank_10kl_ffe(db, tank_ffe_id, current_user.get("user_id"))
    if not deleted:
        raise HTTPException(status_code=404, detail="Master record not found")
    return {"message": "Master record deleted successfully"}

@router.get("/get-all-entries-by-date-range", response_model=List[Tank10KLFfeResponse])
def fetch_by_date_range(from_date: date, to_date: date, db: Session = Depends(get_db)):
    """Fetch records within a specified date range."""
    return get_combined_tank_ffe_by_date(db, from_date, to_date)

@router.get("/{tank_ffe_id}", response_model=Tank10KLFfeResponse)
def fetch_by_id(tank_ffe_id: int, db: Session = Depends(get_db)):
    """Fetch a single record by Master ID."""
    data = get_tank_10kl_ffe_by_id(db, tank_ffe_id)
    if not data:
        raise HTTPException(status_code=404, detail="Master record not found")
    return data

