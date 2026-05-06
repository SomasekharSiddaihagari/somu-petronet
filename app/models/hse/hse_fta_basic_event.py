from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base


class FTABasicEvent(Base):

    __tablename__ = "fta_basic_event"
 
    fte_basic_id = Column(Integer, primary_key=True, autoincrement=True)

    intermediate_event_id = Column(

        Integer, ForeignKey("fta_intermediate_event.intermediate_event_id"), nullable=False

    )
    e1_b1=Column(String(500), nullable=True)
    e1_b2=Column(String(500), nullable=True)
    e2_b1=Column(String(500), nullable=True)
    e2_b2=Column(String(500), nullable=True)
    
    

    created_at = Column(DateTime, default=datetime.utcnow)
 
    

 