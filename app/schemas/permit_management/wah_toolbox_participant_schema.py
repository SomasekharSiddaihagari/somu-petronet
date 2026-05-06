from pydantic import BaseModel
from typing import Optional


class WorkAtHeightToolboxTalkParticipantBase(BaseModel):
    toolbox_talk_id: Optional[int] = None
    participant_name: Optional[str] = None
    participant_signature: Optional[str] = None


class WorkAtHeightToolboxTalkParticipantCreate(
    WorkAtHeightToolboxTalkParticipantBase
):
    pass


class WorkAtHeightToolboxTalkParticipantUpdate(
    WorkAtHeightToolboxTalkParticipantBase
):
    pass
