from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db

from app.schemas.travel_expense.travel_car_schema import (
   
    CarCreate, CarUpdate
)

from app.crud.travel_expense.travel_car_crud import (
    create_car, update_car, delete_car
)


router = APIRouter(prefix="/api/requisition-travel-car", tags=["Requisition Travel Car"])

    
# ---------------------- CAR ----------------------
@router.post("/create")
def create_car_api(data: CarCreate, db: Session = Depends(get_db)):
    return create_car(db, data)


@router.put("/update/{trc_id}")
def update_car_api(trc_id: int, data: CarUpdate, db: Session = Depends(get_db)):
    res = update_car(db, trc_id, data)
    if not res:
        raise HTTPException(404, "Car entry not found")
    return res


@router.delete("/delete/{trc_id}")
def delete_car_api(trc_id: int, db: Session = Depends(get_db)):
    return delete_car(db, trc_id)
