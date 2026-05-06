from pydantic import BaseModel
from typing import Optional

class StationBase(BaseModel):
    station_id: int
    station_name: str
    station_code: str
    is_deleted: Optional[bool] = False

    class Config:
       from_attributes = True

