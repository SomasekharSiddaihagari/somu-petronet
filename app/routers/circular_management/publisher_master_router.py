from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.circular_management.publisher_master_schema import (
    PublisherCreate,
    PublisherUpdate
)
from app.crud.circular_management.publisher_master_crud import (
    create_publisher,
    update_publisher,
    get_publisher,
    get_all_publishers,
    update_publisher_status
)

router = APIRouter(prefix="/publisher", tags=["Publisher Master"])

@router.post("/create")
def create(data: PublisherCreate, db: Session = Depends(get_db)):
    publisher_id = create_publisher(db, data)

    return {
        "status": "success",
        "publisher_id": publisher_id
    }

@router.put("/update/{publisher_id}")
def update(
    publisher_id: int,
    data: PublisherUpdate,
    db: Session = Depends(get_db)
):
    update_publisher(db, publisher_id, data)

    return {
        "status": "success",
        "message": "Publisher updated successfully"
    }

@router.get("/get/{publisher_id}")
def get(publisher_id: int, db: Session = Depends(get_db)):
    result = get_publisher(db, publisher_id)

    return {
        "status": "success",
        "data": result
    }

@router.get("/get-all")
def get_all(db: Session = Depends(get_db)):
    result = get_all_publishers(db)

    return {
        "status": "success",
        "data": result
    }

@router.put(
    "/status_change/{publisher_id}",
    summary="Change ACTIVE / INACTIVE status by publisher"
)
def change_publisher_status(
    publisher_id: int,
    status: str,  
    db: Session = Depends(get_db)
):
    result = update_publisher_status(db, publisher_id, status)

    return {
        "status": "success",
        "data": result
    }
