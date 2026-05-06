from pydantic import BaseModel
from typing import Optional
from datetime import date


class DiscussionCreate(BaseModel):
    scmm_id: int
    row_no: int
    description_of_discussion: Optional[str] = None
    issues_discussed: Optional[str] = None
    action_taken: Optional[str] = None
    completed_on: Optional[date] = None
    action_by: Optional[str] = None
    target_date: Optional[date] = None
    user_id: Optional[int] = None


class DiscussionUpdate(BaseModel):
    row_no: Optional[int] = None
    description_of_discussion: Optional[str] = None
    issues_discussed: Optional[str] = None
    action_taken: Optional[str] = None
    completed_on: Optional[date] = None
    action_by: Optional[str] = None
    target_date: Optional[date] = None
    user_id: Optional[int] = None


class DiscussionResponse(BaseModel):
    id: int
    scmm_id: int
    row_no: int
    description_of_discussion: Optional[str]
    issues_discussed: Optional[str]
    action_taken: Optional[str]
    completed_on: Optional[date]
    action_by: Optional[str]
    user_id: Optional[int]
    target_date: Optional[date]

    class Config:
        from_attributes = True