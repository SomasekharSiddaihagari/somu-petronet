from pydantic import BaseModel
from typing import List, Optional


class SubMenuBase(BaseModel):
    id: int
    name: str
    url: Optional[str] = None
    icon: Optional[str] = None

    class Config:
        from_attributes  = True


class MenuBase(BaseModel):
    id: int
    name: str
    url: Optional[str] = None
    icon: Optional[str] = None
    submenus: List[SubMenuBase] = []

    class Config:
        from_attributes  = True
