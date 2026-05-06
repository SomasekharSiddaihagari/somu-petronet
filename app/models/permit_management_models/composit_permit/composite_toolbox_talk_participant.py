from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
 
Base = declarative_base()
 
class CompositeToolboxTalkParticipant(Base):
    __tablename__ = "composite_toolbox_talk_participant"
 
    cttp_id = Column(Integer, primary_key=True, autoincrement=True)
 
    # ---------------------------------
    # FK TO TOOL BOX TALK
    # ---------------------------------
    toolbox_talk_id = Column(
        Integer,
        ForeignKey("composite_toolbox_talk.ctt_id"),
        nullable=True
    )
 
    # =================================================
    # PARTICIPANT DETAILS
    # =================================================
    participant_name = Column(String(150), nullable=True)
    participant_signature = Column(String(255), nullable=True)
 
    # =================================================
    # SYSTEM
    # =================================================
    created_at = Column(DateTime, default=datetime.utcnow, nullable=True)