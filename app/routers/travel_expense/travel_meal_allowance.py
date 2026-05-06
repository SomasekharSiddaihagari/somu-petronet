
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from app.crud.travel_expense.meal_allowance_notification_crud import handle_meal_allowance_status_change
from app.crud.travel_expense.travel_meal_allowance import create_meal_detail, create_meal_sheet, delete_meal_detail,  update_meal_detail, update_meal_sheet
from app.database import get_db
import os
import shutil
import uuid

from app.schemas.travel_expense.travel_forms_schema import MealAllowanceCreate, MealAllowanceDetailResponse, MealAllowanceResponse, MealAllowanceUpdate




router = APIRouter(
    prefix="/api/travel/meal",
    tags=["Travel Meal Allowance"]
)


UPLOAD_DIR = "files/meal_proofs"
os.makedirs(UPLOAD_DIR, exist_ok=True)

from fastapi import BackgroundTasks

@router.post("/create", response_model=MealAllowanceResponse)
async def create_meal(
    data: MealAllowanceCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
):
    sheet = create_meal_sheet(db, data.model_dump())

    # 🔔 Notify Supervisor
    from app.crud.travel_expense.meal_allowance_notification_crud import (
        notify_supervisor_on_ma_create
    )

    await notify_supervisor_on_ma_create(
        db=db,
        sheet=sheet,
        background_tasks=background_tasks
    )

    return sheet


from fastapi import BackgroundTasks

@router.put("/update/{meal_sheet_id}", response_model=MealAllowanceResponse)
async def update_meal(
    meal_sheet_id: int,
    data: MealAllowanceUpdate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    payload = data.model_dump(exclude_unset=True)

    sheet = update_meal_sheet(db, meal_sheet_id, payload)
    if not sheet:
        raise HTTPException(status_code=404, detail="Meal sheet not found")

    # 🔔 SINGLE UNIFIED NOTIFICATION HANDLER
    await handle_meal_allowance_status_change(
        db=db,
        sheet=sheet,
        background_tasks=background_tasks
    )

    return sheet




# @router.delete("/delete/{meal_sheet_id}")
# def delete_meal(
#     meal_sheet_id: int,
#     db: Session = Depends(get_db)
# ):
#     deleted_id = delete_meal_sheet(db, meal_sheet_id)

#     if not deleted_id:
#         raise HTTPException(status_code=404, detail="Meal sheet not found")

#     return {
#         "meal_sheet_id": deleted_id,
#         "message": "Meal sheet deleted successfully"
#     }



# -------- POST --------
@router.post("/detail/create", response_model=MealAllowanceDetailResponse)
def create_detail(
    meal_sheet_id: int = Form(...),
    date: str = Form(None),
    from_time: str = Form(None),       
    to_time: str = Form(None),         
    travel_route: str = Form(None),
    time_duration: str = Form(None),
    distance_from_station: str = Form(None),
    purpose: str = Form(None),
    meal_amount: float = Form(None),
    meal_gst: float = Form(None),
    meal_total: float = Form(None),
    remarks: str = Form(None),
    file: UploadFile = File(None),
    db: Session = Depends(get_db)
):
    file_path = None

    if file:
        filename = f"{uuid.uuid4().hex}_{file.filename}"
        file_path = os.path.join(UPLOAD_DIR, filename)

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

    payload = {
        "meal_sheet_id": meal_sheet_id,
        "date": date,
        "from_time": from_time,        
        "to_time": to_time,            
        "travel_route": travel_route,
        "time_duration": time_duration,
        "distance_from_station": distance_from_station,
        "purpose": purpose,
        "meal_amount": meal_amount,
        "meal_gst": meal_gst,
        "meal_total": meal_total,
        "meal_proof": file_path,
        "remarks": remarks
    }

    return create_meal_detail(db, payload)



# -------- PUT --------
@router.put("/detail/update/{meal_sheet_detail_id}", response_model=MealAllowanceDetailResponse)
def update_detail(
    meal_sheet_detail_id: int,
    date: str = Form(None),
    from_time: str = Form(None),       
    to_time: str = Form(None),         
    travel_route: str = Form(None),
    time_duration: str = Form(None),
    distance_from_station: str = Form(None),
    purpose: str = Form(None),
    meal_amount: float = Form(None),
    meal_gst: float = Form(None),
    meal_total: float = Form(None),
    remarks: str = Form(None),
    file: UploadFile = File(None),
    db: Session = Depends(get_db)
):
    payload = {}

    for key, value in {
        "date": date,
        "from_time": from_time,        
        "to_time": to_time,            
        "travel_route": travel_route,
        "time_duration": time_duration,
        "distance_from_station": distance_from_station,
        "purpose": purpose,
        "meal_amount": meal_amount,
        "meal_gst": meal_gst,
        "meal_total": meal_total,
        "remarks": remarks
    }.items():
        if value is not None:
            payload[key] = value

    if file:
        filename = f"{uuid.uuid4().hex}_{file.filename}"
        file_path = os.path.join(UPLOAD_DIR, filename)

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        payload["meal_proof"] = file_path

    updated = update_meal_detail(db, meal_sheet_detail_id, payload)

    if not updated:
        raise HTTPException(status_code=404, detail="Meal detail not found")

    return updated



# # -------- DELETE --------
# @router.delete("/detail/delete/{meal_sheet_detail_id}")
# def delete_detail(detail_id: int, db: Session = Depends(get_db)):
#     success = delete_meal_detail(db, detail_id)

#     if not success:
#         raise HTTPException(status_code=404, detail="Meal detail not found")

#     return {"message": "Meal allowance detail deleted successfully"}

# -------- DELETE --------
@router.delete("/detail/delete/{meal_sheet_detail_id}")
def delete_detail(
    meal_sheet_detail_id: int,  # ← was `detail_id`, must match path param
    db: Session = Depends(get_db)
):
    success = delete_meal_detail(db, meal_sheet_detail_id)

    if not success:
        raise HTTPException(status_code=404, detail="Meal detail not found")

    return {"message": "Meal allowance detail deleted successfully"}
