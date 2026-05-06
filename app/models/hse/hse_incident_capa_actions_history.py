from sqlalchemy import Column, ForeignKey, ForeignKey, Integer, String, Date, Time, Boolean, Text
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
 
Base = declarative_base()
 
class HSEIncidentCAPAActionsHistory(Base):
    __tablename__ = "hse_incident_capa_actions_history"
 
    historyid = Column(Integer, primary_key=True, autoincrement=True)
 
    capa_id = Column(
        Integer,
        nullable=True
    )
    incident_id = Column(
        Integer,
        nullable=True
    )
 
    action = Column(Text, nullable=True)
    action_type = Column(String(20), nullable=True)  # Corrective / Preventive
    target_date = Column(Date, nullable=True)