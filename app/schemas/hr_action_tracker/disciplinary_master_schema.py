from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional, List
 
class DisciplinaryIncidentDocumentResponse(BaseModel):
    id: int
    disciplinary_id: int
    file_name: str
    file_path: str
    uploaded_at: datetime
    acknowledgement: Optional[bool] = None
    is_deleted: Optional[bool] = None

    model_config = ConfigDict(from_attributes=True)


class DisciplinaryIncidentCreate(BaseModel):
    user_id: int
    incident_date: datetime
    severity: str
    incident_details: str
    investigation_finding: Optional[str] = None
    measures_taken: Optional[str] = None
    enable_suspension: Optional[bool] = False
    enable_termination: Optional[bool] = False
    suspension_effective_from: Optional[datetime] = None
    suspension_effective_to: Optional[datetime] = None
    termination_effective_from: Optional[datetime] = None
    outcome: Optional[str] = None
    created_by: Optional[int] = None
 
class DisciplinaryIncidentResponse(BaseModel):
    disciplinary_id: int
    user_id: int
    incident_date: datetime
    severity: str
    incident_details: str
    investigation_finding: Optional[str] = None
    measures_taken: Optional[str] = None
    enable_suspension: bool
    enable_termination: bool
    suspension_effective_from: Optional[datetime] = None
    suspension_effective_to: Optional[datetime] = None
    termination_effective_from: Optional[datetime] = None
    outcome: Optional[str] = None
    acknowledgement: Optional[bool] = None
    is_deleted: Optional[bool] = None
    created_at: datetime
    created_by: Optional[int] = None
    comments: Optional[str] = None
    attachments: List[DisciplinaryIncidentDocumentResponse] = []
    model_config = ConfigDict(from_attributes=True)

class AcknowledgeDisciplinaryRequest(BaseModel):
    acknowledgement: bool = True
    comments: str | None = None