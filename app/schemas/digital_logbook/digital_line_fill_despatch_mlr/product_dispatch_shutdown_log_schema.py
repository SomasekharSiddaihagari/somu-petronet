from datetime import date, datetime
from typing import Optional, List, Any
from pydantic import BaseModel, ConfigDict, Field, model_validator
from app.schemas.digital_logbook.digital_line_fill_despatch_mlr.product_dispatch_category_schema import (
    ProductDispatchCategoryResponse,
)


class ProductDispatchShutdownBase(BaseModel):
    category_master_id: Optional[int] = Field(default=None, alias="p_category_master_id")
    log_date: Optional[date] = None

    # Shift A Data
    shift_a_from: Optional[float] = None
    shift_a_to: Optional[float] = None
    shift_a_subtotal: Optional[float] = None

    # Shift B Data
    shift_b_from: Optional[float] = None
    shift_b_to: Optional[float] = None
    shift_b_subtotal: Optional[float] = None

    # Shift C Data
    shift_c_from: Optional[float] = None
    shift_c_to: Optional[float] = None
    shift_c_subtotal: Optional[float] = None

    # Shutdown Summary & Totals
    total: Optional[float] = None
    pre_sd_hrs: Optional[float] = None
    cumulative: Optional[float] = None
    reason_remarks: Optional[str] = None

    # Audit Trail
    created_at: Optional[datetime] = None
    created_by: Optional[int] = None
    updated_at: Optional[datetime] = None
    updated_by: Optional[int] = None

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)


class ProductDispatchShutdownCreate(ProductDispatchShutdownBase):
    pass


class ProductDispatchShutdownUpdate(ProductDispatchShutdownBase):
    pass


class ProductDispatchShutdownResponse(ProductDispatchShutdownBase):
    p_dispatch_shutdown_id: int
    created_by_name: Optional[str] = None
    updated_by_name: Optional[str] = None
    
    # Calculated fields shown in output
    shift_a_subtotal: Optional[float] = None
    shift_b_subtotal: Optional[float] = None
    shift_c_subtotal: Optional[float] = None
    total: Optional[float] = None
    cumulative: Optional[float] = None



class ProductDispatchShutdownMasterResponse(BaseModel):
    master: Optional[ProductDispatchCategoryResponse] = None
    entries: List[ProductDispatchShutdownResponse]
    summary: Optional[dict] = None


class ProductDispatchShutdownDateSearch(ProductDispatchCategoryResponse):
    entries: List[ProductDispatchShutdownResponse] = []
    summary: Optional[dict] = None
