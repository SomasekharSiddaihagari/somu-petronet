from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db

from app.schemas.travel_expense.travel_hotel_schema import (
  
    HotelCreate, HotelUpdate,
    
)

from app.crud.travel_expense.travel_hotel_crud import (
    
    create_hotel, update_hotel, delete_hotel,
    
)


router = APIRouter(prefix="/api/requisition-travel-hotel", tags=["Requisition Travel Hotel"])



# ---------------------- HOTEL ----------------------
@router.post("/create")
def create_hotel_api(data: HotelCreate, db: Session = Depends(get_db)):
    return create_hotel(db, data)


@router.put("/update/{trh_id}")
def update_hotel_api(trh_id: int, data: HotelUpdate, db: Session = Depends(get_db)):
    res = update_hotel(db, trh_id, data)
    if not res:
        raise HTTPException(404, "Hotel entry not found")
    return res


@router.delete("/delete/{trh_id}")
def delete_hotel_api(trh_id: int, db: Session = Depends(get_db)):
    return delete_hotel(db, trh_id)

