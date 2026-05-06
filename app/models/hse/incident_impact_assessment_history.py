from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
 
Base = declarative_base()
 
 
class IncidentImpactAssessmentHistory(Base):
    __tablename__ = "incident_impact_assessment_history"
 
    # =========================
    # PRIMARY KEY
    # =========================
    history_id = Column(Integer, primary_key=True, autoincrement=True)
    impact_id = Column(
        Integer, nullable=True
    )
    # =========================
    # FK TO INCIDENT REPORT
    # =========================
    incident_id = Column(Integer, nullable=True)   # FK to incident_report.incident_id
 
    # =========================
    # CASUALTIES & INJURIES
    # =========================
    fatalities_employees = Column(Integer, nullable=True)
    fatalities_contractor = Column(Integer, nullable=True)
    fatalities_others = Column(Integer, nullable=True)
 
    injuries_employees = Column(Integer, nullable=True)
    injuries_contractor = Column(Integer, nullable=True)
    injuries_others = Column(Integer, nullable=True)
 
    man_hours_lost_employees = Column(Integer, nullable=True)
    man_hours_lost_contractor = Column(Integer, nullable=True)
    man_hours_lost_others = Column(Integer, nullable=True)
 
    # =========================
    # FINANCIAL IMPACT
    # =========================
    direct_loss_details = Column(Text, nullable=True)
    indirect_loss_details = Column(Text, nullable=True)
 
    # =========================
    # FACILITY STATUS
    # =========================
    facility_status = Column(String(50), nullable=True)
    # Construction / Commissioning / Operation / Shutting down /
    # Turn around / Maintenance / Start up / Any other
 
    # =========================
    # INCIDENT DESCRIPTION
    # =========================
    brief_incident_description = Column(Text, nullable=True)
 
    similar_incident_past = Column(Text, nullable=True)
 
    # =========================
    # SYSTEM FIELDS
    # =========================
    status = Column(String(50), nullable=True)    # Draft / Submitted / etc
    created_by = Column(String(100), nullable=True)
    updated_by = Column(String(100), nullable=True)
 
    created_at = Column(DateTime, default=datetime.utcnow, nullable=True)
    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=True
    )