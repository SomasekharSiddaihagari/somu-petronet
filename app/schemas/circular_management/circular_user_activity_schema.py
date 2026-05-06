from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class CircularRead(BaseModel):
    circular_id: int
    user_id: int


class CircularAcknowledge(BaseModel):
    circular_id: int
    user_id: int


class CircularUserActivityResponse(BaseModel):
    employee_name: str
    # department: str
    station_id:str
    station_name: str
    status: str
    read_at: Optional[datetime]
    acknowledged_at: Optional[datetime]
