from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class RoleBase(BaseModel):
    role_id: int
    role_name: str
    created_by: str
    created_date: Optional[datetime]
    modified_by: Optional[str] = None
    modified_date: Optional[datetime] = None
    is_deleted: Optional[bool] = False
    
class RoleCreate(RoleBase):
    pass

class RoleUpdate(BaseModel):
    role_name: str
    modified_by: int

class RoleResponse(RoleBase):
    role_id: int
    created_date: Optional[datetime]
    modified_date: Optional[datetime]
    is_deleted: bool

    class Config:
        from_attributes  = True
