from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.utils.access_service import validate_token

from app.schemas.circular_management.circular_user_activity_schema import (
    CircularRead,
    CircularAcknowledge
)

from app.crud.circular_management.circular_user_activity_crud import (
    get_circular_user_activity,
    mark_circular_as_read,
    acknowledge_circular
)

router = APIRouter(
    prefix="/circular-user-activity",
    tags=["Circular User Activity"]
)

@router.post("/mark-read")
def mark_read_api(
    data: CircularRead,
    db: Session = Depends(get_db)
):
    mark_circular_as_read(
        db=db,
        circular_id=data.circular_id,
        user_id=data.user_id
    )

    return {
        "status": "success",
        "message": "Circular marked as read"
    }


@router.post("/acknowledge")
def acknowledge_api(
    data: CircularAcknowledge,
    db: Session = Depends(get_db)
):
    success = acknowledge_circular(
        db=db,
        circular_id=data.circular_id,
        user_id=data.user_id
    )

    if not success:
        raise HTTPException(
            status_code=404,
            detail="Circular read record not found"
        )

    return {
        "status": "success",
        "message": "Circular acknowledged successfully"
    }


# @router.get("/status/{circular_id}/{user_id}")
# def get_status(
#     circular_id: int,
#     user_id: int,
#     db: Session = Depends(get_db)
# ):
#     result = get_user_circular_activity(db, circular_id, user_id)

#     if not result:
#         return {
#             "status": "success",
#             "data": {
#                 "is_read": False,
#                 "is_acknowledged": False
#             }
#         }

#     return {
#         "status": "success",
#         "data": result
#     }
@router.get("/get/{circular_id}")
def get(circular_id: int, db: Session = Depends(get_db)):
    result = get_circular_user_activity(db, circular_id)
    return result