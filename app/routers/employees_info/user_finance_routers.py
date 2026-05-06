# app/routers/user_finance.py
from datetime import datetime
import os
import shutil
from typing import List, Union
from fastapi import APIRouter, BackgroundTasks, Depends, File, Form, HTTPException, UploadFile
from sqlalchemy import text
from sqlalchemy.orm import Session
from app.crud.employees_info.employee_notifications_crud import handle_employee_form_submission
from app.database import get_db
from app.crud.employees_info.user_finance_crud import (
    get_all_finance,
    get_finance_by_id,
    get_finance_by_user_id,
)
from app.models.UserModel import User
from app.schemas.employees_info.user_finance_schemas import UserFinanceResponse

router = APIRouter(prefix="/api/finance", tags=["User Finance"])
UPLOAD_DIR = "files/employee_family"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.get("/")
def route_get_all(db: Session = Depends(get_db)):
    return get_all_finance(db)


@router.get("/{finance_id}")
def route_get_by_id(finance_id: int, db: Session = Depends(get_db)):
    return get_finance_by_id(db, finance_id)


from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
import math

@router.get("/user/{user_id}")
def route_get_by_user(user_id: int, db: Session = Depends(get_db)):
    data = get_finance_by_user_id(db, user_id)
    return JSONResponse(
        content=jsonable_encoder(
            data,
            custom_encoder={float: lambda v: None if math.isnan(v) else v}
        )
    )


# @router.post("/crud")
# async def user_finance_crud(
#     user_finance_id: str = Form(None),
#     user_id: int = Form(...),
#     date: str = Form(None),
#     financial_year: str = Form(None),
#     opting_for_concessional_rate: str = Form(None),

#     residing_in_rented_house: str = Form(None),
#     monthly_rent: float = Form(None),
#     landlord_name: str = Form(None),
#     temporary_address: str = Form(None),

#     pension_plan: str = Form(None),
#     lic_premium: str = Form(None),
#     ppf: str = Form(None),
#     ulip: str = Form(None),
#     tuition_fees: str = Form(None),
#     nsc: str = Form(None),
#     nsc_interest: str = Form(None),
#     housing_loan_repayment: str = Form(None),
#     other_investments: str = Form(None),
#     infrastructure_bond: str = Form(None),
#     medical_insurance_80D: str = Form(None),
#     educational_loan_interest: str = Form(None),
#     contribution_to_nps: str = Form(None),
#     interest_housing_24b: float = Form(None),
#     declaration_text: str = Form(None),
#     signature_name: str = Form(None),
#     status:str = Form(None),

#     upload_document: List[UploadFile] = File(None),
#     signature_file: UploadFile = File(None),   # ⭐ ADDED SIGNATURE FILE

#     db: Session = Depends(get_db),
#     bg: BackgroundTasks = None
#     ):
#     # Convert date
#     if user_finance_id in (None, "", "null", "None"):
#       user_finance_id = None
#     else:
#         user_finance_id = int(user_finance_id)
#     date_value = None
#     if date:
#         date_value = datetime.strptime(date, "%Y-%m-%d").date()

#     # Save multiple documents
#     file_paths = []
#     if upload_document:
#         os.makedirs(UPLOAD_DIR, exist_ok=True)
#         for file in upload_document:
#             save_path = os.path.join(UPLOAD_DIR, file.filename)
#             with open(save_path, "wb") as f:
#                 shutil.copyfileobj(file.file, f)
#             file_paths.append(save_path)

#     stored_paths = ",".join(file_paths) if file_paths else None

#     # Save signature file
#     signature_path = None
#     if signature_file:
#         os.makedirs(UPLOAD_DIR, exist_ok=True)
#         signature_path = os.path.join(UPLOAD_DIR, signature_file.filename)
#         with open(signature_path, "wb") as f:
#             shutil.copyfileobj(signature_file.file, f)

#     # Payload
#     payload = {
#         "user_id": user_id,
#         "date": date_value,
#         "financial_year": financial_year,
#         "opting_for_concessional_rate": opting_for_concessional_rate,
#         "residing_in_rented_house": residing_in_rented_house,
#         "monthly_rent": monthly_rent,
#         "landlord_name": landlord_name,
#         "temporary_address": temporary_address,
#         "medical_insurance_80d":medical_insurance_80D,
#         "interest_housing_24b": interest_housing_24b,
#         "pension_plan": pension_plan,
#         "lic_premium": lic_premium,
#         "ppf": ppf,
#         "ulip": ulip,
#         "tuition_fees": tuition_fees,
#         "nsc": nsc,
#         "status":status,
#         "nsc_interest": nsc_interest,
#         "housing_loan_repayment": housing_loan_repayment,
#         "other_investments": other_investments,
#         "infrastructure_bond": infrastructure_bond,
#         "educational_loan_interest": educational_loan_interest,
#         "contribution_to_nps": contribution_to_nps,
#         "declaration_text": declaration_text,
#     }

#     if stored_paths:
#         payload["upload_document"] = stored_paths

#     if signature_path:
#         payload["signature_name"] = signature_path   # ⭐ SAVED IN DB

#     payload_clean = {k: v for k, v in payload.items() if v is not None}

#     # INSERT
#     if user_finance_id is None:
#         sql = text(f"""
#             INSERT INTO user_finance ({", ".join(payload_clean.keys())})
#             VALUES ({", ".join([f":{k}" for k in payload_clean.keys()])})
#             RETURNING *;
#         """)
#         row = db.execute(sql, payload_clean).fetchone()
#         db.commit()
#         record = dict(row._mapping)

#     # --- NOTIFICATION TRIGGER ---
#         user = db.query(User).filter(User.user_id == user_id).first()

#         if user:
#             await handle_employee_form_submission(
#                 db=db,
#                 employee_username=user.username,
#                 form_name="Investment Declaration",
#                 status=status,
#                 bg=bg
#             )

#         return record

#     # UPDATE
#     payload_clean["user_finance_id"] = user_finance_id

#     sql = text(f"""
#         UPDATE user_finance
#         SET {", ".join([f"{k} = :{k}" for k in payload_clean if k != "user_finance_id"])}
#         WHERE user_finance_id = :user_finance_id
#         RETURNING *;
#     """)

#     row = db.execute(sql, payload_clean).fetchone()
#     db.commit()

#     if not row:
#         raise HTTPException(404, "Finance record not found")
#     record = dict(row._mapping)

# # --- NOTIFICATION TRIGGER ---
#     user = db.query(User).filter(User.user_id == user_id).first()

#     if user:
#         await handle_employee_form_submission(
#             db=db,
#             employee_username=user.username,
#             form_name="Investment Declaration",
#             status=status,
#             bg=bg
#         )

#     return record

@router.post("/crud")
async def user_finance_crud(
    user_finance_id: str = Form(None),
    user_id: int = Form(...),
    date: str = Form(None),
    financial_year: str = Form(None),
    opting_for_concessional_rate: str = Form(None),

    residing_in_rented_house: str = Form(None),
    monthly_rent: float = Form(None),
    landlord_name: str = Form(None),
    temporary_address: str = Form(None),

    pension_plan: str = Form(None),
    lic_premium: str = Form(None),
    ppf: str = Form(None),
    ulip: str = Form(None),
    tuition_fees: str = Form(None),
    nsc: str = Form(None),
    nsc_interest: str = Form(None),
    housing_loan_repayment: str = Form(None),
    other_investments: str = Form(None),
    infrastructure_bond: str = Form(None),
    medical_insurance_80D: str = Form(None),
    educational_loan_interest: str = Form(None),
    contribution_to_nps: str = Form(None),
    interest_housing_24b: float = Form(None),
    declaration_text: str = Form(None),
    signature_name: str = Form(None),
    status:str = Form(None),

    upload_document: List[UploadFile] = File(None),
    signature_file: UploadFile = File(None),

    db: Session = Depends(get_db),
    bg: BackgroundTasks = None
):
    # ── Helper to safely return JSON ──────────────────────────────────────
    def safe_json(data):
        return JSONResponse(
            content=jsonable_encoder(
                data,
                custom_encoder={float: lambda v: None if math.isnan(v) else v}
            )
        )

    # Convert date
    if user_finance_id in (None, "", "null", "None"):
        user_finance_id = None
    else:
        user_finance_id = int(user_finance_id)

    date_value = None
    if date:
        date_value = datetime.strptime(date, "%Y-%m-%d").date()

    # Save multiple documents
    file_paths = []
    if upload_document:
        os.makedirs(UPLOAD_DIR, exist_ok=True)
        for file in upload_document:
            save_path = os.path.join(UPLOAD_DIR, file.filename)
            with open(save_path, "wb") as f:
                shutil.copyfileobj(file.file, f)
            file_paths.append(save_path)

    stored_paths = ",".join(file_paths) if file_paths else None

    # Save signature file
    signature_path = None
    if signature_file:
        os.makedirs(UPLOAD_DIR, exist_ok=True)
        signature_path = os.path.join(UPLOAD_DIR, signature_file.filename)
        with open(signature_path, "wb") as f:
            shutil.copyfileobj(signature_file.file, f)

    # Payload
    payload = {
        "user_id": user_id,
        "date": date_value,
        "financial_year": financial_year,
        "opting_for_concessional_rate": opting_for_concessional_rate,
        "residing_in_rented_house": residing_in_rented_house,
        "monthly_rent": monthly_rent,
        "landlord_name": landlord_name,
        "temporary_address": temporary_address,
        "medical_insurance_80d": medical_insurance_80D,
        "interest_housing_24b": interest_housing_24b,
        "pension_plan": pension_plan,
        "lic_premium": lic_premium,
        "ppf": ppf,
        "ulip": ulip,
        "tuition_fees": tuition_fees,
        "nsc": nsc,
        "status": status,
        "nsc_interest": nsc_interest,
        "housing_loan_repayment": housing_loan_repayment,
        "other_investments": other_investments,
        "infrastructure_bond": infrastructure_bond,
        "educational_loan_interest": educational_loan_interest,
        "contribution_to_nps": contribution_to_nps,
        "declaration_text": declaration_text,
    }

    if stored_paths:
        payload["upload_document"] = stored_paths

    if signature_path:
        payload["signature_name"] = signature_path

    payload_clean = {k: v for k, v in payload.items() if v is not None}

    # INSERT
    if user_finance_id is None:
        sql = text(f"""
            INSERT INTO user_finance ({", ".join(payload_clean.keys())})
            VALUES ({", ".join([f":{k}" for k in payload_clean.keys()])})
            RETURNING *;
        """)
        row = db.execute(sql, payload_clean).fetchone()
        db.commit()
        record = dict(row._mapping)

        # --- NOTIFICATION TRIGGER ---
        user = db.query(User).filter(User.user_id == user_id).first()
        if user:
            await handle_employee_form_submission(
                db=db,
                employee_username=user.username,
                form_name="Investment Declaration",
                status=status,
                bg=bg,
                reference_id=str(user_id),
                redirect_url=f"/profile/profile-info/{str(user_id)}/review",
            )

        return safe_json(record)  # ✅ fixed

    # UPDATE
    payload_clean["user_finance_id"] = user_finance_id

    sql = text(f"""
        UPDATE user_finance
        SET {", ".join([f"{k} = :{k}" for k in payload_clean if k != "user_finance_id"])}
        WHERE user_finance_id = :user_finance_id
        RETURNING *;
    """)

    row = db.execute(sql, payload_clean).fetchone()
    db.commit()

    if not row:
        raise HTTPException(404, "Finance record not found")

    record = dict(row._mapping)

    # --- NOTIFICATION TRIGGER ---
    user = db.query(User).filter(User.user_id == user_id).first()
    if user:
        await handle_employee_form_submission(
            db=db,
            employee_username=user.username,
            form_name="Investment Declaration",
            status=status,
            bg=bg,
            reference_id=str(user_id),
            redirect_url=f"/profile/profile-info/{str(user_id)}/review",
        )

    return safe_json(record)  # ✅ fixed

