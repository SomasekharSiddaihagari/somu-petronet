from pydantic import BaseModel
from typing import Optional, List

class PublisherBase(BaseModel):
    user_id: Optional[int] = None
    category_id: Optional[List[int]] = None
    status: Optional[str] = "ACTIVE"
    role_id: Optional[int] = None
    role_name: Optional[str] = "PUBLISHER"

class PublisherCreate(PublisherBase):
    created_by: Optional[int] = None


class PublisherUpdate(BaseModel):
    user_id: Optional[int] = None
    category_id:  Optional[List[int]] = None
    status: Optional[str] = None
    modified_by: Optional[int] = None

class PublisherResponse(PublisherBase):
    publisher_id: int

    class Config:
        from_attributes = True
