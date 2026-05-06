import datetime
import os
from fastapi import HTTPException
import token
import uuid
from app.models.UserModel import User
from app.models.ResetPasswordModel import ResetPasswordModel
from app.utils.EmailUtils import send_email
from app.utils.UserAuthUtils import get_password_hash
from sqlalchemy.orm import Session, joinedload
from datetime import datetime, timedelta

def request_reset(db: Session, email: str):

    # Find user by email
    user = db.query(User).filter(User.email == email, User.is_deleted == False).first()
    if not user:
        raise HTTPException(status_code=404, detail="No account found with this email.")

    # Generate token
    token = str(uuid.uuid4())

    # Create reset entry
    reset_entry = ResetPasswordModel(
                user_id=user.user_id,
                email=email,
                reset_token=token,
                expires_at=datetime.utcnow() + timedelta(minutes=30)
            )


    db.add(reset_entry)
    db.commit()
    db.refresh(reset_entry)
    FrontEndPath=os.getenv("FrontEndPath")
    # Email reset link
    reset_link = f"{FrontEndPath}/reset-password?token={token}&email={email}"

    email_body = (
        f"Hello {user.first_name},\n\n"
        f"Click the link below to reset your password:\n"
        f"{reset_link}\n\n"
        f"This link will expire in 30 minutes."
    )

    send_email(
        to_email=email,
        subject="Password Reset Request",
        body=email_body
    )

    return {"message": "Reset link sent to your email."}


def submit_new_password_crud(db: Session, token: str, newPassword: str, confirmPassword: str):

    reset_entry = db.query(ResetPasswordModel).filter(
        ResetPasswordModel.reset_token == token,
        ResetPasswordModel.used == False
    ).first()

    if not reset_entry:
        raise HTTPException(status_code=400, detail="Invalid or expired token.")

    # Check expiry
    if reset_entry.expires_at < datetime.utcnow():
        raise HTTPException(status_code=400, detail="Reset link expired.")

    # Check password match
    if newPassword != confirmPassword:
        raise HTTPException(status_code=400, detail="Passwords do not match.")

    # Update user password
    user = reset_entry.user
    user.hashed_password = get_password_hash(newPassword)

    # Mark reset token as used
    reset_entry.used = True

    db.commit()

    return {"message": "Password successfully reset."}