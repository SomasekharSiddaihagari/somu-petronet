from pydantic import BaseModel
from typing import List, Optional
from datetime import date


class CompOffCreate(BaseModel):
    user_id: int
    leave_application_id: Optional[int] = None
    leave_dates: List[date]
    type_id: Optional[int] = None


class CompOffResponse(BaseModel):
    id: int
    employee_name: Optional[str]
    employee_code: Optional[str]
    leave_date: date
    user_id: int
    supervisor_id: int

class CompOffValidate(BaseModel):
    # main
    user_id: int
    leave_type: str = "COMP_OFF"

    from_date: date
    to_date: date
    comp_dates: List[date]

    number_of_days: Optional[float] = 0
    reason: Optional[str] = None

    # optional employee info
    supervisor_id: Optional[int] = None
    supervisor_name: Optional[str] = None
    user_name: Optional[str] = None

    # optional document/contact
    document_path: Optional[str] = None
    contact_address: Optional[str] = None
    phone_number: Optional[str] = None

    # reversal
    reversal_from_date: Optional[date] = None
    reversal_to_date: Optional[date] = None
    reversal_remarks: Optional[str] = None

    # extra
    status: Optional[str] = "Pending"
    supervisor_remarks: Optional[str] = None
    leave_nature: Optional[str] = None

    # optional UI fields
    half_day_count: Optional[float] = 0
    selected_days: Optional[float] = 0
    
class MessageResponse(BaseModel):
    success: bool
    message: str


from datetime import date
from pydantic import BaseModel, Field, validator


class CompOffApplyRequest(BaseModel):
    user_id: int = Field(..., example=443)
    leave_type: str = Field(..., example="COMP_OFF")
    from_date: date = Field(..., example="2026-02-09")
    to_date: date = Field(..., example="2026-02-10")
    half_day_count: float | None = Field(0, example=0)

    # --------------------------------------------------
    # 🔵 VALIDATORS
    # --------------------------------------------------
    @validator("leave_type")
    def validate_leave_type(cls, v):
        if v.upper() != "COMP_OFF":
            raise ValueError("leave_type must be COMP_OFF")
        return v.upper()

    @validator("to_date")
    def validate_dates(cls, v, values):
        from_date = values.get("from_date")
        if from_date and v < from_date:
            raise ValueError("to_date cannot be before from_date")
        return v

    @validator("half_day_count")
    def validate_half_day(cls, v):
        if v not in (0, 0.5, 1, None):
            raise ValueError("half_day_count must be 0, 0.5, or 1")
        return v or 0




from pydantic import BaseModel

from pydantic import BaseModel
from typing import List

from pydantic import BaseModel
from typing import List, Optional

class CompOffItem(BaseModel):
    id: int
    is_used: bool

class BulkCompOffUpdate(BaseModel):
    user_id: int
    leave_application_id: Optional[int] = None
    comp_off_updates: List[CompOffItem]
