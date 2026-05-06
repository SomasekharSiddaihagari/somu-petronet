# app/schemas/digital_logbook/digital_cp_reading/cp_reading_mlr_entry_schema.py
from pydantic import BaseModel, ConfigDict, Field, AliasChoices
from typing import Optional
from app.utils.schema_validators import FlexTime, FlexDate, FlexDatetime


class CPReadingMLREntryBase(BaseModel):
    master_id: Optional[int] = Field(
        None,
        serialization_alias="mlr_master_id",
        validation_alias=AliasChoices("mlr_master_id", "master_id"),
    )
    sr_no: Optional[int] = None
    entry_date: Optional[FlexDate] = None
    entry_time: Optional[FlexTime] = None
    remarks: Optional[str] = None

    # -------- MLR --------
    mlr_ac_ip_v: Optional[str] = None
    mlr_psp_ve: Optional[str] = None
    mlr_ac_ip_amp: Optional[str] = None
    mlr_op_dc_v: Optional[str] = None
    mlr_op_dc_amp: Optional[str] = None

    # -------- SV1 --------
    sv1_ac_ip_v: Optional[str] = None
    sv1_psp_ve: Optional[str] = None
    sv1_ac_ip_amp: Optional[str] = None
    sv1_op_dc_v: Optional[str] = None
    sv1_op_dc_amp: Optional[str] = None

    # -------- SV2 --------
    sv2_ac_ip_v: Optional[str] = None
    sv2_psp_ve: Optional[str] = None
    sv2_ac_ip_amp: Optional[str] = None
    sv2_op_dc_v: Optional[str] = None
    sv2_op_dc_amp: Optional[str] = None

    created_at: Optional[FlexDatetime] = None
    created_by: Optional[int] = None
    updated_at: Optional[FlexDatetime] = None
    updated_by: Optional[int] = None

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)


class CPReadingMLREntryCreate(CPReadingMLREntryBase):
    pass


class CPReadingMLREntryUpdate(CPReadingMLREntryBase):
    pass


class CPReadingMLREntryResponse(CPReadingMLREntryBase):
    cp_mlr_entry_id: int
    created_by_name: Optional[str] = None
    updated_by_name: Optional[str] = None

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)
