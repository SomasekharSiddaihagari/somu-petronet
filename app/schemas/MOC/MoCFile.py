from typing import Optional
from pydantic import BaseModel
from datetime import datetime

class FileBase(BaseModel):
    moc_request_id: int
    moc_request_no: str

class FileOut(BaseModel):
    id: int
    filename: str
    filepath: str
    model_id: int
    model_name: str
    uploaded_at: datetime
    download_url: Optional[str] = None

    class Config:
        orm_mode = True