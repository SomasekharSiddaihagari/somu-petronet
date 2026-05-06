from pydantic import BaseModel, validator
from typing import Optional
from datetime import date, datetime

class AssetBase(BaseModel):
    user_id: int
    date: Optional[datetime] = None
    financial_year: Optional[str] = None
    document: Optional[str] = None
    asset_type: Optional[str] = None
    details: Optional[str] = None
    held_in_name: Optional[str] = None
    acquisition_date: Optional[datetime] = None
    nature: Optional[str] = None
    party: Optional[str] = None
    finance_amount: Optional[float] = None
    source_of_finance: Optional[str] = None
    profit_amount: Optional[float] = None


class AssetCreateUpdate(AssetBase):
    asset_id: Optional[int] = None

    # Fix empty string issue
    @validator("asset_id", pre=True)
    def empty_string_to_none(cls, v):
        if v == "" or v is None:
            return None
        return v


class AssetResponse(AssetBase):
    asset_id: int
    class Config:
        orm_mode = True
