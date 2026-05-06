# app/schemas/mfm_accounting_hsn_schema.py
from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime, time


class MFMAccountingHSNBase(BaseModel):
    # Header
    station: Optional[str] = None
    station_in_charge: Optional[str] = None
    shift: Optional[str] = None
    start_time: Optional[time] = None
    status: Optional[str] = None
    document_number: Optional[str] = None
    otr_no: Optional[str] = None
    mfm_number: Optional[str] = None
    receiving_company: Optional[str] = None
    entry_date: Optional[date] = None

    tank_no: Optional[str] = None
    product: Optional[str] = None
    mrpl_batch_no: Optional[str] = None
    pmhbl_batch_no: Optional[str] = None

    # Opening
    open_vol_kl_amb: Optional[float] = None
    open_vol_kl_15c: Optional[float] = None
    open_mass_mt: Optional[float] = None
    open_density_amb: Optional[float] = None
    open_density_15c: Optional[float] = None
    open_temp: Optional[float] = None
    open_date: Optional[date] = None
    open_time: Optional[time] = None

    # Closing
    close_vol_kl_amb: Optional[float] = None
    close_vol_kl_15c: Optional[float] = None
    close_mass_mt: Optional[float] = None
    close_density_amb: Optional[float] = None
    close_density_15c: Optional[float] = None
    close_temp: Optional[float] = None
    close_date: Optional[date] = None
    close_time: Optional[time] = None

    # Remarks
    remarks: Optional[str] = None

    # Signatures
    sign_open_pmhbl: Optional[str] = None
    sign_open_pmhbl_time: Optional[datetime] = None
    sign_open_hpcl: Optional[str] = None
    sign_open_hpcl_time: Optional[datetime] = None
    sign_close_pmhbl: Optional[str] = None
    sign_close_pmhbl_time: Optional[datetime] = None
    sign_close_hpcl: Optional[str] = None
    sign_close_hpcl_time: Optional[datetime] = None

    name_open_pmhbl: Optional[str] = None
    name_open_hpcl: Optional[str] = None
    name_close_pmhbl: Optional[str] = None
    name_close_hpcl: Optional[str] = None

    quality_tranfered_amb_total: Optional[float] = None
    quality_tranfered_15c_total: Optional[float] = None
    quality_tranfered_mass_total: Optional[float] = None

    created_at : Optional[datetime] = None
    created_by :Optional[int] = None
    updated_at: Optional[datetime] = None
    updated_by: Optional[int] = None
class MFMAccountingHSNCreate(MFMAccountingHSNBase):
    pass


class MFMAccountingHSNUpdate(MFMAccountingHSNBase):
    pass
