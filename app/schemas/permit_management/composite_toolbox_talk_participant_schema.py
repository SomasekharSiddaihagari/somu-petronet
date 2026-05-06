from pydantic import BaseModel
from typing import Optional


class CompositeToolboxTalkParticipantBase(BaseModel):
    toolbox_talk_id: Optional[int] = None
    participant_name: Optional[str] = None
    participant_signature: Optional[str] = None


class CompositeToolboxTalkParticipantCreate(CompositeToolboxTalkParticipantBase):
    pass


class CompositeToolboxTalkParticipantUpdate(CompositeToolboxTalkParticipantBase):
    pass
