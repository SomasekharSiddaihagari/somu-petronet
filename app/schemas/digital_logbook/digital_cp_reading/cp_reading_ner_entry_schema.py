# app/schemas/digital_logbook/digital_cp_reading/cp_reading_ner_entry_schema.py
from pydantic import BaseModel, ConfigDict, Field, AliasChoices
from typing import Optional
from app.utils.schema_validators import FlexTime, FlexDate, FlexDatetime


class CPReadingNEREntryBase(BaseModel):
    master_id: Optional[int] = Field(
        None,
        serialization_alias="ner_master_id",
        validation_alias=AliasChoices("ner_master_id", "master_id"),
    )
    sr_no: Optional[int] = None
    entry_date: Optional[FlexDate] = None
    entry_time: Optional[FlexTime] = None
    remarks: Optional[str] = None

    # -------- NER --------
    ner_ac_ip_v: Optional[str] = None
    ner_psp_ve: Optional[str] = None
    ner_ac_ip_amp: Optional[str] = None
    ner_op_dc_v: Optional[str] = None
    ner_op_dc_amp: Optional[str] = None

    # -------- SV3 --------
    sv3_ac_ip_v: Optional[str] = None
    sv3_psp_ve: Optional[str] = None
    sv3_ac_ip_amp: Optional[str] = None
    sv3_op_dc_v: Optional[str] = None
    sv3_op_dc_amp: Optional[str] = None

    # -------- SV4 --------
    sv4_ac_ip_v: Optional[str] = None
    sv4_psp_ve: Optional[str] = None
    sv4_ac_ip_amp: Optional[str] = None
    sv4_op_dc_v: Optional[str] = None
    sv4_op_dc_amp: Optional[str] = None

    created_at: Optional[FlexDatetime] = None
    created_by: Optional[int] = None
    updated_at: Optional[FlexDatetime] = None
    updated_by: Optional[int] = None

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)


class CPReadingNEREntryCreate(CPReadingNEREntryBase):
    pass


class CPReadingNEREntryUpdate(CPReadingNEREntryBase):
    pass


class CPReadingNEREntryResponse(CPReadingNEREntryBase):
    cp_ner_entry_id: int
    created_by_name: Optional[str] = None
    updated_by_name: Optional[str] = None

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)
