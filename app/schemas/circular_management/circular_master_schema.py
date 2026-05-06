from pydantic import BaseModel
from typing import List,Optional
from datetime import datetime

class TargetAudience(BaseModel):
    audience_type: str   # GROUP | DEPT | STATION | USER
    audience_ref_id: List[int] 

class CircularBase(BaseModel):
    title: Optional[str] = None
    category_id: int
    subcategory_id: Optional[int] = None
    content: Optional[str] = None
    change_type: Optional[str] = None
    mandatory_status: Optional[bool] = False
    status: Optional[str] = "ACTIVE"

class CircularCreate(CircularBase):
    title: str
    category_id: int
    subcategory_id: Optional[int] = None
    content: str
    change_type: str
    mandatory_status: bool
    status: str
    created_by: int
    tags: str
    target_audience: list[TargetAudience]

    

class CircularUpdate(BaseModel):
    title: Optional[str] = None
    category_id: Optional[int] = None
    subcategory_id: Optional[int] = None
    content: Optional[str] = None
    change_type: Optional[str] = None
    mandatory_status: Optional[bool] = None
    status: Optional[str] = None
    is_archived: Optional[bool] = None
    updated_by: int = None
    tags: Optional[str] = None
    target_audience: Optional[List[TargetAudience]] = []

class CircularResponse(CircularBase):
    circular_id: int
    read_count: int
    acknowledge_count: int
    created_date: datetime

    class Config:
        from_attributes = True
