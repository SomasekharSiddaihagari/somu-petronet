from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class CategoryCreate(BaseModel):
    category_id: Optional[int] = None
    category_name: Optional[str] = None
    description: Optional[str] = None
    created_by: Optional[int] = None
    created_date: datetime

class CategoryUpdate(BaseModel):
    category_name: Optional[str] = None
    description: Optional[str] = None
    updated_by: Optional[int] = None
    updated_date: Optional[datetime] = None
