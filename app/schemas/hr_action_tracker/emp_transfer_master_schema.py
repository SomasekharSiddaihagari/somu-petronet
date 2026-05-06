from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional, List

# from sqlalchemy import text
 
class TransferDocumentResponse(BaseModel):
    id: int
    transfer_id: int
    file_name: str
    file_path: str
    uploaded_at: datetime
    acknowledgement: Optional[bool] = None
    is_deleted: Optional[bool] = False
 
    model_config = ConfigDict(from_attributes=True)
 
class EmployeeTransferCreate(BaseModel):
    user_id: int
    current_station: int
    new_station: int
    effective_date: datetime
    remarks: Optional[str] = None
    created_by: int
    office_order_number: Optional[str] = None
 
class EmployeeTransferUpdate(BaseModel):
    current_station: Optional[int] = None
    new_station: Optional[int] = None
    effective_date: Optional[datetime] = None
    remarks: Optional[str] = None
    acknowledgement: Optional[bool] = None
    is_deleted: Optional[bool] = None
    office_order_number: Optional[str] = None
 
class EmployeeTransferResponse(BaseModel):
    id: int
    user_id: int
    current_station: int
    current_station_name: str
    new_station: int
    new_station_name: str
    effective_date: datetime
    remarks: Optional[str] = None
    acknowledgement: Optional[bool] = None
    is_deleted: Optional[bool] = False
    created_at: datetime
    created_by: Optional[int] = None
    office_order_number: Optional[str] = None
    comments: Optional[str] = None
    office_order_number: Optional[str] = None
    actual_joining_date: Optional[datetime] = None
    attachments: List[TransferDocumentResponse] = []
 
    model_config = ConfigDict(from_attributes=True)

class AcknowledgeTransferRequest(BaseModel):
    acknowledgement: bool = True
    comments: str | None = None
    actual_joining_date: Optional[datetime] = None
 