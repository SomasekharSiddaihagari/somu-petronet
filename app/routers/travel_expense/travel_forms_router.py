from decimal import Decimal
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from typing import List, Optional

from app.database import get_db

from app.crud.travel_expense.travel_forms_crud import (

    get_dashboard_summary,
    get_form_details,
    get_global_dashboard_summary,
    get_self_travel_by_user_id,
    get_travel_for_supervisor,
    get_all_travel_forms,
)
from app.models.leave.leave_balance import LeaveBalance
from app.schemas.travel_expense.travel_forms_schema import SupervisorTravelResponse, TravelFormItem

router = APIRouter(
    prefix="/api/travel-forms",
    tags=["Travel Forms"]
)


# ------------------------------------------------------------
# 1. USER SELF FORMS
# ------------------------------------------------------------
@router.get("/self/{user_id}", response_model=List[TravelFormItem])
def get_self_forms(user_id: int, db: Session = Depends(get_db)):
    rows = get_self_travel_by_user_id(db, user_id)
    return [{"data": row["data"]} for row in rows]


# ------------------------------------------------------------
# 2. SUPERVISOR FORMS
# ------------------------------------------------------------
@router.get("/supervisor/{supervisor_id}")
def get_supervisor_forms(
    supervisor_id: int,
    db: Session = Depends(get_db)
):
    return get_travel_for_supervisor(db, supervisor_id)


# ------------------------------------------------------------
# 3. ALL FORMS
# ------------------------------------------------------------
@router.get("/all")
def get_all_forms(db: Session = Depends(get_db)):
    result = get_all_travel_forms(db)
    return result



@router.get("/summary")
def global_dashboard_summary(db: Session = Depends(get_db)):
    return get_global_dashboard_summary(db)

FORM_ID_COLUMN = {
    "travel_requisition": "travel_id",
    "daily_allowance": "da_sheet_id",
    "meal_allowance": "meal_sheet_id",
    "travel_expense": "tes_id",
}


def normalize_form_type(form_type: str) -> str:
    """
    Converts frontend form_type into backend canonical key.
    Handles typos & variations safely.
    """
    if not form_type:
        return ""

    ft = (
        form_type
        .strip()
        .lower()
        .replace(" ", "_")
        .replace("-", "_")
    )

    aliases = {
        "travel_requestion": "travel_requisition",
        "travel_reqiesion": "travel_requisition",
        "travel_requisition": "travel_requisition",

        "daily_allowance": "daily_allowance",
        "daily_allowance_sheet": "daily_allowance",

        "meal_allowance": "meal_allowance",
        "meal_allowance_sheet": "meal_allowance",

        "travel_expense": "travel_expense",
        "travel_expense_sheet": "travel_expense",
    }

    return aliases.get(ft, ft)

@router.get("/summary/{user_id}")
def dashboard_summary(user_id: int, db: Session = Depends(get_db)):
    return get_dashboard_summary(db, user_id)




    
@router.get("/details/{form_type}/{form_id}")
def fetch_form_details(form_type: str, form_id: int, db: Session = Depends(get_db)):
    """
    API endpoint to return full form + child details.
    """
    print("form_type",form_type)
    normalized_form_type = normalize_form_type(form_type)
    print("normalized_form_type",normalized_form_type)
    data = get_form_details(db, normalized_form_type, form_id)

    if not data:
        raise HTTPException(
            status_code=404,
            detail={
                "message": "Form not found",
                "form_type": normalized_form_type,
                "form_id": form_id,
            }
        )

    return {
        "form_type": normalized_form_type,
        "form_id": form_id,
        "data": data
    }