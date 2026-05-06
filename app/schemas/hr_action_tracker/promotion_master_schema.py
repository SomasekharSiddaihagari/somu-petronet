from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, ConfigDict


class PromotionDocumentResponse(BaseModel):
    id: int
    promotion_id: int
    file_name: str
    file_path: str
    uploaded_at: datetime
    acknowledgement: Optional[bool] = None
    is_deleted: Optional[bool] = None

    model_config = ConfigDict(from_attributes=True)
class PromotionCreate(BaseModel):
    id: int
    user_id: int
    current_grade: str
    new_grade: str
    current_designation: str
    new_designation: str
    effective_date: datetime
    remarks: Optional[str] = None
    created_by: Optional[int] = None
    created_at: Optional[datetime]= None
    

class PromotionUpdate(BaseModel):
    current_grade: Optional[str]
    new_grade: Optional[str]
    current_designation: Optional[str]
    new_designation: Optional[str]
    effective_date: Optional[datetime]
    remarks: Optional[str]


class PromotionResponse(BaseModel):
    id: int
    user_id: int
    current_grade: str
    new_grade: str
    current_designation: str
    new_designation: str
    effective_date: datetime
    remarks: Optional[str]
    attachments: List[PromotionDocumentResponse] = []
    comments: Optional[str] = None
    model_config = ConfigDict(from_attributes=True)

class AcknowledgePromotionRequest(BaseModel):
    acknowledgement: bool = True
    comments: str | None = None

# class CommonFilterRequest(BaseModel):
#     filter_type: Optional[str] = None   # today, week, days_15, month_1, month_3, month_6, quarterly, half_yearly
#     quarters: Optional[List[str]] = None   # ["Q1-2026", "Q2-2026"]
class CommonFilterRequest(BaseModel):
    filter_type: Optional[str] = None  
    from_date: Optional[str] = None
    to_date: Optional[str] = None