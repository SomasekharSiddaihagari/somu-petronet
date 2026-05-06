from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.circular_management.group_master_schema import GroupCreate, GroupUpdate
from app.crud.circular_management.group_master_crud import (
    create_group, get_all_employee, get_all_station_users, update_group, get_group, get_all_groups, delete_group
)

router = APIRouter(
    prefix="/group-master",
    tags=["Group Master"]
)

@router.post("/create")
def create_group_api(data: GroupCreate, db: Session = Depends(get_db)):
    group_id = create_group(db, data)
    return {"status": "success", "group_id": group_id}

@router.put("/update/{group_id}")
def update_group_api(
    group_id: int,
    data: GroupUpdate,
    db: Session = Depends(get_db)
):
    update_group(db, group_id, data)
    return {"status": "success", "message": "Group updated successfully"}

@router.get("/get/{group_id}")
def get_group_api(group_id: int, db: Session = Depends(get_db)):
    result = get_group(db, group_id)
    if not result:
        raise HTTPException(status_code=404, detail="Group not found")
    return result

@router.get("/get-all")
def get_all_groups_api(db: Session = Depends(get_db)):
    return get_all_groups(db)

@router.delete("/delete/{group_id}")
def delete_group_api(
    group_id: int,
    db: Session = Depends(get_db)
):
    success = delete_group(db, group_id)
    if not success:
        raise HTTPException(status_code=404, detail="Group not found or already deleted")

    return {
        "status": "success",
        "message": "Group deleted successfully"
    }

@router.get("/get-all-employee")
def get_all_employee_api(db: Session = Depends(get_db)):
    return get_all_employee(db)

@router.get("/get-all-station-users")
def get_all_station_users_api(db: Session = Depends(get_db)):
    return get_all_station_users(db)

