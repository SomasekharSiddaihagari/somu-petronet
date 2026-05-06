# app/routers/asset_declaration.py
from datetime import datetime
import os
import shutil
from typing import List, Union
import uuid
from fastapi import APIRouter, BackgroundTasks, Depends, File, Form, HTTPException, UploadFile
from sqlalchemy import text
from sqlalchemy.orm import Session
from app.crud.employees_info.employee_notifications_crud import handle_employee_form_submission
from app.database import get_db
from app.crud.employees_info.asset_declaration_crud import (
    get_all_asset_declarations,
    get_asset_declaration_by_id,
    get_asset_declaration_by_user_id,
)
from app.models.UserModel import User
from app.models.employees_info.asset_declaration import UserAssetDeclaration
from app.routers.UserAuthR2 import make_download_url
from app.routers.employees_info.employee_family_routers import UPLOAD_DIR
from app.schemas.employees_info.asset_declaration_schemas import AssetCreateUpdate,  AssetResponse

router = APIRouter(prefix="/api/asset-declaration", tags=["Asset Declaration"])

UPLOAD_ROOT = "files/asset_declaration"
os.makedirs(UPLOAD_ROOT, exist_ok=True)

def serialize_asset(row, user=None):

    get = row.get if isinstance(row, dict) else lambda k: getattr(row, k)

    # ---------------- EMPLOYEE DETAILS ----------------
    if user:
        employee_code = user.get("employee_code")
        first = user.get("first_name")
        last = user.get("last_name")
        employee_full_name = f"{first} {last}".strip() if first or last else None
    else:
        employee_code = None
        employee_full_name = None
    # --------------------------------------------------

    # ----------------------------- 
    # HANDLE MULTIPLE DOCUMENTS 
    # ----------------------------- 
    raw_docs = get("document")

    if raw_docs in (None, "", "null", "None"):
        document_urls = []
    else:
        paths = [p.strip() for p in raw_docs.split(",") if p.strip()]
        document_urls = [make_download_url(p) for p in paths]

    # ----------------------------- 
    # HANDLE SIGNATURE (1 FILE ONLY) 
    # ----------------------------- 
    raw_signature = get("signature")
    signature_url = make_download_url(raw_signature) if raw_signature else None

    return {
        "asset_id": get("asset_id"),
        "user_id": get("user_id"),
        "date": get("date"),
        "financial_year": get("financial_year"),

        # New fields – EXACTLY LIKE form12c
        "employee_code": employee_code,
        "employee_full_name": employee_full_name,

        # EXISTING
        "document": document_urls,
        "asset_type": get("asset_type"),
        "details": get("details"),
        "held_in_name": get("held_in_name"),
        "acquisition_date": get("acquisition_date"),
        "nature": get("nature"),
        "party": get("party"),
        "finance_amount": get("finance_amount"),
        "source_of_finance": get("source_of_finance"),
        "profit_amount": get("profit_amount"),
        "status":get("status"),
        "signature": signature_url,
    }

# GET ALL
@router.get("/get-all")
def route_get_all(db: Session = Depends(get_db)):
    rows = get_all_asset_declarations(db)

    results = []

    for row in rows:
        # row is a dict → use row["user_id"] or row.get("user_id")
        user_id = row.get("user_id")

        user_obj = db.query(User).filter(User.user_id == user_id).first()

        if user_obj:
            user_dict = {
                "employee_code": user_obj.employee_code,
                "first_name": user_obj.first_name,
                "last_name": user_obj.last_name
            }
        else:
            user_dict = None

        results.append(serialize_asset(row, user=user_dict))

    return results



# GET BY ASSET ID
@router.get("/{asset_id}")
def route_get_by_id(asset_id: int, db: Session = Depends(get_db)):
    row = get_asset_declaration_by_id(db, asset_id)
    if not row:
        return None
    return serialize_asset(row)


# GET BY USER ID
@router.get("/user/{user_id}")
def route_get_by_user(user_id: int, db: Session = Depends(get_db)):
    rows = get_asset_declaration_by_user_id(db, user_id)

    # Fetch employee/user info once
    user_obj = db.query(User).filter(User.user_id == user_id).first()

    if user_obj:
        user_dict = {
            "employee_code": user_obj.employee_code,
            "first_name": user_obj.first_name,
            "last_name": user_obj.last_name,
        }
    else:
        user_dict = None

    return [serialize_asset(row, user=user_dict) for row in rows]



@router.post("/curd", response_model=AssetResponse)
async def create_or_update_asset(
    asset_id: str = Form(None),
    user_id: int = Form(...),
    date: str = Form(None),
    financial_year: str = Form(None),
    asset_type: str = Form(None),
    details: str = Form(None),
    held_in_name: str = Form(None),
    acquisition_date: str = Form(None),
    nature: str = Form(None),
    party: str = Form(None),
    finance_amount: float = Form(None),
    source_of_finance: str = Form(None),
    profit_amount: float = Form(None),
    status:str = Form(None),

    # MULTIPLE DOC UPLOAD
    document: List[UploadFile] = File(None),

    # SINGLE SIGNATURE
    signature: UploadFile = File(None),
    bg: BackgroundTasks=None,
    db: Session = Depends(get_db)
):
    # ------------------------------------
    # Convert asset_id
    # ------------------------------------
    if asset_id in (None, "", "null", "None"):
        asset_id = None
    else:
        try:
            asset_id = int(asset_id)
        except:
            raise HTTPException(400, "asset_id must be an integer")

    # ------------------------------------
    # Save uploaded documents + signature
    # ------------------------------------
    os.makedirs(UPLOAD_DIR, exist_ok=True)

    # MULTIPLE DOCUMENT UPLOAD
    doc_paths = []
    if document:
        for file in document:
            file_path = os.path.join(UPLOAD_DIR, file.filename) # type: ignore
            with open(file_path, "wb") as f:
                f.write(await file.read())
            doc_paths.append(file_path)

    # stored as comma-separated paths
    stored_docs = ",".join(doc_paths) if doc_paths else None

    # SINGLE SIGNATURE
    signature_path = None
    if signature:
        sign_name = signature.filename
        signature_path = os.path.join(UPLOAD_DIR, sign_name) # type: ignore
        with open(signature_path, "wb") as f:
            f.write(await signature.read())

    # ------------------------------------
    # UPDATE existing record
    # ------------------------------------
    if asset_id:
        record = db.query(UserAssetDeclaration).filter(
            UserAssetDeclaration.asset_id == asset_id
        ).first()

        if not record:
            raise HTTPException(status_code=404, detail="Asset not found")

        record.user_id = user_id# type: ignore
        record.date = date# type: ignore
        record.financial_year = financial_year# type: ignore
        record.asset_type = asset_type# type: ignore
        record.details = details# type: ignore
        record.status=status# type: ignore
        record.held_in_name = held_in_name# type: ignore
        record.acquisition_date = acquisition_date# type: ignore
        record.nature = nature# type: ignore
        record.party = party# type: ignore
        record.finance_amount = finance_amount# type: ignore
        record.source_of_finance = source_of_finance# type: ignore
        record.profit_amount = profit_amount # type: ignore

        if stored_docs:
            record.document = stored_docs   # type: ignore

        if signature_path:
            record.signature = signature_path

        db.commit()
        db.refresh(record)
            # --- NOTIFICATION TRIGGER ---
        user = db.query(User).filter(User.user_id == user_id).first()

        if user:
            await handle_employee_form_submission(
                db=db,
                employee_username=user.username, # type: ignore
                form_name="Asset Declaration",
                status=status,
                bg=bg
            )

        return record

    # ------------------------------------
    # INSERT new record
    # ------------------------------------
    new_asset = UserAssetDeclaration(
        user_id=user_id,
        date=date,
        financial_year=financial_year,
        asset_type=asset_type,
        details=details,
        status=status,
        held_in_name=held_in_name,
        acquisition_date=acquisition_date,
        nature=nature,
        party=party,
        finance_amount=finance_amount,
        source_of_finance=source_of_finance,
        profit_amount=profit_amount,
        document=stored_docs,           # MULTIPLE FILE PATHS
        signature=signature_path        # ONE SIGNATURE
    )

    db.add(new_asset)
    db.commit()
    db.refresh(new_asset)
    record = record if asset_id else new_asset

    # --- NOTIFICATION TRIGGER ---
    user = db.query(User).filter(User.user_id == user_id).first()

    if user:
        await handle_employee_form_submission(
            db=db,
            employee_username=user.username, # type: ignore
            form_name="Asset Declaration",
            status=status,
            bg=bg
        )

    return record




