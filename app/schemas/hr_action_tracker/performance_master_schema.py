from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, ConfigDict
 
class EmployeePerformanceDocumentResponse(BaseModel):
    id: int
    performance_id: int
    file_name: str
    file_path: str
    uploaded_at: datetime
    acknowledgement: Optional[bool] = None
    is_deleted: Optional[bool] = None

    model_config = ConfigDict(from_attributes=True)
class EmployeeAppraisalItem(BaseModel):
    user_id:  Optional[int] = None
    appraisal_start_date: datetime
    appraisal_end_date: datetime
    annual_appraisal_rating:  Optional[str] = None
    annual_rating_score:  Optional[str] = None

class EmployeeAppraisalRequest(BaseModel):
    appraisals: List[EmployeeAppraisalItem]