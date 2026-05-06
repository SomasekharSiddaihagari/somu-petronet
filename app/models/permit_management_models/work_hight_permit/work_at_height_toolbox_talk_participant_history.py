from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
 
Base = declarative_base()
 
class WorkAtHeightToolboxTalkParticipant(Base):
    __tablename__ = "work_at_height_toolbox_talk_participant_history"

    history_id = Column(Integer, primary_key=True, autoincrement=True)
    whttp_id = Column(Integer, nullable=True)

    # ---------------------------------
    # FK TO TOOL BOX TALK
    # ---------------------------------
    toolbox_talk_id = Column(
        Integer,
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