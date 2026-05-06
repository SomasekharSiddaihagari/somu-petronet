from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class SubCategoryCreate(BaseModel):
    subcategory_id: Optional[int] = None
    subcategory_name: Optional[str] = None
    category_id: Optional[int] = None
    description: Optional[str] = None
    


class SubCategoryUpdate(BaseModel):
    subcategory_name: Optional[str] = None
    category_id: Optional[int] = None
    description: Optional[str] = None
   
