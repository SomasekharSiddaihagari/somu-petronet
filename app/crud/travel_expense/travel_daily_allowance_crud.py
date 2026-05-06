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
 
# ------------------- File Upload -------------------
UPLOAD_ROOT = "files/daily_allowance"
os.makedirs(UPLOAD_ROOT, exist_ok=True)

def create_sheet(db: Session, data: DailyAllowanceSheetCreate):

    payload = data.dict()

    columns = ", ".join(payload.keys())
    values = ", ".join([f":{k}" for k in payload.keys()])

    sql = text(f"""
        INSERT INTO daily_allowance_sheet ({columns})
        VALUES ({values})
        RETURNING da_sheet_id;
    """)

    result = db.execute(sql, payload)
    db.commit()

    sheet_id = result.scalar()
    return get_sheet_by_id(db, sheet_id)

def update_sheet(db: Session, sheet_id: int, data: DailyAllowanceSheetUpdate):
    payload = data.dict(exclude_unset=True)

    if not payload:
        return get_sheet_by_id(db, sheet_id)

    payload["da_sheet_id"] = sheet_id

    set_clause = ", ".join([f"{k} = :{k}" for k in payload.keys() if k != "da_sheet_id"])

    sql = text(f"""
        UPDATE daily_allowance_sheet
        SET {set_clause}
        WHERE da_sheet_id = :da_sheet_id
    """)

    result = db.execute(sql, payload)
    db.commit()

    if result.rowcount == 0:
        return None

    return get_sheet_by_id(db, sheet_id)

def get_sheet_by_id(db: Session, sheet_id: int):

    sql = text("""
        SELECT *
        FROM daily_allowance_sheet
        WHERE da_sheet_id = :sheet_id;
    """)

    row = db.execute(sql, {"sheet_id": sheet_id}).mappings().first()

    if not row:
        return None

    return dict(row)


import os
from sqlalchemy import text

def delete_da_detail_sql(db, detail_id):
    record = get_da_detail_by_id_sql(db, detail_id)
    if not record:
        return False

    # Delete physical files
    if record["da_proof"]:
        for path in record["da_proof"].split(","):
            if os.path.exists(path):
                os.remove(path)

    sql = text("DELETE FROM daily_allowance_sheet_detail WHERE da_sheet_detail_id = :detail_id")
    db.execute(sql, {"detail_id": detail_id})
    db.commit()

    return True
def get_da_detail_by_id_sql(db, detail_id):
    sql = text("SELECT * FROM daily_allowance_sheet_detail WHERE da_sheet_detail_id = :id")
    result = db.execute(sql, {"id": detail_id}).mappings().first()
    return dict(result) if result else None
