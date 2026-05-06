# app/schemas/hse/capa_document_change_schema.py
from pydantic import BaseModel
from typing import Optional


class CapaDocumentChangeCreate(BaseModel):
    capa_id: int
    document_code: Optional[str] = None
    changes_in_brief: Optional[str] = None


class CapaDocumentChangeUpdate(BaseModel):
    document_code: Optional[str] = None
    changes_in_brief: Optional[str] = None
