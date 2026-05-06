# app/schemas/dg_250kva_entry_schema.py
from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime, time


class DG250KVAEntryBase(BaseModel):
    master_id: Optional[int] = None

    log_date: Optional[date] = None

    start_time: Optional[datetime] = None
    stop_time: Optional[datetime] = None
    run_time: Optional[str] = None

    cumulative: Optional[float] = None
    hmr: Optional[float] = None
    battery_voltage: Optional[float] = None
    lube_oil_pressure: Optional[float] = None
    rpm: Optional[float] = None
    electrical_hmr: Optional[float] = None
    water_temperature: Optional[float] = None

    # Voltage
    voltage_load: Optional[float] = None
    voltage_ry: Optional[float] = None
    voltage_yb: Optional[float] = None
    voltage_br: Optional[float] = None

    # Current
    current_r: Optional[float] = None
    current_y: Optional[float] = None
    current_b: Optional[float] = None

    # KWH
    kwh_initial: Optional[float] = None
    kwh_final: Optional[float] = None
    kwh_consumed: Optional[float] = None
    kwh_cumulative: Optional[float] = None

    # Diesel
    diesel_initial: Optional[float] = None
    diesel_final: Optional[float] = None
    diesel_consumed: Optional[float] = None
    diesel_total: Optional[float] = None

    remarks: Optional[str] = None
    signature: Optional[str] = None


    created_at : Optional[datetime] = None
    created_by :Optional[int] = None
    updated_at: Optional[datetime] = None
    updated_by: Optional[int] = None

class DG250KVAEntryCreate(DG250KVAEntryBase):
    pass


class DG250KVAEntryUpdate(DG250KVAEntryBase):
    pass
