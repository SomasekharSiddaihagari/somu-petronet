from dataclasses import Field

from pydantic import BaseModel
from datetime import datetime
from typing import Dict, List, Optional
import json


# ===========================
# BASE
# ===========================
class EmployeeBankBase(BaseModel):
    bank_name: str | None = None
    branch_name: str | None = None
    account_number: str | None = None
    ifsc_code: str | None = None
    account_holder_name: str | None = None
    account_type: str | None = None
    document_details: str | None = None  # JSON string of existing documents
    comment: str | None = None
    cancelled_cheque: str | None = None
    is_active: bool | None = None
    status: str | None = None
    remarks: str | None = None
    # changed_fields: Optional[List[dict]] = Field(default_factory=list)


# ===========================
# CREATE
# ===========================
class EmployeeBankCreate(EmployeeBankBase):
    user_id: int


# ===========================
# UPDATE
# ===========================
class EmployeeBankUpdate(EmployeeBankBase):
    pass


# ===========================
# OUTPUT
# ===========================


class EmployeeBankOut(EmployeeBankBase):
    id: int
    user_id: int
    document_name: List[str] | None = None
    

    class Config:
        from_attributes = True

    @classmethod
    def model_validate(cls, obj):
        if obj.get("document_name"):
            obj["document_name"] = json.loads(obj["document_name"])
        return super().model_validate(obj)

