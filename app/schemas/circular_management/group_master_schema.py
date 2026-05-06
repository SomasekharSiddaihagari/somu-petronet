from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class GroupCreate(BaseModel):
    group_name: str
    description: Optional[str] = None
    employee_ids: List[int]
    created_by: Optional[int] = None
    created_date: datetime

class GroupUpdate(BaseModel):
    group_name: Optional[str] = None
    description: Optional[str] = None
    employee_ids: Optional[List[int]] = None
    updated_by: Optional[int] = None
    updated_date: Optional[datetime] = None
