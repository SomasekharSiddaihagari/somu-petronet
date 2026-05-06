# app/schemas/digital_logbook/digital_cp_reading/cp_reading_hsn_entry_schema.py
from pydantic import BaseModel, ConfigDict, Field, AliasChoices
from typing import Optional
from app.utils.schema_validators import FlexTime, FlexDate, FlexDatetime


class CPReadingHSNEntryBase(BaseModel):
    master_id: Optional[int] = Field(
        None,
        serialization_alias="hsn_master_id",
        validation_alias=AliasChoices("hsn_master_id", "master_id"),
    )
    sr_no: Optional[int] = None
    entry_date: Optional[FlexDate] = None
    entry_time: Optional[FlexTime] = None
    remarks: Optional[str] = None

    # -------- HSN --------
    hsn_ac_ip_v: Optional[str] = None
    hsn_psp_ve: Optional[str] = None
    hsn_ac_ip_amp: Optional[str] = None
    hsn_op_dc_v: Optional[str] = None
    hsn_op_dc_amp: Optional[str] = None

    # -------- SV5 --------
    sv5_ac_ip_v: Optional[str] = None
    sv5_psp_ve: Optional[str] = None
    sv5_ac_ip_amp: Optional[str] = None
    sv5_op_dc_v: Optional[str] = None
    sv5_op_dc_amp: Optional[str] = None

    # -------- SV6 --------
    sv6_ac_ip_v: Optional[str] = None
    sv6_psp_ve: Optional[str] = None
    sv6_ac_ip_amp: Optional[str] = None
    sv6_op_dc_v: Optional[str] = None
    sv6_op_dc_amp: Optional[str] = None

    # -------- SV7 --------
    sv7_ac_ip_v: Optional[str] = None
    sv7_psp_ve: Optional[str] = None
    sv7_ac_ip_amp: Optional[str] = None
    sv7_op_dc_v: Optional[str] = None
    sv7_op_dc_amp: Optional[str] = None

    created_at: Optional[FlexDatetime] = None
    created_by: Optional[int] = None
    updated_at: Optional[FlexDatetime] = None
    updated_by: Optional[int] = None

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)


class CPReadingHSNEntryCreate(CPReadingHSNEntryBase):
    pass


class CPReadingHSNEntryUpdate(CPReadingHSNEntryBase):
    pass


class CPReadingHSNEntryResponse(CPReadingHSNEntryBase):
    cp_hsn_entry_id: int
    created_by_name: Optional[str] = None
    updated_by_name: Optional[str] = None

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)
