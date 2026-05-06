import json
import os
import shutil
from typing import Literal, Optional
from click import File
from typing import Optional, Union
from fastapi import (
    APIRouter, Depends, UploadFile, File as FastAPIFile, Form, HTTPException
)
from fastapi import APIRouter, Depends, Form, HTTPException, HTTPException, Query, UploadFile
from sqlalchemy import text
from sqlalchemy.orm import Session
from app.crud.gate_pass.igGatePassCrud import   create_inward_gate_pass_crud, get_all_inward_gate_passes, get_cardData_crud,  get_gatepass_by_formtype, get_inward_gate_pass_by_id, update_inward_gate_pass_full
from app.database import get_db
from app.schemas.gate_pass.GatePass import AllGatePassListResponse,  InwardGatePassData, InwardGatePassUpdate
from app.utils.UserAuthUtils import verify_access_token  # check token
from sqlalchemy import text

router = APIRouter(prefix="/api/leave/type", tags=["Leave"])
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
@router.get("")
def get_leave_types(
    user_id: int,
    db: Session = Depends(get_db)
):
    # print("DEBUG: API called")
    # print("DEBUG: user_id =", user_id)

    # 1. Get user gender
    # print("DEBUG: Fetching user gender")

    user_result = db.execute(
        text("SELECT gender FROM users WHERE user_id = :user_id"),
        {"user_id": user_id}
    ).fetchone()

    # print("DEBUG: user_result =", user_result)

    if not user_result:
        # print("DEBUG: User not found")
        raise HTTPException(status_code=404, detail="User not found")

    gender = (user_result.gender or "").lower()
    # print("DEBUG: gender =", gender)

    # 2. Fetch leave types
    # print("DEBUG: Fetching leave types")

    leave_result = db.execute(text("SELECT * FROM get_leave_types();"))
    rows = [dict(row._mapping) for row in leave_result.fetchall()]

    # print("DEBUG: leave types before filter =", rows)

    # 3. Apply gender-based filtering
    # 3. Apply gender-based filtering
    if gender == "male":
        # print("DEBUG: Gender is male, removing id = 5")
        rows = [row for row in rows if row.get("id") != 5]

    elif gender == "female":
        # print("DEBUG: Gender is female, removing id = 6")
        rows = [row for row in rows if row.get("id") != 6]

    rows = [row for row in rows if row.get("id") != 2]
    # print("DEBUG: leave types after filter =", rows)

    return rows
