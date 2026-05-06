from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List
 
class HRActionCreate(BaseModel):
    user_id: int
    action_type: str
    action_date: datetime
    justification: str
    created_by: Optional[int] = None
    
 
class HRActionUpdate(BaseModel):
    action_type: Optional[str] = None
    action_date: Optional[datetime] = None
    justification: Optional[str] = None
    acknowledgement: Optional[bool] = None
 
class HRActionDocumentResponse(BaseModel):
    id: int
    hr_action_id: int
    file_name: str
    file_path: str
    uploaded_at: datetime
 
    class Config:
        from_attributes = True
 
class HRActionResponse(BaseModel):
    id: int
    user_id: int
    action_type: str
    action_date: datetime
    justification: str
    acknowledgement: Optional[bool] = None
    is_deleted: Optional[bool] = False
    created_at: datetime
    created_by: Optional[int] = None
    attachments: List[HRActionDocumentResponse] = []
 
    class Config:
        from_attributes = True
 
class HRActionListResponse(BaseModel):
    items: List[HRActionResponse]
    total: int

class AcknowledgeActionRequest(BaseModel):
    acknowledgement: bool = True
    comments: str | None = None