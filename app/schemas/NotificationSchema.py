from typing import Optional
from pydantic import BaseModel, ConfigDict
from datetime import datetime

class NotificationBase(BaseModel):
    type: str
    title: str
    description: str
    from_user: str
    to_user: str
    module_name: Optional[str] = None     
    module_status: Optional[str] = None  
    
    reference_id: Optional[str] = None
    redirect_url: Optional[str] = None


class NotificationCreate(NotificationBase):
    pass



class NotificationUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    module_name: Optional[str] = None
    module_status: Optional[str] = None
    is_read: Optional[bool] = None



class NotificationResponse(NotificationBase):
    id: int
    date: datetime
    is_read: bool

    # NEW (Pydantic V2 style)
    model_config = ConfigDict(from_attributes=True)