from sqlalchemy import desc
from sqlalchemy.orm import Session
from datetime import datetime
from app.models.employees_info.user_vehicle import UserVehicle
from app.models.employees_info.user_vehicle_history import UserVehicleHistory
from app.routers.UserAuthR2 import make_download_url
from app.schemas.employees_info.user_vehicle_schemas import (
    UserVehicleCreate,
    UserVehicleUpdate
)


# --------------------------------
# Helper: Create History Snapshot
# --------------------------------
def get_user_vehicle_by_id(db: Session, vehicle_id: int):
    return db.query(UserVehicle).filter(
        UserVehicle.id == vehicle_id
    ).first()



def create_vehicle_history(db: Session, vehicle: UserVehicle):
    history = UserVehicleHistory(
        user_id=vehicle.user_id,
        vehicle_type=vehicle.vehicle_type,
        vehicle_make=vehicle.vehicle_make,
        vehicle_model=vehicle.vehicle_model,
        color=vehicle.color,
        fuel_type=vehicle.fuel_type,
        vehicle_registration_no=vehicle.vehicle_registration_no,
        rc_expiry_date=vehicle.rc_expiry_date,
        insurance_provider=vehicle.insurance_provider,
        insurance_policy_number=vehicle.insurance_policy_number,
        insurance_expiry_date=vehicle.insurance_expiry_date,
        puc_expiry_date=vehicle.puc_expiry_date,
        document_upload=vehicle.document_upload,
        history_created_at=datetime.now()
    )
    db.add(history)


# --------------------------------
# CREATE
# --------------------------------
def create_user_vehicle(db: Session, payload: UserVehicleCreate):
    vehicle = UserVehicle(**payload.dict())
    db.add(vehicle)
    db.flush()         # ← assigns ID without committing yet
    db.refresh(vehicle)

    create_vehicle_history(db, vehicle)  # should only db.add(), no commit inside

    db.commit()        # ← single commit saves both vehicle + history together
    db.refresh(vehicle)

    return vehicle


# --------------------------------
# READ (by user)
# --------------------------------
def get_user_vehicles(db: Session, user_id: int):
    vehicles = db.query(UserVehicle).filter(
        UserVehicle.user_id == user_id
    ).order_by(desc(UserVehicle.id)).all()

    for vehicle in vehicles:
        if vehicle.document_upload:
            # Split by comma, generate URL for each, return as list
            docs = vehicle.document_upload.split(",")
            vehicle.download_url = [make_download_url(doc.strip()) for doc in docs]
        else:
            vehicle.download_url = []
    
    return vehicles

# --------------------------------
# UPDATE
# --------------------------------
def update_user_vehicle(
    db: Session,
    vehicle_id: int,
    payload: UserVehicleUpdate,
    changed_fields: list | None = None
):
    vehicle = db.query(UserVehicle).filter(
        UserVehicle.id == vehicle_id
    ).first()

    if not vehicle:
        return None

    for key, value in payload.dict(exclude_unset=True).items():
        setattr(vehicle, key, value)

    vehicle.modified_date = datetime.now()
        # ✅ FIX: Ensure always list (NOT string)
    if isinstance(changed_fields, str):
        import json
        changed_fields = json.loads(changed_fields)

    vehicle.changed_fields = changed_fields or []

    create_vehicle_history(db, vehicle)

    db.commit()
    db.refresh(vehicle)
        # ✅ FIX: Ensure response always list
    if isinstance(vehicle.changed_fields, str):
        import json
        vehicle.changed_fields = json.loads(vehicle.changed_fields)

    if vehicle.changed_fields is None:
        vehicle.changed_fields = []

    return vehicle


# --------------------------------
# DELETE
# --------------------------------
def delete_user_vehicle(db: Session, vehicle_id: int):
    vehicle = db.query(UserVehicle).filter(
        UserVehicle.id == vehicle_id
    ).first()

    if not vehicle:
        return None

    create_vehicle_history(db, vehicle)

    db.delete(vehicle)
    db.commit()
    return True


# --------------------------------
# HISTORY
# --------------------------------
def get_vehicle_history(db: Session, user_id: int):
    return db.query(UserVehicleHistory).filter(
        UserVehicleHistory.user_id == user_id
    ).order_by(UserVehicleHistory.history_created_at.desc()).all()
