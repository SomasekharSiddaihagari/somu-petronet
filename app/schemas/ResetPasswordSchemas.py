from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional


class PasswordResetRequest(BaseModel):
    email: EmailStr

class PasswordResetSubmit(BaseModel):
    token: str
    newPassword: str
    confirmPassword: str