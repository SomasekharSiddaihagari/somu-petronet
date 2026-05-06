from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class FuelRateCreate(BaseModel):
    petrol_rate: float
    others_rate: float


class FuelRateUpdate(BaseModel):
    petrol_rate: Optional[float] = None
    others_rate: Optional[float] = None


from pydantic import BaseModel
from datetime import datetime


class FuelRateResponse(BaseModel):
    fuel_claim_id: int
    petrol_rate: float | None
    others_rate: float | None
    created_at: datetime
    updated_at: datetime

