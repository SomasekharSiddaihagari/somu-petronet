from pydantic import BaseModel
from datetime import date
from typing import Optional





# -------------------- HOTEL --------------------
class HotelBase(BaseModel):
    requisition_id: Optional[int]
    city: Optional[str]
    hotel_name: Optional[str]
    hotel_remarks: Optional[str]


class HotelCreate(HotelBase):
    pass


class HotelUpdate(HotelBase):
    pass

