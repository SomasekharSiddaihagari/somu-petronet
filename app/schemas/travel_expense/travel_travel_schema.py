from pydantic import BaseModel
from datetime import date
from typing import Optional


# -------------------- TRAVEL --------------------
class TravelBase(BaseModel):
    requisition_id: Optional[int]
    from_location: Optional[str]
    to_location: Optional[str]
    travel_date: Optional[date]
    flight_train_number: Optional[str]
    class_of_travel: Optional[str]
    travel_remarks: Optional[str]
    to_date: Optional[date]


class TravelCreate(TravelBase):
    pass


class TravelUpdate(TravelBase):
    pass

