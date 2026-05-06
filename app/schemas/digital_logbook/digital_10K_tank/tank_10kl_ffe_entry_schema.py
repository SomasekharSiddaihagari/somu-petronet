# app/schemas/digital_logbook/digital_10K_tank/tank_10kl_ffe_entry_schema.py
from pydantic import BaseModel, ConfigDict, Field, AliasChoices
from typing import Optional
from app.utils.schema_validators import FlexFloat, FlexDatetime, FlexDate


class Tank10KLFfeEntryBase(BaseModel):
    master_id: Optional[int] = Field(
        None,
        serialization_alias="tank_ffe_master_id",
        validation_alias=AliasChoices("tank_ffe_master_id", "master_id"),
    )

    entry_date: Optional[FlexDate] = None

    opening_dip: Optional[FlexFloat] = None
    opening_qty: Optional[FlexFloat] = None

    qtv_10kl: Optional[FlexFloat] = None
    received_250kva: Optional[FlexFloat] = None

    fe_01: Optional[FlexFloat] = None
    fe_02: Optional[FlexFloat] = None
    fe_03: Optional[FlexFloat] = None

    sv_08: Optional[FlexFloat] = None
    ip: Optional[FlexFloat] = None
    sv_09: Optional[FlexFloat] = None
    sv_10: Optional[FlexFloat] = None

    final_dip: Optional[FlexFloat] = None
    final_qty: Optional[FlexFloat] = None

    # Audit Fields
    created_at: Optional[FlexDatetime] = None
    created_by: Optional[int] = None
    updated_at: Optional[FlexDatetime] = None
    updated_by: Optional[int] = None

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)


class Tank10KLFfeEntryCreate(Tank10KLFfeEntryBase):
    pass


class Tank10KLFfeEntryUpdate(Tank10KLFfeEntryBase):
    pass


class Tank10KLFfeEntryResponse(Tank10KLFfeEntryBase):
    tank_ffe_entry_id: int
    created_by_name: Optional[str] = None
    updated_by_name: Optional[str] = None
