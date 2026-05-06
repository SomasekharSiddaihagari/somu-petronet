from datetime import date, datetime, time
from typing import Optional
from pydantic import BaseModel, ConfigDict

class ProductDispatchCategoryBase(BaseModel):
    station: Optional[str] = None
    station_in_charge: Optional[str] = None
    shift: Optional[str] = None
    start_time: Optional[time] = None
    logbook_date: Optional[date] = None
    ms_logbook_id: Optional[int] = None
    technician_id: Optional[int] = None

    # Audit Trail
    created_at: Optional[datetime] = None
    created_by: Optional[int] = None
    updated_at: Optional[datetime] = None
    updated_by: Optional[int] = None

    model_config = ConfigDict(from_attributes=True)

class ProductDispatchCategoryCreate(ProductDispatchCategoryBase):
    pass

class ProductDispatchCategoryUpdate(ProductDispatchCategoryBase):
    pass

class ProductDispatchCategoryResponse(ProductDispatchCategoryBase):
    p_category_master_id: int
    created_by_name: Optional[str] = None
    updated_by_name: Optional[str] = None
