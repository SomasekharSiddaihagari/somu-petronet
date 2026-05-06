from pydoc import text
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.crud.leave.leave_no_of_days import validate_leave_python
from app.database import get_db
from app.schemas.leave.leave_no_of_days_shema import LeaveValidationRequest, LeaveValidationResponse
from app.schemas.leave.leave_schema import LeaveApplicationCreate

router = APIRouter(prefix="/api/leave", tags=["Leave Validation"])


@router.post("/validate")
def validate_api(request: LeaveValidationRequest, db: Session = Depends(get_db)):
    return validate_leave_python(db, request)

