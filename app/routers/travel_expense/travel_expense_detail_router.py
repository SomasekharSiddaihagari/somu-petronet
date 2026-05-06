from fastapi import APIRouter, Depends, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import Optional, List, Union
from app.database import get_db
from app.crud.travel_expense.travel_expense_detail_crud import (
    create_expense_detail,
    save_files,
    update_expense_detail,
    delete_expense_detail
)

router = APIRouter(prefix="/api/travel-expense-detail", tags=["Travel Expense Detail"])


# -------------------- CREATE --------------------
@router.post("/create")
def create_detail(
    db: Session = Depends(get_db),
    expense_sheet_id: int = Form(...),

    from_date: Optional[str] = Form(None),
    to_date: Optional[str] = Form(None),
    travel_route: Optional[str] = Form(None),
    from_location: Optional[str] = Form(None),
    to_location: Optional[str] = Form(None),

    air_rail_bus_amount: Optional[float] = Form(None),
    air_rail_bus_gst: Optional[float] = Form(None),
    air_rail_bus_total: Optional[float] = Form(None),

    hotel_amount: Optional[float] = Form(None),
    hotel_gst: Optional[float] = Form(None),
    hotel_total: Optional[float] = Form(None),

    daily_allowance_amount: Optional[float] = Form(None),
    daily_allowance_gst: Optional[float] = Form(None),
    daily_allowance_total: Optional[float] = Form(None),

    local_conveyance_amount: Optional[float] = Form(None),
    local_conveyance_gst: Optional[float] = Form(None),
    local_conveyance_total: Optional[float] = Form(None),

    other_amount: Optional[float] = Form(None),
    other_gst: Optional[float] = Form(None),
    other_total: Optional[float] = Form(None),

    remarks: Optional[str] = Form(None),
    user_id: Optional[int] = Form(None),
    is_overseas: Optional[bool] = Form(None),

    air_rail_bus_proof: List[UploadFile] = File(None),
    hotel_proof: List[UploadFile] = File(None),
    daily_allowance_proof: List[UploadFile] = File(None),
    local_conveyance_proof: List[UploadFile] = File(None),
    other_proof: List[UploadFile] = File(None),
):
    payload = locals()
    del payload["db"]

    upload_files = {
        "air_rail_bus_proof": air_rail_bus_proof,
        "hotel_proof": hotel_proof,
        "daily_allowance_proof": daily_allowance_proof,
        "local_conveyance_proof": local_conveyance_proof,
        "other_proof": other_proof,
    }

    return create_expense_detail(db, payload, upload_files)
from typing import Optional, List
from fastapi import UploadFile
from sqlalchemy.orm import Session
from sqlalchemy import text



from datetime import datetime
def to_date_safe(value):
    if value in ("", None, "null"):
        return None
    return datetime.strptime(value, "%Y-%m-%d").date()
 
def to_float(value):
    if value in ("", None, "null"):
        return None
    return float(value)
 
def empty_to_none(value):
    return None if value in ("", None, "null") else value

@router.put("/update/{tesd_id}")
def update_detail(
    tesd_id: int,
    db: Session = Depends(get_db),
 
    expense_sheet_id: Optional[int] = Form(None),
 
    from_date: Optional[datetime] = Form(None),
    to_date: Optional[datetime] = Form(None),
    travel_route: Optional[str] = Form(None),
    from_location: Optional[str] = Form(None),
    to_location: Optional[str] = Form(None),
 
    air_rail_bus_amount: Optional[str] = Form(None),
    air_rail_bus_gst: Optional[str] = Form(None),
    air_rail_bus_total: Optional[str] = Form(None),
 
    hotel_amount: Optional[str] = Form(None),
    hotel_gst: Optional[str] = Form(None),
    hotel_total: Optional[str] = Form(None),
 
    daily_allowance_amount: Optional[str] = Form(None),
    daily_allowance_gst: Optional[str] = Form(None),
    daily_allowance_total: Optional[str] = Form(None),
 
    local_conveyance_amount: Optional[str] = Form(None),
    local_conveyance_gst: Optional[str] = Form(None),
    local_conveyance_total: Optional[str] = Form(None),
 
    other_amount: Optional[str] = Form(None),
    other_gst: Optional[str] = Form(None),
    other_total: Optional[str] = Form(None),
 
    remarks: Optional[str] = Form(None),
    user_id: Optional[int] = Form(None),
    is_overseas: Optional[bool] = Form(None),
 
    air_rail_bus_proof: List[UploadFile] | None = File(None),
    hotel_proof: List[UploadFile] | None = File(None),
    daily_allowance_proof: List[UploadFile] | None = File(None),
    local_conveyance_proof: List[UploadFile] | None = File(None),
    other_proof: List[UploadFile] | None = File(None),
):
    payload = {
        "expense_sheet_id": expense_sheet_id,
        "from_date": from_date,
        "to_date": to_date,
        "travel_route": empty_to_none(travel_route),
        "from_location": empty_to_none(from_location),
        "to_location": empty_to_none(to_location),
 
        "air_rail_bus_amount": to_float(air_rail_bus_amount),
        "air_rail_bus_gst": to_float(air_rail_bus_gst),
        "air_rail_bus_total": to_float(air_rail_bus_total),
 
        "hotel_amount": to_float(hotel_amount),
        "hotel_gst": to_float(hotel_gst),
        "hotel_total": to_float(hotel_total),
 
        "daily_allowance_amount": to_float(daily_allowance_amount),
        "daily_allowance_gst": to_float(daily_allowance_gst),
        "daily_allowance_total": to_float(daily_allowance_total),
 
        "local_conveyance_amount": to_float(local_conveyance_amount),
        "local_conveyance_gst": to_float(local_conveyance_gst),
        "local_conveyance_total": to_float(local_conveyance_total),
 
        "other_amount": to_float(other_amount),
        "other_gst": to_float(other_gst),
        "other_total": to_float(other_total),
 
        "remarks": remarks,
        "user_id": user_id,
        "is_overseas": is_overseas,
    }
 
    upload_files = {
        "air_rail_bus_proof": air_rail_bus_proof,
        "hotel_proof": hotel_proof,
        "daily_allowance_proof": daily_allowance_proof,
        "local_conveyance_proof": local_conveyance_proof,
        "other_proof": other_proof,
    }
 
    return update_expense_detail(db, tesd_id, payload, upload_files)


# -------------------- DELETE --------------------
@router.delete("/delte/{tesd_id}")
def delete_detail(tesd_id: int, db: Session = Depends(get_db)):
    return delete_expense_detail(db, tesd_id)


