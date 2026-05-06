from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import text
from typing import List

from app.database import get_db
from app.utils.access_service import validate_token
from app.schemas.digital_logbook.digital_erv_logbook.erv_vehicle_inspection_entry_schema import (
    ERVVehicleInspectionCreate,
    ERVVehicleInspectionUpdate,
    ERVVehicleInspectionResponse,
)
from app.crud.digital_logbook.digital_erv_logbook.erv_vehicle_inspection_entry_crud import (
    create_erv_vehicle_inspection,
    update_erv_vehicle_inspection,
    delete_erv_vehicle_inspection,
    get_erv_vehicle_inspection_by_id,
)

router = APIRouter(
    prefix="/erv-vehicle-inspection",
    tags=["ERV Logbook Vehicle Inspection"],
    dependencies=[Depends(validate_token)],
)




@router.post("", status_code=status.HTTP_201_CREATED)
def create(
    payload: ERVVehicleInspectionCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(validate_token),
):
    """Create a new ERV vehicle inspection log. Requires an existing erv_master_id (erv_id)."""
    master_exists = db.execute(
        text("SELECT 1 FROM erv_logbook_master WHERE erv_id = :eid"),
        {"eid": payload.category_master_id},
    ).first()
    if not master_exists:
        raise HTTPException(
            status_code=400,
            detail=f"ERV Master record with ID {payload.category_master_id} not found",
        )

    evi_id = create_erv_vehicle_inspection(db, payload, current_user.get("user_id"))
    return {
        "message": "ERV vehicle inspection log created successfully",
        "evi_id": evi_id,
    }

@router.put("/{evi_id}")
def update(
    evi_id: int,
    payload: ERVVehicleInspectionUpdate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(validate_token),
):
    """Update a vehicle inspection log and record to history."""
    updated = update_erv_vehicle_inspection(
        db, evi_id, payload, current_user.get("user_id")
    )
    if not updated:
        raise HTTPException(status_code=404, detail="Vehicle inspection log not found")
    return {"message": "ERV vehicle inspection log updated successfully"}

@router.delete("/{evi_id}")
def delete(
    evi_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(validate_token),
):
    """Delete a vehicle inspection log and archive it to history."""
    deleted = delete_erv_vehicle_inspection(db, evi_id, current_user.get("user_id"))
    if not deleted:
        raise HTTPException(status_code=404, detail="Vehicle inspection log not found")
    return {"message": "ERV vehicle inspection log deleted successfully"}

@router.get("/{evi_id}", response_model=ERVVehicleInspectionResponse)
def fetch_by_id(evi_id: int, db: Session = Depends(get_db)):
    """Fetch a specific ERV vehicle inspection log by its ID."""
    inspection = get_erv_vehicle_inspection_by_id(db, evi_id)
    if not inspection:
        raise HTTPException(status_code=404, detail="Vehicle inspection log not found")
    return inspection

