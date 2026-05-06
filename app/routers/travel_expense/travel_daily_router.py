import uuid
from fastapi import APIRouter, BackgroundTasks, UploadFile, File, Form, Depends
from typing import List, Optional, Union
from sqlalchemy import text
from sqlalchemy.orm import Session
from datetime import date, datetime
from decimal import Decimal
from decimal import Decimal
from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.crud.travel_expense.daily_allowance_notification_crud import handle_daily_allowance_status_change, notify_supervisor_on_da_create
from app.crud.travel_expense.travel_daily_allowance_crud import  create_sheet, delete_da_detail_sql, get_da_detail_by_id_sql, save_file,  update_sheet
from app.database import get_db
from app.schemas.travel_expense.travel_daily_schema import DailyAllowanceDetailCreate, DailyAllowanceDetailUpdate, DailyAllowanceSheetCreate, DailyAllowanceSheetResponse, DailyAllowanceSheetUpdate

import os
import shutil
import json
from datetime import datetime
from typing import List
from sqlalchemy import text
from sqlalchemy.orm import Session
from fastapi import UploadFile, HTTPException
 
from app.models.travel_expense.daily_allowance_sheet import DailyAllowanceSheet
from app.models.travel_expense.daily_allowance_sheet_history import DailyAllowanceSheetHistory
from app.models.travel_expense.daily_allowance_sheet_details import DailyAllowanceSheetDetail
from app.models.travel_expense.daily_allowance_sheet_details_history import DailyAllowanceSheetDetailHistory
from app.routers.UserAuth import save_file
from app.schemas.travel_expense.travel_daily_schema import DailyAllowanceSheetCreate, DailyAllowanceSheetUpdate


router = APIRouter(
    prefix="/api/da",
    tags=["Daily Allowance"]
)


UPLOAD_DIR = "files/da"
os.makedirs(UPLOAD_DIR, exist_ok=True)

def save_da_files(files: Optional[List[UploadFile]]) -> Optional[str]:
    if not files:
        return None

    os.makedirs(UPLOAD_DIR, exist_ok=True)
    paths = []

    for file in files:
        ext = os.path.splitext(file.filename)[1]
        filename = f"{uuid.uuid4()}{ext}"
        full_path = os.path.join(UPLOAD_DIR, filename)

        with open(full_path, "wb") as f:
            f.write(file.file.read())

        paths.append(full_path)

    return ",".join(paths)
@router.post("/allowanceDetails")
def create_allowance_detail(
    da_sheet_id: Optional[int] = Form(None),
    user_id: Optional[int] = Form(None),

    from_date: Optional[str] = Form(None),
    from_date_time: Optional[datetime] = Form(None),
    to_date_time: Optional[datetime] = Form(None),

    time_duration: Optional[str] = Form(None),
    travel_from: Optional[str] = Form(None),
    travel_to: Optional[str] = Form(None),
    distance_from_station: Optional[str] = Form(None),
    purpose: Optional[str] = Form(None),

    da_amount: Optional[float] = Form(None),
    da_gst: Optional[float] = Form(None),
    da_total: Optional[float] = Form(None),

    remarks: Optional[str] = Form(None),
    from_location: Optional[str] = Form(None),
    to_location: Optional[str] = Form(None),

    files: Optional[List[UploadFile]] = File(None),
    db: Session = Depends(get_db)
):
    da_proof = save_da_files(files)

    allowance = DailyAllowanceSheetDetail(
        da_sheet_id=da_sheet_id,
        user_id=user_id,
        from_date=from_date,
        from_date_time=from_date_time,
        to_date_time=to_date_time,
        time_duration=time_duration,
        travel_from=travel_from,
        travel_to=travel_to,
        distance_from_station=distance_from_station,
        purpose=purpose,
        da_amount=da_amount,
        da_gst=da_gst,
        da_total=da_total,
        remarks=remarks,
        from_location=from_location,
        to_location=to_location,
        da_proof=da_proof
    )

    db.add(allowance)
    db.commit()
    db.refresh(allowance)

    return {
        "message": "Daily allowance created successfully",
        "data": allowance
    }
@router.put("/allowanceDetails/{allowance_id}")
def update_allowance_detail(
    allowance_id: int,

    da_sheet_id: Optional[int] = Form(None),
    user_id: Optional[int] = Form(None),

    from_date: Optional[str] = Form(None),
    from_date_time: Optional[datetime] = Form(None),
    to_date_time: Optional[datetime] = Form(None),

    time_duration: Optional[str] = Form(None),
    travel_from: Optional[str] = Form(None),
    travel_to: Optional[str] = Form(None),
    distance_from_station: Optional[str] = Form(None),
    purpose: Optional[str] = Form(None),

    da_amount: Optional[float] = Form(None),
    da_gst: Optional[float] = Form(None),
    da_total: Optional[float] = Form(None),

    remarks: Optional[str] = Form(None),
    from_location: Optional[str] = Form(None),
    to_location: Optional[str] = Form(None),

    files: Optional[List[UploadFile]] = File(None),

    db: Session = Depends(get_db)
):
    allowance = db.query(DailyAllowanceSheetDetail).filter(
        DailyAllowanceSheetDetail.da_sheet_detail_id == allowance_id
    ).first()

    if not allowance:
        raise HTTPException(status_code=404, detail="Daily allowance not found")

    # --- Scalar fields (update only if explicitly provided) ---
    update_map = {
        "da_sheet_id": da_sheet_id,
        "user_id": user_id,
        "from_date": from_date,
        "from_date_time": from_date_time,
        "to_date_time": to_date_time,
        "time_duration": time_duration,
        "travel_from": travel_from,
        "travel_to": travel_to,
        "distance_from_station": distance_from_station,
        "purpose": purpose,
        "da_amount": da_amount,
        "da_gst": da_gst,
        "da_total": da_total,
        "remarks": remarks,
        "from_location": from_location,
        "to_location": to_location,
    }

    for field, value in update_map.items():
        if value is not None:
            setattr(allowance, field, value)

    # --- File handling (append, never nullify) ---
    new_files = save_da_files(files)
    if new_files:
        if allowance.da_proof:
            allowance.da_proof = f"{allowance.da_proof},{new_files}"
        else:
            allowance.da_proof = new_files

    db.commit()
    db.refresh(allowance)

    return {
        "message": "Daily allowance updated successfully",
        "data": allowance
    }


# ---------------- POST API ----------------

@router.post("/allowance", response_model=DailyAllowanceSheetResponse)
async def create_daily_allowance(
    data: DailyAllowanceSheetCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
):
    sheet = create_sheet(db, data)

    # 🔔 Notify Supervisor ONLY
    await notify_supervisor_on_da_create(
        db=db,
        sheet=sheet,
        background_tasks=background_tasks,
    )

    return sheet


# ============================================================
# UPDATE DAILY ALLOWANCE
# ============================================================

@router.put("/allowance/{sheet_id}", response_model=DailyAllowanceSheetResponse)
async def update_daily_allowance(
    sheet_id: int,
    data: DailyAllowanceSheetUpdate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
):
    sheet = update_sheet(db, sheet_id, data)
    if not sheet:
        raise HTTPException(status_code=404, detail="Sheet not found")

    # 🔔 Status-driven notification handler
    await handle_daily_allowance_status_change(
        db=db,
        sheet=sheet,
        background_tasks=background_tasks,
    )

    return sheet



from fastapi import Form
@router.post("/allowanceDetails")
async def create_da(
    user_id: int = Form(None),
    da_sheet_id: int = Form(None),

    from_date: str = Form(None),
    time_duration: str = Form(None),
    travel_from: str = Form(None),
    travel_to: str = Form(None),
    distance_from_station: str = Form(None),
    purpose: str = Form(None),

    da_amount: float = Form(None),
    da_gst: float = Form(None),
    da_total: float = Form(None),

    remarks: str = Form(None),

    from_location: str = Form(None),
    to_location: str = Form(None),

    from_date_time: str = Form(None),
    to_date_time: str = Form(None),

    files: UploadFile | None = File(None),
    db: Session = Depends(get_db)
):
    # Convert date (string → date)
    parsed_from_date = None
    if from_date:
        try:
            # Handles "YYYY-MM-DD" OR "YYYY-MM-DDTHH:MM:SS"
            dt = datetime.fromisoformat(from_date)
            parsed_from_date = dt.date()
        except:
            parsed_from_date = date.fromisoformat(from_date)

    # Convert datetime (string → datetime)
    parsed_from_date_time = None
    parsed_to_date_time = None

    if from_date_time:
        parsed_from_date_time = datetime.fromisoformat(from_date_time)

    if to_date_time:
        parsed_to_date_time = datetime.fromisoformat(to_date_time)

    payload = DailyAllowanceDetailCreate(
        user_id=user_id,
        da_sheet_id=da_sheet_id,
        from_date=parsed_from_date,
        time_duration=time_duration,
        travel_from=travel_from,
        travel_to=travel_to,
        distance_from_station=distance_from_station,
        purpose=purpose,
        da_amount=da_amount,
        da_gst=da_gst,
        da_total=da_total,
        remarks=remarks,
        from_location=from_location,
        to_location=to_location,
        from_date_time=parsed_from_date_time,
        to_date_time=parsed_to_date_time,
    )

    return create_da_detail_sql(db, payload, files)


UPLOAD_ROOT = "files/daily_allowance"
os.makedirs(UPLOAD_ROOT, exist_ok=True)


def save_files(files: list[UploadFile]) -> list[str]:
    paths = []

    for file in files:
        if not file.filename:
            continue

        filename = f"{int(datetime.now().timestamp())}_{file.filename}"
        file_path = os.path.join(UPLOAD_ROOT, filename)

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        paths.append(os.path.abspath(file_path).replace("\\", "/"))

    return paths


def create_da_detail_sql(db, data, files):
    file_paths = save_files(files) if files else []
    da_proof = ",".join(file_paths) if file_paths else None

    sql = text("""
        INSERT INTO daily_allowance_sheet_detail (
            da_sheet_id, user_id, from_date, time_duration,
            travel_from, travel_to, distance_from_station,
            purpose, da_amount, da_gst, da_total,
            da_proof, remarks, from_location, to_location,
            from_date_time, to_date_time
        )
        VALUES (
            :da_sheet_id, :user_id, :from_date, :time_duration,
            :travel_from, :travel_to, :distance_from_station,
            :purpose, :da_amount, :da_gst, :da_total,
            :da_proof, :remarks, :from_location, :to_location,
            :from_date_time, :to_date_time
        )
        RETURNING da_sheet_detail_id
    """)

    result = db.execute(sql, {
        "da_sheet_id": data.da_sheet_id,
        "user_id": data.user_id,
        "from_date": data.from_date,
        "time_duration": data.time_duration,
        "travel_from": data.travel_from,
        "travel_to": data.travel_to,
        "distance_from_station": data.distance_from_station,
        "purpose": data.purpose,
        "da_amount": data.da_amount,
        "da_gst": data.da_gst,
        "da_total": data.da_total,
        "da_proof": da_proof,
        "remarks": data.remarks,
        "from_location": data.from_location,
        "to_location": data.to_location,
        "from_date_time": data.from_date_time,
        "to_date_time": data.to_date_time,
    })

    db.commit()
    return result.scalar()
@router.post("/allowanceDetails")
async def create_da(
    # ---------- FORM FIELDS ----------
    da_sheet_id: int = Form(...),
    user_id: int = Form(...),
    from_date: str = Form(...),
    time_duration: Optional[str] = Form(None),
    travel_from: Optional[str] = Form(None),
    travel_to: Optional[str] = Form(None),
    distance_from_station: Optional[float] = Form(None),
    purpose: Optional[str] = Form(None),
    da_amount: Optional[float] = Form(None),
    da_gst: Optional[float] = Form(None),
    da_total: Optional[float] = Form(None),
    remarks: Optional[str] = Form(None),
    from_location: Optional[str] = Form(None),
    to_location: Optional[str] = Form(None),
    from_date_time: Optional[str] = Form(None),
    to_date_time: Optional[str] = Form(None),

    # ---------- FILES ----------
    files: Optional[List[UploadFile]] = File(None),

    db: Session = Depends(get_db),
):
    """
    Handles:
    - no file
    - single file
    - multiple files
    """

    # ---------- NORMALIZE FILE INPUT ----------
    if files is None:
        files = []
    elif isinstance(files, UploadFile):
        files = [files]

    # ---------- BUILD PAYLOAD ----------
    payload = DailyAllowanceDetailCreate(
        da_sheet_id=da_sheet_id,
        user_id=user_id,
        from_date=from_date,
        time_duration=time_duration,
        travel_from=travel_from,
        travel_to=travel_to,
        distance_from_station=distance_from_station,
        purpose=purpose,
        da_amount=da_amount,
        da_gst=da_gst,
        da_total=da_total,
        remarks=remarks,
        from_location=from_location,
        to_location=to_location,
        from_date_time=from_date_time,
        to_date_time=to_date_time,
    )

    # ---------- CALL CRUD ----------
    try:
        return create_da_detail_sql(db, payload, files)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
@router.delete("/allowanceDetails{detail_id}")
def delete_da(detail_id: int, db: Session = Depends(get_db)):
    deleted = delete_da_detail_sql(db, detail_id)
    return {"deleted": deleted}
