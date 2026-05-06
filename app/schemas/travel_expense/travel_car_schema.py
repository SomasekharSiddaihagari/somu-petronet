from pydantic import BaseModel
from datetime import date
from typing import Optional


# -------------------- CAR --------------------
class CarBase(BaseModel):
    requisition_id: Optional[int]
    city: Optional[str]
    car_from: Optional[str]
    car_to: Optional[str]
    car_type: Optional[str]
    car_remarks: Optional[str]


class CarCreate(CarBase):
    pass


class CarUpdate(CarBase):
    pass
