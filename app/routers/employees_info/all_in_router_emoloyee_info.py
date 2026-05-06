from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import text
from sqlalchemy.orm import Session
from app.database import get_db
from app.crud.employees_info.all_in_one_employee_crud import (
    get_all_forms,
    get_form_by_type_and_id,
    get_forms_by_user_id,
)
from app.routers.UserAuthR2 import make_download_url

router = APIRouter(prefix="/api/all-combined-emplyee_info", tags=["Dashboard emploee info"])

def get_user_basic_info(db: Session, user_id: int):
    row = db.execute(text("""
        SELECT employee_code, first_name, last_name
        FROM users WHERE user_id = :uid
    """), {"uid": user_id}).fetchone()

    return dict(row._mapping) if row else {
        "employee_code": None,
        "first_name": "",
        "last_name": ""
    }


def serialize_common(row, user, submission_type):
    
    def fix_file(path):
        if not path:
            return None
        return make_download_url(path)

    def fix_multiple(path_list):
        if not path_list:
            return None
        return [fix_file(p.strip()) for p in path_list.split(",")]

    return {
        **row,

        # USER DETAILS
        "employee_code": user.get("employee_code"),
        "employee_full_name": f"{user.get('first_name')} {user.get('last_name')}".strip(),

        # FIXED
        "submission_type": submission_type,

        # FILES
        "document": fix_multiple(row.get("document")) if row.get("document") else None,
        "upload_document": fix_multiple(row.get("upload_document")) if row.get("upload_document") else None,
        "signature": fix_file(row.get("signature")),
        "signature_name": fix_file(row.get("signature_name")),
    }


# -------------------------------
# GET ALL FORMS (all users)
# -------------------------------
@router.get("/all")
def api_get_all_forms(db: Session = Depends(get_db)):
    return get_all_forms(db)


# -------------------------------
# GET ALL FORMS FOR USER
# -------------------------------
# @router.get("/user/{user_id}")
# def api_get_forms_by_user(user_id: int, db: Session = Depends(get_db)):
#     result = get_forms_by_user_id(db, user_id)
#     return result

from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
import math

@router.get("/user/{user_id}")
def api_get_forms_by_user(user_id: int, db: Session = Depends(get_db)):
    result = get_forms_by_user_id(db, user_id)
    return JSONResponse(
        content=jsonable_encoder(
            result,
            custom_encoder={float: lambda v: None if math.isnan(v) else v}
        )
    )


# -------------------------------
# GET BY FORM TYPE + ID
# -------------------------------
@router.get("/{form_type}/{item_id}")
def api_get_form_by_type_and_id(form_type: str, item_id: int, db: Session = Depends(get_db)):
    
    result = get_form_by_type_and_id(db, form_type, item_id)

    if not result:
        raise HTTPException(status_code=404, detail="Record not found")

    return {
        "form_type": form_type,
        "data": result
    }
