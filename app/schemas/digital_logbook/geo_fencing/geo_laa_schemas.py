from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List


# ---------- TOKEN RESPONSE ----------
class LocationTokenResponseSchema(BaseModel):
    id: int
    user_id: int
    station_id: int
    token: str
    access_type: str
    ip_address: str
    latitude: float
    longitude: float
    approved_by_user_id: Optional[int]
    expires_at: datetime
    is_active: bool


# ---------- GET RESPONSE ----------
class LocationTokenListResponse(BaseModel):
    user_id: int
    tokens: List[LocationTokenResponseSchema]
from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class AccessTokenGetResponse(BaseModel):
    status: str
    token: Optional[str] = None
    expires_at: Optional[datetime] = None
    next_action: Optional[str] = None


# ---------- APPROVAL UPDATE ----------
class ApprovalUpdateSchema(BaseModel):
    status: str  # APPROVED / REJECTED

from pydantic import BaseModel
from typing import Optional


class ApproveRequestSchema(BaseModel):
    approver_user_id: int
    latitude: float
    longitude: float
    reason: Optional[str] = None


class RejectRequestSchema(BaseModel):
    approver_user_id: int
    reason: Optional[str] = None
