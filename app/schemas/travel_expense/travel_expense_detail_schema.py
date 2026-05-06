from pydantic import BaseModel
from typing import Optional, List
from datetime import date

class TravelExpenseDetailBase(BaseModel):
    from_date: Optional[date] = None
    travel_route: Optional[str] = None

    air_rail_bus_amount: Optional[float] = None
    air_rail_bus_gst: Optional[float] = None
    air_rail_bus_total: Optional[float] = None

    hotel_amount: Optional[float] = None
    hotel_gst: Optional[float] = None
    hotel_total: Optional[float] = None

    daily_allowance_amount: Optional[float] = None
    daily_allowance_gst: Optional[float] = None
    daily_allowance_total: Optional[float] = None

    local_conveyance_amount: Optional[float] = None
    local_conveyance_gst: Optional[float] = None
    local_conveyance_total: Optional[float] = None

    other_amount: Optional[float] = None
    other_gst: Optional[float] = None
    other_total: Optional[float] = None

    remarks: Optional[str] = None


class TravelExpenseDetailCreate(TravelExpenseDetailBase):
    expense_sheet_id: int


class TravelExpenseDetailUpdate(TravelExpenseDetailBase):
    pass
