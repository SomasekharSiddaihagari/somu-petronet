import datetime
from sqlalchemy import (
    Column, DateTime, Integer, String, Date, Time, Text, Boolean, ForeignKey
)
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class HSEIncidentInvestigationTeam(Base):
    __tablename__ = "hse_incident_investigation_team"

    invest_team_id = Column(Integer, primary_key=True, autoincrement=True)

    incident_id = Column(
        Integer,
        ForeignKey(
            "hse_incident_investigation_master.hiim_id",
            ondelete="CASCADE"
        ),
        nullable=False
    )

    sl_no = Column(Integer, nullable=True)
    name = Column(String(150), nullable=True)
    designation = Column(String(150), nullable=True)
    role = Column(String(50), nullable=True)  # Leader / Member
    is_acknowledged = Column(Boolean, nullable=True)
    user_id = Column(Integer, nullable=True)

    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)



    
