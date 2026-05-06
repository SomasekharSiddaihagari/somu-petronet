from datetime import date, datetime, time
from typing import Optional, List
from pydantic import BaseModel, ConfigDict, Field
from app.schemas.digital_logbook.digital_line_fill_despatch_mlr.product_dispatch_category_schema import ProductDispatchCategoryResponse


class ProductDispatchHourlyBase(BaseModel):
    category_master_id: Optional[int] = Field(default=None, alias="p_category_master_id")
    log_date: Optional[date] = None
    log_time: Optional[time] = None

    # Mangalore Station
    mangalore_product: Optional[str] = None
    mangalore_tank: Optional[str] = None
    mangalore_batch: Optional[str] = None
    mangalore_volt: Optional[float] = None
    mangalore_curr: Optional[float] = None
    mangalore_ld: Optional[float] = None
    mangalore_temp: Optional[float] = None
    mangalore_den: Optional[float] = None
    mangalore_fmr: Optional[float] = None
    mangalore_ofc: Optional[str] = None
    mangalore_rcil: Optional[str] = None
    mangalore_flow: Optional[float] = None
    mangalore_dpg: Optional[float] = None

    # Neriya Station
    neriya_product: Optional[str] = None
    neriya_batch: Optional[str] = None
    neriya_fmr: Optional[float] = None
    neriya_flow: Optional[float] = None

    # Hassan Station
    hassan_product: Optional[str] = None
    hassan_batch: Optional[str] = None
    hassan_bpfmr: Optional[float] = None
    hassan_dfmr: Optional[float] = None
    hassan_flow: Optional[float] = None
    hassan_tank: Optional[str] = None

    # Bangalore Station
    bangalore_product: Optional[str] = None
    bangalore_batch: Optional[str] = None
    bangalore_dfmr: Optional[float] = None
    bangalore_flow: Optional[float] = None
    bangalore_tank: Optional[str] = None
    bangalore_omc: Optional[str] = None

    # Audit Trail
    created_at: Optional[datetime] = None
    created_by: Optional[int] = None
    updated_at: Optional[datetime] = None
    updated_by: Optional[int] = None

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)


class ProductDispatchHourlyCreate(ProductDispatchHourlyBase):
    pass


class ProductDispatchHourlyUpdate(ProductDispatchHourlyBase):
    pass


class ProductDispatchHourlyResponse(ProductDispatchHourlyBase):
    p_dispatch_hour_id: int
    created_by_name: Optional[str] = None
    updated_by_name: Optional[str] = None


class ProductDispatchHourlyMasterResponse(BaseModel):
    master: Optional[ProductDispatchCategoryResponse] = None
    entries: List[ProductDispatchHourlyResponse]


class ProductDispatchHourlyDateSearch(ProductDispatchCategoryResponse):
    entries: List[ProductDispatchHourlyResponse] = []

