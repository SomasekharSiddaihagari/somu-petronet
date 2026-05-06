from datetime import date, datetime, time
from enum import Enum
from pydantic import BaseModel, ConfigDict, Field, model_validator
from typing import Optional, List
from app.schemas.digital_logbook.digital_line_fill_despatch_mlr.product_dispatch_category_schema import (
    ProductDispatchCategoryResponse,
)

# --- Enums ---

class ProductEnum(str, Enum):
    HSD = "HSD"
    SKO_PCK = "SKO/PCK"
    MS = "MS"
    PCA_ATF = "PCA/ ATF"

# --- Sub Entry Models ---

class SuctionMovement(BaseModel):
    product: Optional[ProductEnum] = None
    pmhbl_batch_no: Optional[str] = None
    mrpl_batch_no: Optional[str] = None
    quantity_kl: Optional[float] = 0.0
    model_config = ConfigDict(extra="ignore")


class LineFillEntry(BaseModel):
    section_name: Optional[str] = None # e.g., "MLR-NER"
    product: Optional[ProductEnum] = None
    pmhbl_batch_no: Optional[str] = None
    mrpl_batch_no: Optional[str] = None
    quantity_kl: Optional[float] = 0.0
    model_config = ConfigDict(extra="ignore")


class SectionCapacity(BaseModel):
    section_name: Optional[str] = None
    section_capacity: Optional[float] = 0.0
    section_current_fill: Optional[float] = 0.0
    model_config = ConfigDict(extra="ignore")

# --- Default Values for Section Capacity Summary ---
SECTION_CAPACITY_DEFAULTS = [
    {"section_name": "MLR-NER", "section_capacity": 0.0, "section_current_fill": 0.0},
    {"section_name": "NER-HSN", "section_capacity": 0.0, "section_current_fill": 0.0},
    {"section_name": "HSN-DKN", "section_capacity": 0.0, "section_current_fill": 0.0}
]

class ProductDispatchLogEntryResponse(BaseModel):
    entry_id: int
    shift_log_id: int
    entry_type: str
    section_name: Optional[str] = None
    product: Optional[str] = None
    pmhbl_batch_no: Optional[str] = None
    mrpl_batch_no: Optional[str] = None
    quantity_kl: Optional[float] = 0.0
    section_capacity: Optional[float] = 0.0
    section_current_fill: Optional[float] = 0.0
    model_config = ConfigDict(from_attributes=True)

class ProductDispatchShiftLogBase(BaseModel):
    category_master_id: Optional[int] = Field(default=None, alias="p_category_master_id")
    shift_id: Optional[int] = None
    shift: Optional[str] = None
    log_date: Optional[date] = None

    # JSON Entries using sub-models for Swagger documentation
    suction_movements: Optional[List[SuctionMovement]] = Field(
        default_factory=list,
        examples=[
            [
                {"product": "MS", "pmhbl_batch_no": "", "mrpl_batch_no": "", "quantity_kl": 0.0}
            ]
        ]
    )
    
    line_fill_entries: Optional[List[LineFillEntry]] = Field(
        default_factory=list,
        examples=[
            [
                {"section_name": "MLR-NER", "product": "MS", "pmhbl_batch_no": "", "mrpl_batch_no": "", "quantity_kl": 0.0}
            ]
        ]
    )

    section_capacity_summary: Optional[List[SectionCapacity]] = Field(
        default_factory=lambda: SECTION_CAPACITY_DEFAULTS,
        examples=[SECTION_CAPACITY_DEFAULTS]
    )

    # Booster Pump 101A
    bp_101a_previous_hrs: Optional[float] = 0.0
    bp_101a_current_hrs: Optional[float] = 0.0
    bp_101a_cumulative_hrs: Optional[float] = 0.0
    bp_101a_availability: Optional[bool] = True
    bp_101a_product: Optional[str] = None

    # Booster Pump 101B
    bp_101b_previous_hrs: Optional[float] = 0.0
    bp_101b_current_hrs: Optional[float] = 0.0
    bp_101b_cumulative_hrs: Optional[float] = 0.0
    bp_101b_availability: Optional[bool] = True
    bp_101b_product: Optional[str] = None

    # Multi-Stage Pump 102A
    mp_102a_previous_hrs: Optional[float] = 0.0
    mp_102a_current_hrs: Optional[float] = 0.0
    mp_102a_cumulative_hrs: Optional[float] = 0.0
    mp_102a_availability: Optional[bool] = True
    mp_102a_product: Optional[str] = None

    # Multi-Stage Pump 102B
    mp_102b_previous_hrs: Optional[float] = 0.0
    mp_102b_current_hrs: Optional[float] = 0.0
    mp_102b_cumulative_hrs: Optional[float] = 0.0
    mp_102b_availability: Optional[bool] = True
    mp_102b_product: Optional[str] = None

    # Multi-Stage Pump 102C
    mp_102c_previous_hrs: Optional[float] = 0.0
    mp_102c_current_hrs: Optional[float] = 0.0
    mp_102c_cumulative_hrs: Optional[float] = 0.0
    mp_102c_availability: Optional[bool] = True
    mp_102c_product: Optional[str] = None

    # Sump Pump
    sump_pump_previous_hrs: Optional[float] = 0.0
    sump_pump_current_hrs: Optional[float] = 0.0
    sump_pump_cumulative_hrs: Optional[float] = 0.0
    sump_pump_availability: Optional[bool] = True
    sump_pump_product: Optional[str] = None

    # Corrosion Inhibitor Pump 101A
    ci_pump_101a_previous_hrs: Optional[float] = 0.0
    ci_pump_101a_current_hrs: Optional[float] = 0.0
    ci_pump_101a_cumulative_hrs: Optional[float] = 0.0
    ci_pump_101a_availability: Optional[bool] = True
    ci_pump_101a_product: Optional[str] = None

    # Corrosion Inhibitor Pump 101B
    ci_pump_101b_previous_hrs: Optional[float] = 0.0
    ci_pump_101b_current_hrs: Optional[float] = 0.0
    ci_pump_101b_cumulative_hrs: Optional[float] = 0.0
    ci_pump_101b_availability: Optional[bool] = True
    ci_pump_101b_product: Optional[str] = None

    # DRA Engine
    dra_previous_hrs: Optional[float] = 0.0
    dra_current_hrs: Optional[float] = 0.0
    dra_cumulative_hrs: Optional[float] = 0.0
    dra_availability: Optional[bool] = True
    dra_product: Optional[str] = None
    total_pump_hrs: Optional[float] = 0.0

    # Fire System
    fire_pump_auto: Optional[bool] = True
    fire_pump_manual: Optional[bool] = False
    fire_pump_1_available: Optional[bool] = True
    fire_pump_2_available: Optional[bool] = True
    fire_pump_3_available: Optional[bool] = True

    # Performance
    sump_level_percent: Optional[float] = 0.0
    ci_pumped_percent: Optional[float] = 0.0
    net_qty_of_shift: Optional[float] = 0.0
    gross_qty_of_shift: Optional[float] = 0.0
    atg_qty_of_shift: Optional[float] = 0.0

    # Maintenance
    maintenance_details: Optional[str] = None
    shift_engineer_name: Optional[str] = None
    signature: Optional[str] = None

    created_by: Optional[int] = None
    updated_by: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class ProductDispatchShiftLogCreate(ProductDispatchShiftLogBase):
    pass


class ProductDispatchShiftLogUpdate(ProductDispatchShiftLogBase):
    pass


class ProductDispatchShiftLogResponse(ProductDispatchShiftLogBase):
    shift_log_id: int
    created_by_name: Optional[str] = None
    updated_by_name: Optional[str] = None

    model_config = ConfigDict(from_attributes=True, extra="ignore", populate_by_name=True)

class ProductDispatchShiftLogMasterResponse(BaseModel):
    master: Optional[ProductDispatchCategoryResponse] = None
    entries: List[ProductDispatchShiftLogResponse]


class ProductDispatchShiftLogDateSearch(ProductDispatchCategoryResponse):
    entries: List[ProductDispatchShiftLogResponse] = []
