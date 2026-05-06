import os
import shutil
from uuid import uuid4
from sqlalchemy.orm import Session
from sqlalchemy import text

from app.models.travel_expense.travel_expense_sheet import TravelExpenseSheet

UPLOAD_ROOT = "files/travel_expense_details"
os.makedirs(UPLOAD_ROOT, exist_ok=True)



def save_files(files_list):
    if not files_list:
        return None

    os.makedirs(UPLOAD_ROOT, exist_ok=True)

    saved_paths = []

    for file in files_list:
        ext = file.filename.split('.')[-1]
        new_name = f"{uuid4()}.{ext}"
        full_path = os.path.join(UPLOAD_ROOT, new_name)

        with open(full_path, "wb") as f:
            f.write(file.file.read())

        saved_paths.append(full_path)

    return ",".join(saved_paths)


def insert_to_history(db: Session, data: dict):
    sql = """
        INSERT INTO travel_expense_sheet_detail_history (
            tesd_id,
            expense_sheet_id,
            from_date, to_date,
            travel_route,
            from_location, to_location,

            air_rail_bus_amount, air_rail_bus_gst, air_rail_bus_total,
            hotel_amount, hotel_gst, hotel_total,
            daily_allowance_amount, daily_allowance_gst, daily_allowance_total,
            local_conveyance_amount, local_conveyance_gst, local_conveyance_total,
            other_amount, other_gst, other_total,

            remarks,
            user_id,
            is_overseas,

            air_rail_bus_proof, hotel_proof, daily_allowance_proof,
            local_conveyance_proof, other_proof
        )
        VALUES (
            :tesd_id,
            :expense_sheet_id,
            :from_date, :to_date,
            :travel_route,
            :from_location, :to_location,

            :air_rail_bus_amount, :air_rail_bus_gst, :air_rail_bus_total,
            :hotel_amount, :hotel_gst, :hotel_total,
            :daily_allowance_amount, :daily_allowance_gst, :daily_allowance_total,
            :local_conveyance_amount, :local_conveyance_gst, :local_conveyance_total,
            :other_amount, :other_gst, :other_total,

            :remarks,
            :user_id,
            :is_overseas,

            :air_rail_bus_proof, :hotel_proof, :daily_allowance_proof,
            :local_conveyance_proof, :other_proof
        )
    """

    db.execute(text(sql), data)

def create_expense_detail(db: Session, payload: dict, upload_files: dict):
    for key, files in upload_files.items():
        if files:
            payload[key] = list_to_text(save_files(files, key))
        else:
            payload[key] = None


    sql = """
        INSERT INTO travel_expense_sheet_detail (
            expense_sheet_id,
            from_date, to_date,
            travel_route,
            from_location, to_location,

            air_rail_bus_amount, air_rail_bus_gst, air_rail_bus_total,
            hotel_amount, hotel_gst, hotel_total,
            daily_allowance_amount, daily_allowance_gst, daily_allowance_total,
            local_conveyance_amount, local_conveyance_gst, local_conveyance_total,
            other_amount, other_gst, other_total,

            remarks,
            user_id,
            is_overseas,

            air_rail_bus_proof, hotel_proof, daily_allowance_proof,
            local_conveyance_proof, other_proof
        )
        VALUES (
            :expense_sheet_id,
            :from_date, :to_date,
            :travel_route,
            :from_location, :to_location,

            :air_rail_bus_amount, :air_rail_bus_gst, :air_rail_bus_total,
            :hotel_amount, :hotel_gst, :hotel_total,
            :daily_allowance_amount, :daily_allowance_gst, :daily_allowance_total,
            :local_conveyance_amount, :local_conveyance_gst, :local_conveyance_total,
            :other_amount, :other_gst, :other_total,

            :remarks,
            :user_id,
            :is_overseas,

            :air_rail_bus_proof, :hotel_proof, :daily_allowance_proof,
            :local_conveyance_proof, :other_proof
        )
        RETURNING tesd_id
    """

    result = db.execute(text(sql), payload).fetchone()
    tesd_id = result[0]

    payload["tesd_id"] = tesd_id
    insert_to_history(db, payload)

    db.commit()
    return {"tesd_id": tesd_id, "message": "Expense detail added successfully"}
from datetime import datetime, date

def to_date(value: str | None) -> date | None:
    if value in (None, "", "null"):
        return None
    return datetime.strptime(value, "%Y-%m-%d").date()

from typing import Optional, List
from fastapi import HTTPException, UploadFile
from sqlalchemy.orm import Session
from sqlalchemy import text


def to_float(value):
    if value in (None, "", "null"):
        return None
    return float(value)

from sqlalchemy import text
from fastapi import HTTPException
from sqlalchemy.orm import Session
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
def update_expense_detail(
    db: Session,
    tesd_id: int,
    payload: dict,
    upload_files: dict
):
    # 1. Check if record exists
    check_sql = text("""
        SELECT 1
        FROM travel_expense_sheet_detail
        WHERE tesd_id = :tesd_id
    """)
 
    exists = db.execute(check_sql, {"tesd_id": tesd_id}).fetchone()
    if not exists:
        raise HTTPException(status_code=404, detail="Expense detail not found")
 
    # 2. Build UPDATE fields (DO NOT SKIP VALID VALUES)
    update_fields = {}
    for key, value in payload.items():
        if value is not None:
            update_fields[key] = value
 
    # 3. Handle file fields (replace or remove)
    for field, files in upload_files.items():
        if files is not None:
            if len(files) == 0:
                # Remove file
                update_fields[field] = None
            else:
                fetch_existing_sql = text(f"""
                    SELECT {field}
                    FROM travel_expense_sheet_detail
                    WHERE tesd_id = :tesd_id
                """)
 
                existing_value = db.execute(
                    fetch_existing_sql,
                    {"tesd_id": tesd_id}
                ).scalar()
 
                existing_files = text_to_list(existing_value)
                new_paths = save_files(files, field)
                update_fields[field] = list_to_text(existing_files + new_paths)
 
    # 4. Run UPDATE
    if update_fields:
        set_clause = ", ".join([f"{k} = :{k}" for k in update_fields.keys()])
        update_fields["tesd_id"] = tesd_id
 
        update_sql = text(f"""
            UPDATE travel_expense_sheet_detail
            SET {set_clause}
            WHERE tesd_id = :tesd_id
        """)
 
        db.execute(update_sql, update_fields)
        db.commit()
 
    # 5. Return updated row
    fetch_sql = text("""
        SELECT *
        FROM travel_expense_sheet_detail
        WHERE tesd_id = :tesd_id
    """)
 
    return db.execute(fetch_sql, {"tesd_id": tesd_id}).mappings().first()
def text_to_list(value: str | None) -> list[str]:
    if not value:
        return []
    return [v for v in value.split(",") if v]


def list_to_text(values: list[str]) -> str | None:
    if not values:
        return None
    return ",".join(values)


def save_files(files: list[UploadFile], folder: str) -> list[str]:
    paths = []
    target_dir = os.path.join(UPLOAD_ROOT, folder)
    os.makedirs(target_dir, exist_ok=True)

    for file in files:
        ext = os.path.splitext(file.filename)[1]
        filename = f"{uuid4()}{ext}"
        full_path = os.path.join(target_dir, filename)

        with open(full_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        paths.append(full_path)

    return paths

def process_uploads(upload_files: dict):
    result = {}
    for key, files in upload_files.items():
        if files and isinstance(files, list) and isinstance(files[0], UploadFile):
            result[key] = save_files(files)
        else:
            result[key] = None
    return result

def delete_expense_detail(db: Session, tesd_id: int):
    sql = "DELETE FROM travel_expense_sheet_detail WHERE tesd_id = :tesd_id"
    db.execute(text(sql), {"tesd_id": tesd_id})
    db.commit()
    return {"message": "Expense detail deleted successfully"}
