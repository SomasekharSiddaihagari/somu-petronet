# app/schemas/digital_logbook/digital_cp_reading/cp_reading_dkn_entry_schema.py
from pydantic import BaseModel, ConfigDict, Field, AliasChoices
from typing import Optional
from app.utils.schema_validators import FlexTime, FlexDate, FlexDatetime


class CPReadingDKNEntryBase(BaseModel):
    master_id: Optional[int] = Field(
        None,
        serialization_alias="dkn_master_id",
        validation_alias=AliasChoices("dkn_master_id", "master_id"),
    )
    sr_no: Optional[int] = None
    entry_date: Optional[FlexDate] = None
    entry_time: Optional[FlexTime] = None
    remarks: Optional[str] = None

    # -------- DKN --------
    dkn_ac_ip_v: Optional[str] = None
    dkn_psp_ve: Optional[str] = None
    dkn_ac_ip_amp: Optional[str] = None
    dkn_op_dc_v: Optional[str] = None
    dkn_op_dc_amp: Optional[str] = None

    # -------- SV8 --------
    sv8_ac_ip_v: Optional[str] = None
    sv8_psp_ve: Optional[str] = None
    sv8_ac_ip_amp: Optional[str] = None
    sv8_op_dc_v: Optional[str] = None
    sv8_op_dc_amp: Optional[str] = None

    # -------- IP STN --------
    ipstn_ac_ip_v: Optional[str] = None
    ipstn_psp_ve: Optional[str] = None
    ipstn_ac_ip_amp: Optional[str] = None
    ipstn_op_dc_v: Optional[str] = None
    ipstn_op_dc_amp: Optional[str] = None

    # -------- SV-9 --------
    sv9_ac_ip_v: Optional[str] = None
    sv9_psp_ve: Optional[str] = None
    sv9_ac_ip_amp: Optional[str] = None
    sv9_op_dc_v: Optional[str] = None
    sv9_op_dc_amp: Optional[str] = None

    # -------- SV-10 --------
    sv10_ac_ip_v: Optional[str] = None
    sv10_psp_ve: Optional[str] = None
    sv10_ac_ip_amp: Optional[str] = None
    sv10_op_dc_v: Optional[str] = None
    sv10_op_dc_amp: Optional[str] = None

    created_at: Optional[FlexDatetime] = None
    created_by: Optional[int] = None
    updated_at: Optional[FlexDatetime] = None
    updated_by: Optional[int] = None

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)


class CPReadingDKNEntryCreate(CPReadingDKNEntryBase):
    pass


class CPReadingDKNEntryUpdate(CPReadingDKNEntryBase):
    pass


class CPReadingDKNEntryResponse(CPReadingDKNEntryBase):
    cp_dkn_entry_id: int
    created_by_name: Optional[str] = None
    updated_by_name: Optional[str] = None

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)
