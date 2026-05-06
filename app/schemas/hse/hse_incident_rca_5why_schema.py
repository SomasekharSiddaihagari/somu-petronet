from pydantic import BaseModel, Field
from typing import Optional, List
 
 
# =========================
# CREATE
# =========================
class RCA5WhyCreate(BaseModel):
    hiim_id: int = Field(..., description="Investigation master ID")
 
    why1: Optional[str] = None
    why2: Optional[str] = None
    why3: Optional[str] = None
    why4: Optional[str] = None
    why5_root_cause: Optional[str] = None
    problem_statement: Optional[str] = None
    
 
 
# =========================
# UPDATE
# =========================
class RCA5WhyUpdate(BaseModel):
    why1: Optional[str] = None
    why2: Optional[str] = None
    why3: Optional[str] = None
    why4: Optional[str] = None
    why5_root_cause: Optional[str] = None
    problem_statement: Optional[str] = None
 
 
# =========================
# RESPONSE (SINGLE)
# =========================
class RCA5WhyResponse(BaseModel):
    rca_id: int
    hiim_id: int
 
    why1: Optional[str]
    why2: Optional[str]
    why3: Optional[str]
    why4: Optional[str]
    why5_root_cause: Optional[str]
    problem_statement: Optional[str] 
 
 
# =========================
# RESPONSE (LIST)
# =========================
class RCA5WhyListResponse(BaseModel):
    count: int
    data: List[RCA5WhyResponse]
 
 