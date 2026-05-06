import datetime
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Date, Time, Text, Boolean
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
Base = declarative_base()
 
 
class HSEIncidentInvestigationMaster(Base):
    __tablename__ = "hse_incident_investigation_master"
 
    hiim_id = Column(Integer, primary_key=True, autoincrement=True)
    incident_id = Column(Integer, ForeignKey("incident_report.incident_id"), nullable=False)
    # =========================
    # STEP 1 — GENERAL INFO
    # =========================
    incident_reference_no = Column(String(100), nullable=True)
    report_number = Column(String(100), nullable=True)
 
    incident_date = Column(Date, nullable=True)
    incident_time = Column(Time, nullable=True)
    reporting_date = Column(Date, nullable=True)
 
    location_details = Column(String(255), nullable=True)
    pipeline_name_section = Column(String(255), nullable=True)
    reported_by = Column(String(150), nullable=True)
 
    # Incident Type
    is_leak = Column(Boolean, nullable=True)
    is_spill = Column(Boolean, nullable=True)
    is_fire = Column(Boolean, nullable=True)
    is_explosion = Column(Boolean, nullable=True)
    is_injury = Column(Boolean, nullable=True)
    is_near_miss = Column(Boolean, nullable=True)
    is_other = Column(Boolean, nullable=True)
 
    # Severity
    severity_major = Column(Boolean, nullable=True)
    severity_minor = Column(Boolean, nullable=True)
    severity_near_miss = Column(Boolean, nullable=True)
    severity_unsafe_act = Column(Boolean, nullable=True)
    severity_unsafe_condition = Column(Boolean, nullable=True)
    severity_high_potential_near_miss = Column(Boolean, nullable=True)
 
    # Impact Assessment
    impact_on_people = Column(Text, nullable=True)
    impact_on_asset = Column(Text, nullable=True)
    environmental_impact = Column(Text, nullable=True)
    business_interruption = Column(Text, nullable=True)
 
    # =========================
    # STEP 2
    # =========================
    immediate_action_taken = Column(Text, nullable=True)
    statutory_management_intimation = Column(Text, nullable=True)
 
    # =========================
    # STEP 3
    # =========================
    incident_description = Column(Text, nullable=True)
    site_observations_evidence = Column(Text, nullable=True)
 
    immediate_causes = Column(Text, nullable=True)
    underlying_causes = Column(Text, nullable=True)
    root_causes = Column(Text, nullable=True)
 
    # RCA Tool Selected
    rca_tool_used = Column(String(50), nullable=True)  
    # values: '5-Why', 'Fishbone', 'FTA'
 
    # =========================
    # STEP 4
    # =========================
    learning_recommendations = Column(Text, nullable=True)
    verification_closure = Column(Text, nullable=True)
    status = Column(String(50), nullable=True)   # <-- added
    annexure_files = Column(Text, nullable=True)
 
    remarks_md = Column(Text, nullable=True)
    remarks_hse_head = Column(Text, nullable=True)
    remarks_station_incharge = Column(Text, nullable=True)
 
    allotted_to_name = Column(Integer, nullable=True)
    allotted_to_designation = Column(String(150), nullable=True)
 
    created_by = Column(String(100), nullable=True)
    updated_by = Column(String(100), nullable=True)
 
    created_at = Column(DateTime, default=datetime.utcnow, nullable=True)
    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=True
    )