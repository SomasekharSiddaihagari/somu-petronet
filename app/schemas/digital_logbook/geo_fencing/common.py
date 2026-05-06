from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class APIResponse(BaseModel):
    status: str
    message: Optional[str] = None


class TokenResponse(BaseModel):
    token: str
    expires_at: datetime
from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class HandoverRequestSchema(BaseModel):
    station_id: int
    shift_id: int
    from_user_id: int
    to_user_id: int
    comment_for_next_incharge:str


class HandoverAcceptSchema(BaseModel):
    station_id: int
    shift_id: int
    user_id: int


class ShiftInchargeResponse(BaseModel):
    station_id: int
    shift_id: int
    user_id: int
    responsibility_from: datetime
    responsibility_to: Optional[datetime]
from pydantic import BaseModel
from datetime import datetime


class AccessValidationSchema(BaseModel):
    user_id: int
    station_id: int
    latitude: float
    longitude: float


class AccessTokenResponse(BaseModel):
    token: str
    expires_at: datetime
from pydantic import BaseModel
from datetime import datetime


class ApprovalRequestSchema(BaseModel):
    approval_id: int
    approver_user_id: int
    approver_station_id: int
    latitude: float
    longitude: float


class ApprovalResponseSchema(BaseModel):
    token: str
    expires_at: datetime
from pydantic import BaseModel
from datetime import datetime


class TokenVerificationResponse(BaseModel):
    user_id: int
    station_id: int
    expires_at: datetime
from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class AccessControlCreateSchema(BaseModel):
    station_id: int                  # 👈 REQUIRED
    station_name: Optional[str] = None
    ip_from: Optional[str] = None
    ip_to: Optional[str] = None
    latitude: Optional[str] = None
    longitude: Optional[str] = None
    radius: Optional[float] = None
    is_active: bool = True


class AccessControlUpdateSchema(BaseModel):
    station_id: Optional[int] = None  # 👈 CAN be updated if needed
    station_name: Optional[str] = None
    ip_from: Optional[str] = None
    ip_to: Optional[str] = None
    latitude: Optional[str] = None
    longitude: Optional[str] = None
    radius: Optional[float] = None
    is_active: Optional[bool] = None

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
class AccessControlResponseSchema(BaseModel):
    id: int
    station_id: int
    station_name: Optional[str]
    ip_from: Optional[str]
    ip_to: Optional[str]
    latitude: Optional[float]
    longitude: Optional[float]
    radius: Optional[float]
    is_active: bool
    created_at: datetime
    updated_at: datetime
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class RequestSchema(BaseModel):
    requested_by_user_id: int
    requested_station_id: int
    approved_by_station_id: int
    create_access_request:int
    latitude: float
    longitude: float


class ApprovalApproveSchema(BaseModel):
    approval_id: int
    approver_user_id: int
    approver_station_id: int
    latitude: float
    longitude: float


class ApprovalResponseSchema(BaseModel):
    token: str
    expires_at: datetime
# app/schemas/shift/current_incharge.py
from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class CurrentShiftInchargeSchema(BaseModel):
    station_id: int
    station_name: str
    station_code: str

    shift_id: int

    user_id: int
    username: Optional[str]
    first_name: Optional[str]
    last_name: Optional[str]
    email: Optional[str]
    employee_code: Optional[str]
    designation: Optional[str]
    grade: Optional[str]
    employment_type: Optional[str]

    role_id: Optional[int]

    responsibility_from: datetime

    class Config:
        from_attributes = True
