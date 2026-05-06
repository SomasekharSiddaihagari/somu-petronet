from pydantic import BaseModel, field_validator
from datetime import date

from pydantic import BaseModel, field_validator
from datetime import date

class DeclarationSettingsBase(BaseModel):
    declaration_type: str
    opening_date: date | None = None
    closing_date: date | None = None
    is_active: bool = False

    @field_validator("opening_date", "closing_date", mode="before")
    def empty_string_to_none(cls, v):
        if v is None:
            return None

        v = str(v).strip()

        if v == "" or v.lower() in ("none", "null"):
            return None

        return v


class DeclarationSettingsCreate(DeclarationSettingsBase):
    pass


class DeclarationSettingsUpdate(BaseModel):
    declaration_type: str | None = None
    opening_date: date | None = None
    closing_date: date | None = None
    is_active: bool | None = None


class DeclarationSettingsOut(DeclarationSettingsBase):
    dec_id: int

    class Config:
        from_attributes = True
