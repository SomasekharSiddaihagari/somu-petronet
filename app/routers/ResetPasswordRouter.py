from app.crud.ResetPasswordCrud import request_reset, submit_new_password_crud
from app.schemas.ResetPasswordSchemas import PasswordResetRequest, PasswordResetSubmit
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db

router = APIRouter(tags=["Reset Password"])

@router.post("/api/password-reset/submit")
def submit_new_password(data: PasswordResetSubmit, db: Session = Depends(get_db)):
    return submit_new_password_crud(
        db,
        token=data.token,
        newPassword=data.newPassword,
        confirmPassword=data.confirmPassword
    )

@router.post("/api/password-reset/request")
def request_password_reset(data: PasswordResetRequest, db: Session = Depends(get_db)):
    return request_reset(db, data.email)

