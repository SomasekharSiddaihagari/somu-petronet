from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class WorkAtHeightToolboxTalkParticipantSchema(BaseModel):
    whttp_id: int

    toolbox_talk_id: Optional[int]

    participant_name: Optional[str]
    participant_signature: Optional[str]

    created_at: Optional[datetime]

    class Config:
        orm_mode = True
