# app/schemas/digital_logbook/digital_cp_reading/cp_reading_entry_schema.py
from pydantic import BaseModel, ConfigDict, Field
from typing import Optional
from app.utils.schema_validators import FlexDate, FlexTime, FlexDatetime


class CPReadingEntryBase(BaseModel):
    master_id: Optional[int] = Field(None, description="Master record ID")
    sr_no: Optional[int] = None
    entry_date: Optional[FlexDate] = None
    entry_time: Optional[FlexTime] = None
    remarks: Optional[str] = None

    # Station 1: MLR
    mlr_ac_ip_v: Optional[str] = None
    mlr_psp_ve: Optional[str] = None
    mlr_ac_ip_amp: Optional[str] = None
    mlr_op_dc_v: Optional[str] = None
    mlr_op_dc_amp: Optional[str] = None
    sv1_ac_ip_v: Optional[str] = None
    sv1_psp_ve: Optional[str] = None
    sv1_ac_ip_amp: Optional[str] = None
    sv1_op_dc_v: Optional[str] = None
    sv1_op_dc_amp: Optional[str] = None
    sv2_ac_ip_v: Optional[str] = None
    sv2_psp_ve: Optional[str] = None
    sv2_ac_ip_amp: Optional[str] = None
    sv2_op_dc_v: Optional[str] = None
    sv2_op_dc_amp: Optional[str] = None

    # Station 2: NER
    ner_ac_ip_v: Optional[str] = None
    ner_psp_ve: Optional[str] = None
    ner_ac_ip_amp: Optional[str] = None
    ner_op_dc_v: Optional[str] = None
    ner_op_dc_amp: Optional[str] = None
    sv3_ac_ip_v: Optional[str] = None
    sv3_psp_ve: Optional[str] = None
    sv3_ac_ip_amp: Optional[str] = None
    sv3_op_dc_v: Optional[str] = None
    sv3_op_dc_amp: Optional[str] = None
    sv4_ac_ip_v: Optional[str] = None
    sv4_psp_ve: Optional[str] = None
    sv4_ac_ip_amp: Optional[str] = None
    sv4_op_dc_v: Optional[str] = None
    sv4_op_dc_amp: Optional[str] = None

    # Station 3: HSN
    hsn_ac_ip_v: Optional[str] = None
    hsn_psp_ve: Optional[str] = None
    hsn_ac_ip_amp: Optional[str] = None
    hsn_op_dc_v: Optional[str] = None
    hsn_op_dc_amp: Optional[str] = None
    sv5_ac_ip_v: Optional[str] = None
    sv5_psp_ve: Optional[str] = None
    sv5_ac_ip_amp: Optional[str] = None
    sv5_op_dc_v: Optional[str] = None
    sv5_op_dc_amp: Optional[str] = None
    sv6_ac_ip_v: Optional[str] = None
    sv6_psp_ve: Optional[str] = None
    sv6_ac_ip_amp: Optional[str] = None
    sv6_op_dc_v: Optional[str] = None
    sv6_op_dc_amp: Optional[str] = None
    sv7_ac_ip_v: Optional[str] = None
    sv7_psp_ve: Optional[str] = None
    sv7_ac_ip_amp: Optional[str] = None
    sv7_op_dc_v: Optional[str] = None
    sv7_op_dc_amp: Optional[str] = None

    # Station 4: DKN
    dkn_ac_ip_v: Optional[str] = None
    dkn_psp_ve: Optional[str] = None
    dkn_ac_ip_amp: Optional[str] = None
    dkn_op_dc_v: Optional[str] = None
    dkn_op_dc_amp: Optional[str] = None
    sv8_ac_ip_v: Optional[str] = None
    sv8_psp_ve: Optional[str] = None
    sv8_ac_ip_amp: Optional[str] = None
    sv8_op_dc_v: Optional[str] = None
    sv8_op_dc_amp: Optional[str] = None
    ipstn_ac_ip_v: Optional[str] = None
    ipstn_psp_ve: Optional[str] = None
    ipstn_ac_ip_amp: Optional[str] = None
    ipstn_op_dc_v: Optional[str] = None
    ipstn_op_dc_amp: Optional[str] = None
    sv9_ac_ip_v: Optional[str] = None
    sv9_psp_ve: Optional[str] = None
    sv9_ac_ip_amp: Optional[str] = None
    sv9_op_dc_v: Optional[str] = None
    sv9_op_dc_amp: Optional[str] = None
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

class CPReadingEntryCreate(CPReadingEntryBase):
    master_id: int = Field(..., description="Required: parent master ID")

class CPReadingEntryUpdate(CPReadingEntryBase):
    pass

class CPReadingEntryResponse(CPReadingEntryBase):
    cp_entry_id: Optional[int] = None
    created_by_name: Optional[str] = None
    updated_by_name: Optional[str] = None
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)
