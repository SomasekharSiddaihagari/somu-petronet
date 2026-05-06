from sqlalchemy import Column, Integer, String, Date, Time, Boolean, Text
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
 
Base = declarative_base()
 
 
class IncidentReportHistory(Base):
    __tablename__ = "incident_report_history"
 
    # =========================
    # PRIMARY KEY
    # =========================
    history_id = Column(Integer, primary_key=True, autoincrement=True)
    incident_id = Column(Integer, nullable=True)
 
    # =========================
    # GENERAL INFORMATION
    # =========================
    organisation = Column(String(150), nullable=True)          # Petronet
    category = Column(String(50), nullable=True)               # Major/Minor
    sector = Column(String(150), nullable=True)
 
    location = Column(String(255), nullable=True)
    incident_no_during_year = Column(String(100), nullable=True)
 
    date_of_incident = Column(Date, nullable=True)
    time_of_incident = Column(Time, nullable=True)
 
    incident_type = Column(String(100), nullable=True)
    fire_incident = Column(String(100), nullable=True)
 
    report_type = Column(String(50), nullable=True)            # Preliminary / Final
    duration_of_fire = Column(String(50), nullable=True)       # Hrs / Min / NA
 
    # =========================
    # INCIDENT CLASSIFICATION
    # =========================
    loss_of_life_injury = Column(Boolean, nullable=True)
    electrocution = Column(Boolean, nullable=True)
    slip_trip = Column(Boolean, nullable=True)
    fire = Column(Boolean, nullable=True)
    fall_from_height = Column(Boolean, nullable=True)
    leak_spill = Column(Boolean, nullable=True)
    explosion = Column(Boolean, nullable=True)
    inhalation_of_gas = Column(Boolean, nullable=True)
    blowout = Column(Boolean, nullable=True)
    driving = Column(Boolean, nullable=True)
 
    others = Column(Boolean, nullable=True)
    others_text = Column(String(255), nullable=True)
 
    # =========================
    # LOCATION DETAILS
    # =========================
    incident_location_detail = Column(Text, nullable=True)
    # (Name of Plant / Unit / Area / Facility / Tank farm / Gantry / Road / Parking etc)
 
    # =========================
    # PLANT SHUTDOWN
    # =========================
    plant_shutdown = Column(Boolean, nullable=True)   # Yes / No
 
    # =========================
    # SYSTEM FIELDS
    # =========================
    status = Column(String(50), nullable=True)        # Draft / Submitted / etc
    created_by = Column(String(100), nullable=True)
    updated_by = Column(String(100), nullable=True)
 
    created_at = Column(Date, default=datetime.utcnow, nullable=True)
    updated_at = Column(
        Date,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=True
    )