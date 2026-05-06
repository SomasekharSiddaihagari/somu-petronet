# app/routers/form12c.py
from datetime import date, datetime
import json
import os
import shutil
from typing import List, Union
from fastapi import APIRouter, BackgroundTasks, Depends, File, Form, HTTPException, UploadFile
from sqlalchemy import text
from sqlalchemy.orm import Session
from app.crud.employees_info.employee_notifications_crud import handle_employee_form_submission
from app.database import get_db
from app.crud.employees_info.employee_form_12c_crud import (
    get_all_form12c,
    get_form12c_by_id,
    get_form12c_by_user_id,
    get_user_basic_info,
)
from app.models.UserModel import User
from app.routers.UserAuthR2 import make_download_url
from app.schemas.employees_info.employee_form_12c_schemas import Form12CResponse

router = APIRouter(prefix="/api/form12c", tags=["Form 12C"])
UPLOAD_DIR = "files/employee_form12"
os.makedirs(UPLOAD_DIR, exist_ok=True)
def serialize_form12c(row, user=None):
    if not row:
        return None

    def fix_file(path):
        return make_download_url(path) if path else None

    # ---------------- EMPLOYEE DETAILS ----------------
    if user:
        employee_code = user.get("employee_code")
        first = user.get("first_name")
        last = user.get("last_name")
        employee_full_name = f"{first} {last}".strip() if first or last else None
    else:
        employee_code = None
        employee_full_name = None

    # ---------------------------------------------------

    return {
        **row,  # keep all original form12c fields returned from DB

        # NEW FIELDS
        "employee_code": employee_code,
        "employee_full_name": employee_full_name,
        "submission_type": "Form 12",

        "status": row.get("status"),  # included from your table

        # File conversions
        "upload_document": fix_file(row.get("upload_document")),
        "signature": fix_file(row.get("signature")),
    }



@router.get("/")
def route_get_all(db: Session = Depends(get_db)):
    rows = get_all_form12c(db)
    result = []

    for r in rows:
        user = get_user_basic_info(db, r.get("user_id"))
        result.append(serialize_form12c(r, user))

    return result

@router.get("/{form_id}")
def route_get_by_id(form_id: int, db: Session = Depends(get_db)):
    row = get_form12c_by_id(db, form_id)
    if not row:
        return None

    user = get_user_basic_info(db, row.get("user_id"))
    return serialize_form12c(row, user)

@router.get("/user/{user_id}")
def route_get_by_user(user_id: int, db: Session = Depends(get_db)):
    rows = get_form12c_by_user_id(db, user_id)
    user = get_user_basic_info(db, user_id)
    return [serialize_form12c(r, user) for r in rows]


# @router.post("/crud")
# def employee_form_12c_crud(
#     form_id: str = Form(None),
#     user_id: str = Form(None),

#     self_alv: str = Form(None),
#     lo1_alv: str = Form(None),
#     lo2_alv: str = Form(None),

#     self_municipal_tax: str = Form(None),
#     lo1_municipal_tax: str = Form(None),
#     lo2_municipal_tax: str = Form(None),

#     self_annual_value: str = Form(None),
#     lo1_annual_value: str = Form(None),
#     lo2_annual_value: str = Form(None),

#     self_less_30: str = Form(None),
#     lo1_less_30: str = Form(None),
#     lo2_less_30: str = Form(None),

#     house_type_self: str = Form(None),
#     house_type_lo1: str = Form(None),
#     house_type_lo2: str = Form(None),

#     self_interest: str = Form(None),
#     lo1_interest: str = Form(None),
#     lo2_interest: str = Form(None),

#     self_loan_date: str = Form(None),
#     lo1_loan_date: str = Form(None),
#     lo2_loan_date: str = Form(None),

#     self_one_fifth_interest: str = Form(None),
#     lo1_one_fifth_interest: str = Form(None),
#     lo2_one_fifth_interest: str = Form(None),

#     self_net_income: str = Form(None),
#     lo1_net_income: str = Form(None),
#     lo2_net_income: str = Form(None),

#     self_tds_self_lease: str = Form(None),
#     lo1_tds_self_lease: str = Form(None),
#     lo2_tds_self_lease: str = Form(None),
#     status:str = Form(None),

#     self_cess_self_lease: str = Form(None),
#     lo1_cess_self_lease: str = Form(None),
#     lo2_cess_self_lease: str = Form(None),

#     self_capital_gains: str = Form(None),
#     lo1_capital_gains: str = Form(None),
#     lo2_capital_gains: str = Form(None),

#     self_other_sources: str = Form(None),
#     lo1_other_sources: str = Form(None),
#     lo2_other_sources: str = Form(None),

#     self_aggregate_items: str = Form(None),
#     lo1_aggregate_items: str = Form(None),
#     lo2_aggregate_items: str = Form(None),

#     self_tds_other_income: str = Form(None),
#     lo1_tds_other_income: str = Form(None),
#     lo2_tds_other_income: str = Form(None),

#     self_cess_other_income: str = Form(None),
#     lo1_cess_other_income: str = Form(None),
#     lo2_cess_other_income: str = Form(None),

#     self_total_tds: str = Form(None),
#     lo1_total_tds: str = Form(None),
#     lo2_total_tds: str = Form(None),

#     self_total_cess: str = Form(None),
#     lo1_total_cess: str = Form(None),
#     lo2_total_cess: str = Form(None),

#     declared_place: str = Form(None),
#     declared_date: str = Form(None),
#     signature_name: str = Form(None),
#     financial_year: str = Form(None),

#     upload_document: List[UploadFile] = File(None),
#     signature_file: UploadFile = File(None),

#     db: Session = Depends(get_db)
# ):
#     # --------------------------------------------------
#     # Convert ID fields
#     # --------------------------------------------------
#     if form_id in (None, "", "null", "None"):
#         form_id = None
#     else:
#         form_id = int(form_id)

#     if user_id in (None, "", "null", "None"):
#         user_id = None
#     else:
#         user_id = int(user_id)

#     # --------------------------------------------------
#     # Convert Dates
#     # --------------------------------------------------
#     def parse_date(val):
#         if val in (None, "", "null", "None"):
#             return None
#         return datetime.strptime(val, "%Y-%m-%d").date()

#     declared_date_value = parse_date(declared_date)
#     self_loan_date_val = parse_date(self_loan_date)
#     lo1_loan_date_val = parse_date(lo1_loan_date)
#     lo2_loan_date_val = parse_date(lo2_loan_date)

#     # --------------------------------------------------
#     # Save Multiple Files
#     # --------------------------------------------------
#     file_paths = []
#     if upload_document:
#         os.makedirs(UPLOAD_DIR, exist_ok=True)
#         for file in upload_document:
#             save_path = os.path.join(UPLOAD_DIR, file.filename)
#             with open(save_path, "wb") as f:
#                 shutil.copyfileobj(file.file, f)
#             file_paths.append(save_path)

#     stored_files = ",".join(file_paths) if file_paths else None

#     # --------------------------------------------------
#     # Save Signature File (Single)
#     # --------------------------------------------------
#     signature_path = None
#     if signature_file:
#         os.makedirs(UPLOAD_DIR, exist_ok=True)
#         signature_path = os.path.join(UPLOAD_DIR, signature_file.filename)
#         with open(signature_path, "wb") as f:
#             shutil.copyfileobj(signature_file.file, f)

#     # --------------------------------------------------
#     # Build Payload
#     # --------------------------------------------------
#     payload = {
#         "user_id": user_id,

#         "self_alv": self_alv,
#         "lo1_alv": lo1_alv,
#         "lo2_alv": lo2_alv,
# "financial_year":financial_year,
#         "self_municipal_tax": self_municipal_tax,
#         "lo1_municipal_tax": lo1_municipal_tax,
#         "lo2_municipal_tax": lo2_municipal_tax,

#         "self_annual_value": self_annual_value,
#         "lo1_annual_value": lo1_annual_value,
#         "lo2_annual_value": lo2_annual_value,

#         "self_less_30": self_less_30,
#         "lo1_less_30": lo1_less_30,
#         "lo2_less_30": lo2_less_30,

#         "house_type_self": house_type_self,
#         "house_type_lo1": house_type_lo1,
#         "house_type_lo2": house_type_lo2,
# "status":status,
#         "self_interest": self_interest,
#         "lo1_interest": lo1_interest,
#         "lo2_interest": lo2_interest,

#         "self_loan_date": self_loan_date_val,
#         "lo1_loan_date": lo1_loan_date_val,
#         "lo2_loan_date": lo2_loan_date_val,

#         "self_one_fifth_interest": self_one_fifth_interest,
#         "lo1_one_fifth_interest": lo1_one_fifth_interest,
#         "lo2_one_fifth_interest": lo2_one_fifth_interest,

#         "self_net_income": self_net_income,
#         "lo1_net_income": lo1_net_income,
#         "lo2_net_income": lo2_net_income,

#         "self_tds_self_lease": self_tds_self_lease,
#         "lo1_tds_self_lease": lo1_tds_self_lease,
#         "lo2_tds_self_lease": lo2_tds_self_lease,

#         "self_cess_self_lease": self_cess_self_lease,
#         "lo1_cess_self_lease": lo1_cess_self_lease,
#         "lo2_cess_self_lease": lo2_cess_self_lease,

#         "self_capital_gains": self_capital_gains,
#         "lo1_capital_gains": lo1_capital_gains,
#         "lo2_capital_gains": lo2_capital_gains,

#         "self_other_sources": self_other_sources,
#         "lo1_other_sources": lo1_other_sources,
#         "lo2_other_sources": lo2_other_sources,

#         "self_aggregate_items": self_aggregate_items,
#         "lo1_aggregate_items": lo1_aggregate_items,
#         "lo2_aggregate_items": lo2_aggregate_items,

#         "self_tds_other_income": self_tds_other_income,
#         "lo1_tds_other_income": lo1_tds_other_income,
#         "lo2_tds_other_income": lo2_tds_other_income,

#         "self_cess_other_income": self_cess_other_income,
#         "lo1_cess_other_income": lo1_cess_other_income,
#         "lo2_cess_other_income": lo2_cess_other_income,

#         "self_total_tds": self_total_tds,
#         "lo1_total_tds": lo1_total_tds,
#         "lo2_total_tds": lo2_total_tds,

#         "self_total_cess": self_total_cess,
#         "lo1_total_cess": lo1_total_cess,
#         "lo2_total_cess": lo2_total_cess,

#         "declared_place": declared_place,
#         "declared_date": declared_date_value,
#         "signature_name": signature_name,
#     }

#     if stored_files:
#         payload["upload_document"] = stored_files

#     if signature_path:
#         payload["signature"] = signature_path

#     payload_clean = {k: v for k, v in payload.items()}

#     # --------------------------------------------------
#     # INSERT
#     # --------------------------------------------------
#     if form_id is None:
#         sql = text(f"""
#             INSERT INTO employee_form_12c ({", ".join(payload_clean.keys())})
#             VALUES ({", ".join([f":{k}" for k in payload_clean.keys()])})
#             RETURNING *;
#         """)
#         row = db.execute(sql, payload_clean).fetchone()
#         db.commit()
#         return dict(row._mapping)

#     # --------------------------------------------------
#     # UPDATE
#     # --------------------------------------------------
#     payload_clean["form_id"] = form_id

#     sql = text(f"""
#         UPDATE employee_form_12c
#         SET {", ".join([f"{k} = :{k}" for k in payload_clean if k != "form_id"])}
#         WHERE form_id = :form_id
#         RETURNING *;
#     """)

#     row = db.execute(sql, payload_clean).fetchone()
#     db.commit()

#     if not row:
#         raise HTTPException(status_code=404, detail="Form 12C record not found")

#     return dict(row._mapping)


@router.post("/crud")
async def employee_form_12c_crud(
    form_id: str = Form(None),
    user_id: str = Form(None),

    self_alv: str = Form(None),
    lo1_alv: str = Form(None),
    lo2_alv: str = Form(None),

    self_municipal_tax: str = Form(None),
    lo1_municipal_tax: str = Form(None),
    lo2_municipal_tax: str = Form(None),

    self_annual_value: str = Form(None),
    lo1_annual_value: str = Form(None),
    lo2_annual_value: str = Form(None),

    self_less_30: str = Form(None),
    lo1_less_30: str = Form(None),
    lo2_less_30: str = Form(None),

    house_type_self: str = Form(None),
    house_type_lo1: str = Form(None),
    house_type_lo2: str = Form(None),

    self_interest: str = Form(None),
    lo1_interest: str = Form(None),
    lo2_interest: str = Form(None),

    self_loan_date: str = Form(None),
    lo1_loan_date: str = Form(None),
    lo2_loan_date: str = Form(None),

    self_one_fifth_interest: str = Form(None),
    lo1_one_fifth_interest: str = Form(None),
    lo2_one_fifth_interest: str = Form(None),

    self_net_income: str = Form(None),
    lo1_net_income: str = Form(None),
    lo2_net_income: str = Form(None),

    self_tds_self_lease: str = Form(None),
    lo1_tds_self_lease: str = Form(None),
    lo2_tds_self_lease: str = Form(None),
    status:str = Form(None),

    self_cess_self_lease: str = Form(None),
    lo1_cess_self_lease: str = Form(None),
    lo2_cess_self_lease: str = Form(None),


    self_cess_self_business: str = Form(None),   # ← ADDED
    lo1_cess_self_business: str = Form(None),    # ← ADDED
    lo2_cess_self_business: str = Form(None),    # ← ADDED


    self_capital_gains: str = Form(None),
    lo1_capital_gains: str = Form(None),
    lo2_capital_gains: str = Form(None),

    self_other_sources: str = Form(None),
    lo1_other_sources: str = Form(None),
    lo2_other_sources: str = Form(None),

    self_aggregate_items: str = Form(None),
    lo1_aggregate_items: str = Form(None),
    lo2_aggregate_items: str = Form(None),

    self_tds_other_income: str = Form(None),
    lo1_tds_other_income: str = Form(None),
    lo2_tds_other_income: str = Form(None),

    self_cess_other_income: str = Form(None),
    lo1_cess_other_income: str = Form(None),
    lo2_cess_other_income: str = Form(None),

    self_total_tds: str = Form(None),
    lo1_total_tds: str = Form(None),
    lo2_total_tds: str = Form(None),

    self_total_cess: str = Form(None),
    lo1_total_cess: str = Form(None),
    lo2_total_cess: str = Form(None),

    declared_place: str = Form(None),
    declared_date: str = Form(None),
    signature_name: str = Form(None),
    financial_year: str = Form(None),

    upload_document: List[UploadFile] = File(None),
    signature_file: UploadFile = File(None),

    db: Session = Depends(get_db),
    bg: BackgroundTasks = None
):
    # --------------------------------------------------
    # Convert ID fields
    # --------------------------------------------------
    if form_id in (None, "", "null", "None"):
        form_id = None
    else:
        form_id = int(form_id)

    if user_id in (None, "", "null", "None"):
        user_id = None
    else:
        user_id = int(user_id)

    # --------------------------------------------------
    # Convert Dates
    # --------------------------------------------------
    def parse_date(val):
        if val in (None, "", "null", "None"):
            return None
        return datetime.strptime(val, "%Y-%m-%d").date()

    declared_date_value = parse_date(declared_date)
    self_loan_date_val = parse_date(self_loan_date)
    lo1_loan_date_val = parse_date(lo1_loan_date)
    lo2_loan_date_val = parse_date(lo2_loan_date)

    # --------------------------------------------------
    # Save Multiple Files
    # --------------------------------------------------
    file_paths = []
    if upload_document:
        os.makedirs(UPLOAD_DIR, exist_ok=True)
        for file in upload_document:
            save_path = os.path.join(UPLOAD_DIR, file.filename)
            with open(save_path, "wb") as f:
                shutil.copyfileobj(file.file, f)
            file_paths.append(save_path)

    stored_files = ",".join(file_paths) if file_paths else None

    # --------------------------------------------------
    # Save Signature File (Single)
    # --------------------------------------------------
    signature_path = None
    if signature_file:
        os.makedirs(UPLOAD_DIR, exist_ok=True)
        signature_path = os.path.join(UPLOAD_DIR, signature_file.filename)
        with open(signature_path, "wb") as f:
            shutil.copyfileobj(signature_file.file, f)

    # --------------------------------------------------
    # Build Payload
    # --------------------------------------------------
    payload = {
        "user_id": user_id,

        "self_alv": self_alv,
        "lo1_alv": lo1_alv,
        "lo2_alv": lo2_alv,
"financial_year":financial_year,
        "self_municipal_tax": self_municipal_tax,
        "lo1_municipal_tax": lo1_municipal_tax,
        "lo2_municipal_tax": lo2_municipal_tax,

        "self_annual_value": self_annual_value,
        "lo1_annual_value": lo1_annual_value,
        "lo2_annual_value": lo2_annual_value,

        "self_less_30": self_less_30,
        "lo1_less_30": lo1_less_30,
        "lo2_less_30": lo2_less_30,

        "house_type_self": house_type_self,
        "house_type_lo1": house_type_lo1,
        "house_type_lo2": house_type_lo2,
"status":status,
        "self_interest": self_interest,
        "lo1_interest": lo1_interest,
        "lo2_interest": lo2_interest,

        "self_loan_date": self_loan_date_val,
        "lo1_loan_date": lo1_loan_date_val,
        "lo2_loan_date": lo2_loan_date_val,

        "self_one_fifth_interest": self_one_fifth_interest,
        "lo1_one_fifth_interest": lo1_one_fifth_interest,
        "lo2_one_fifth_interest": lo2_one_fifth_interest,

        "self_net_income": self_net_income,
        "lo1_net_income": lo1_net_income,
        "lo2_net_income": lo2_net_income,

        "self_tds_self_lease": self_tds_self_lease,
        "lo1_tds_self_lease": lo1_tds_self_lease,
        "lo2_tds_self_lease": lo2_tds_self_lease,

        "self_cess_self_business": self_cess_self_business,   # ← ADDED
        "lo1_cess_self_business": lo1_cess_self_business,    # ← ADDED
        "lo2_cess_self_business": lo2_cess_self_business,    # ← ADDED

        "self_cess_self_lease": self_cess_self_lease,
        "lo1_cess_self_lease": lo1_cess_self_lease,
        "lo2_cess_self_lease": lo2_cess_self_lease,

        "self_capital_gains": self_capital_gains,
        "lo1_capital_gains": lo1_capital_gains,
        "lo2_capital_gains": lo2_capital_gains,

        "self_other_sources": self_other_sources,
        "lo1_other_sources": lo1_other_sources,
        "lo2_other_sources": lo2_other_sources,

        "self_aggregate_items": self_aggregate_items,
        "lo1_aggregate_items": lo1_aggregate_items,
        "lo2_aggregate_items": lo2_aggregate_items,

        "self_tds_other_income": self_tds_other_income,
        "lo1_tds_other_income": lo1_tds_other_income,
        "lo2_tds_other_income": lo2_tds_other_income,

        "self_cess_other_income": self_cess_other_income,
        "lo1_cess_other_income": lo1_cess_other_income,
        "lo2_cess_other_income": lo2_cess_other_income,

        "self_total_tds": self_total_tds,
        "lo1_total_tds": lo1_total_tds,
        "lo2_total_tds": lo2_total_tds,

        "self_total_cess": self_total_cess,
        "lo1_total_cess": lo1_total_cess,
        "lo2_total_cess": lo2_total_cess,

        "declared_place": declared_place,
        "declared_date": declared_date_value,
        "signature_name": signature_name,
    }

    if stored_files:
        payload["upload_document"] = stored_files

    if signature_path:
        payload["signature"] = signature_path

    payload_clean = {k: v for k, v in payload.items()}

    # --------------------------------------------------
    # INSERT
    # --------------------------------------------------
    if form_id is None:
        sql = text(f"""
            INSERT INTO employee_form_12c ({", ".join(payload_clean.keys())})
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
                form_name="Form 12C",
                status=status,
                bg=bg
            )

        return record

    # --------------------------------------------------
    # UPDATE
    # --------------------------------------------------
    payload_clean["form_id"] = form_id

    sql = text(f"""
        UPDATE employee_form_12c
        SET {", ".join([f"{k} = :{k}" for k in payload_clean if k != "form_id"])}
        WHERE form_id = :form_id
        RETURNING *;
    """)

    row = db.execute(sql, payload_clean).fetchone()
    db.commit()

    if not row:
        raise HTTPException(status_code=404, detail="Form 12C record not found")

    record = dict(row._mapping)

    # --- NOTIFICATION TRIGGER ---
    user = db.query(User).filter(User.user_id == user_id).first()

    if user:
        await handle_employee_form_submission(
            db=db,
            employee_username=user.username,
            form_name="Form 12C",
            status=status,
            bg=bg,
            reference_id=str(user_id),
            redirect_url=f"/profile/profile-info/{str(user_id)}/review"
        )

    return record







# # app/routers/form12c.py

# from datetime import datetime
# import os
# import shutil
# from typing import List

# from fastapi import APIRouter, BackgroundTasks, Depends, File, Form, HTTPException, UploadFile
# from sqlalchemy import text
# from sqlalchemy.orm import Session

# from app.database import get_db
# from app.crud.employees_info.employee_notifications_crud import handle_employee_form_submission
# from app.crud.employees_info.employee_form_12c_crud import (
#     get_all_form12c,
#     get_form12c_by_id,
#     get_form12c_by_user_id,
#     get_user_basic_info,
# )

# from app.models.UserModel import User
# from app.routers.UserAuthR2 import make_download_url

# router = APIRouter(prefix="/api/form12c", tags=["Form 12C"])

# UPLOAD_DIR = "files/employee_form12"
# os.makedirs(UPLOAD_DIR, exist_ok=True)


# # ======================================
# # SERIALIZER
# # ======================================

# def serialize_form12c(row, user=None):

#     if not row:
#         return None

#     def fix_file(path):
#         return make_download_url(path) if path else None

#     if user:
#         employee_code = user.get("employee_code")
#         first = user.get("first_name")
#         last = user.get("last_name")
#         employee_full_name = f"{first} {last}".strip() if first or last else None
#     else:
#         employee_code = None
#         employee_full_name = None

#     return {
#         **row,
#         "employee_code": employee_code,
#         "employee_full_name": employee_full_name,
#         "submission_type": "Form 12",
#         "status": row.get("status"),
#         "upload_document": fix_file(row.get("upload_document")),
#         "signature": fix_file(row.get("signature")),
#     }


# # ======================================
# # GET ALL
# # ======================================

# @router.get("/all")
# def route_get_all(db: Session = Depends(get_db)):

#     rows = get_all_form12c(db)
#     result = []

#     for r in rows:
#         user = get_user_basic_info(db, r.get("user_id"))
#         result.append(serialize_form12c(r, user))

#     return result


# # ======================================
# # GET BY ID
# # ======================================

# @router.get("/{form_id}")
# def route_get_by_id(form_id: int, db: Session = Depends(get_db)):

#     row = get_form12c_by_id(db, form_id)

#     if not row:
#         return None

#     user = get_user_basic_info(db, row.get("user_id"))

#     return serialize_form12c(row, user)


# # ======================================
# # GET BY USER
# # ======================================

# @router.get("/user/{user_id}")
# def route_get_by_user(user_id: int, db: Session = Depends(get_db)):

#     rows = get_form12c_by_user_id(db, user_id)

#     user = get_user_basic_info(db, user_id)

#     return [serialize_form12c(r, user) for r in rows]


# # ======================================
# # MAIN CRUD
# # ======================================

# @router.post("/crud")
# async def employee_form_12c_crud(

#     form_id: str = Form(None),
#     user_id: str = Form(None),

#     financial_year: str = Form(None),
#     declared_place: str = Form(None),
#     declared_date: str = Form(None),
#     signature_name: str = Form(None),

#     status: str = Form(None),

#     upload_document: List[UploadFile] = File(None),
#     signature_file: UploadFile = File(None),

#     db: Session = Depends(get_db),
#     bg: BackgroundTasks = None
# ):

#     # ==========================
#     # DEFAULT STATUS
#     # ==========================

#     status = status if status else "Pending Approval"

#     # ==========================
#     # ID CONVERSIONS
#     # ==========================

#     if form_id in (None, "", "null", "None"):
#         form_id = None
#     else:
#         form_id = int(form_id)

#     if user_id in (None, "", "null", "None"):
#         user_id = None
#     else:
#         user_id = int(user_id)

#     # ==========================
#     # DATE PARSER
#     # ==========================

#     def parse_date(val):

#         if val in (None, "", "null", "None"):
#             return None

#         return datetime.strptime(val, "%Y-%m-%d").date()

#     declared_date_value = parse_date(declared_date)

#     # ==========================
#     # FILE UPLOAD
#     # ==========================

#     file_paths = []

#     if upload_document:

#         for file in upload_document:

#             save_path = os.path.join(UPLOAD_DIR, file.filename)

#             with open(save_path, "wb") as f:
#                 shutil.copyfileobj(file.file, f)

#             file_paths.append(save_path)

#     stored_files = ",".join(file_paths) if file_paths else None

#     signature_path = None

#     if signature_file:

#         signature_path = os.path.join(UPLOAD_DIR, signature_file.filename)

#         with open(signature_path, "wb") as f:
#             shutil.copyfileobj(signature_file.file, f)

#     # ==========================
#     # PAYLOAD
#     # ==========================

#     payload = {
#         "user_id": user_id,
#         "financial_year": financial_year,
#         "status": status,
#         "declared_place": declared_place,
#         "declared_date": declared_date_value,
#         "signature_name": signature_name,
#     }

#     if stored_files:
#         payload["upload_document"] = stored_files

#     if signature_path:
#         payload["signature"] = signature_path

#     payload_clean = {k: v for k, v in payload.items()}

#     # ======================================
#     # INSERT
#     # ======================================

#     if form_id is None:

#         sql = text(f"""
#             INSERT INTO employee_form_12c ({", ".join(payload_clean.keys())})
#             VALUES ({", ".join([f":{k}" for k in payload_clean.keys()])})
#             RETURNING *;
#         """)

#         row = db.execute(sql, payload_clean).fetchone()

#         db.commit()

#         record = dict(row._mapping)

#         user = db.query(User).filter(User.user_id == user_id).first()

#         if user:

#             await handle_employee_form_submission(
#                 db=db,
#                 employee_username=user.username,
#                 form_name="Form 12C",
#                 status=status,
#                 bg=bg
#             )

#         return record

#     # ======================================
#     # UPDATE
#     # ======================================

#     payload_clean["form_id"] = form_id

#     sql = text(f"""
#         UPDATE employee_form_12c
#         SET {", ".join([f"{k} = :{k}" for k in payload_clean if k != "form_id"])}
#         WHERE form_id = :form_id
#         RETURNING *;
#     """)

#     row = db.execute(sql, payload_clean).fetchone()

#     db.commit()

#     if not row:
#         raise HTTPException(status_code=404, detail="Form 12C record not found")

#     record = dict(row._mapping)

#     user = db.query(User).filter(User.user_id == user_id).first()

#     if user:

#         await handle_employee_form_submission(
#             db=db,
#             employee_username=user.username,
#             form_name="Form 12C",
#             status=status,
#             bg=bg
#         )

#     return record

