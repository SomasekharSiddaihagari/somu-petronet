from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db

from app.schemas.travel_expense.travel_travel_schema import (
    TravelCreate, TravelUpdate,

)

from app.crud.travel_expense.travel_travel_crud import (
    create_travel, update_travel, delete_travel,
  
)


router = APIRouter(prefix="/api/requisition-travel-details", tags=["Requisition Travel Details"])
    

# ---------------------- TRAVEL ----------------------
@router.post("/create")
def create_travel_api(data: TravelCreate, db: Session = Depends(get_db)):
    return create_travel(db, data)


@router.put("/update/{trt_id}")
def update_travel_api(trt_id: int, data: TravelUpdate, db: Session = Depends(get_db)):
    res = update_travel(db, trt_id, data)
    if not res:
        raise HTTPException(404, "Travel entry not found")
    return res


@router.delete("/delete/{trt_id}")
def delete_travel_api(trt_id: int, db: Session = Depends(get_db)):
    return delete_travel(db, trt_id)



