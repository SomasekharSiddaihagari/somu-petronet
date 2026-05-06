# app/schemas/mfm_accounting_dkn_schema.py
from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime, time
from decimal import Decimal


class MFMAccountingDKNBase(BaseModel):
    # Header
    station: Optional[str] = None
    station_in_charge: Optional[str] = None
    shift: Optional[str] = None
    start_time: Optional[time] = None
    document_number: Optional[str] = None
    otr_no: Optional[str] = None
    mfm_number: Optional[str] = None
    receiving_company: Optional[str] = None
    log_date: Optional[date] = None

    tank_no: Optional[str] = None
    product: Optional[str] = None
    mrpl_batch_no: Optional[str] = None
    pmhbl_batch_no: Optional[str] = None

    # Opening
    opening_vol_kl_amb: Optional[Decimal] = None
    opening_vol_kl_15c: Optional[Decimal] = None
    opening_mass_mt: Optional[Decimal] = None
    opening_weighted_amb_density: Optional[Decimal] = None
    opening_weighted_temp: Optional[Decimal] = None
    opening_weighted_15c_density: Optional[Decimal] = None
    opening_date: Optional[date] = None
    opening_time: Optional[time] = None

    # Closing
    closing_vol_kl_amb: Optional[Decimal] = None
    closing_vol_kl_15c: Optional[Decimal] = None
    closing_mass_mt: Optional[Decimal] = None
    closing_weighted_amb_density: Optional[Decimal] = None
    closing_weighted_temp: Optional[Decimal] = None
    closing_weighted_15c_density: Optional[Decimal] = None
    closing_date: Optional[date] = None
    closing_time: Optional[time] = None

    # Auto-calculated
    qty_transferred_vol_kl: Optional[Decimal] = None
    qty_transferred_mass_mt: Optional[Decimal] = None
    qty_transferred_15c_total: Optional[Decimal] = None
    qty_transferred_mass_total: Optional[Decimal] = None
    qty_transferred_amb_total: Optional[Decimal] = None

    # Seals & Status
    hpcl_hsd_line_mov_seal: Optional[str] = None
    hpcl_hsd_line_mov_status: Optional[str] = None
    bpcl_hsd_line_mov_seal: Optional[str] = None
    bpcl_hsd_line_mov_status: Optional[str] = None
    iocl_hsd_line_mov_seal: Optional[str] = None
    iocl_hsd_line_mov_status: Optional[str] = None

    hpcl_hsd_line_hov_seal: Optional[str] = None
    hpcl_hsd_line_hov_status: Optional[str] = None
    bpcl_hsd_line_hov_seal: Optional[str] = None
    bpcl_hsd_line_hov_status: Optional[str] = None
    iocl_hsd_line_hov_seal: Optional[str] = None
    iocl_hsd_line_hov_status: Optional[str] = None

    mrpl_hsd_line_mov_seal: Optional[str] = None
    mrpl_hsd_line_mov_status: Optional[str] = None

    if_tank_101_mov_seal: Optional[str] = None
    if_tank_101_mov_status: Optional[str] = None
    if_tank_102_mov_seal: Optional[str] = None
    if_tank_102_mov_status: Optional[str] = None

    ms_header_line_mov_1415_seal: Optional[str] = None
    ms_header_line_mov_1415_status: Optional[str] = None
    ms_header_line_mov_1416_seal: Optional[str] = None
    ms_header_line_mov_1416_status: Optional[str] = None

    mrpl_hsd_dbvb_mov_seal: Optional[str] = None
    mrpl_hsd_dbvb_mov_status: Optional[str] = None

    # Remarks & Signatures
    remarks: Optional[str] = None
    opening_pmhbl_signature: Optional[str] = None
    opening_pmhbl_signature_time: Optional[datetime] = None
    opening_mrpl_signature: Optional[str] = None
    opening_mrpl_signature_time: Optional[datetime] = None
    closing_pmhbl_signature: Optional[str] = None
    closing_pmhbl_signature_time: Optional[datetime] = None
    closing_mrpl_signature: Optional[str] = None
    closing_mrpl_signature_time: Optional[datetime] = None

    name_open_pmhbl: Optional[str] = None
    name_open_hpcl: Optional[str] = None
    name_close_pmhbl: Optional[str] = None
    name_close_hpcl: Optional[str] = None
    created_at : Optional[datetime] = None
    created_by :Optional[int] = None
    updated_at: Optional[datetime] = None
    updated_by: Optional[int] = None

class MFMAccountingDKNCreate(MFMAccountingDKNBase):
    pass


class MFMAccountingDKNUpdate(MFMAccountingDKNBase):
    pass
