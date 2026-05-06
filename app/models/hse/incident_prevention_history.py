from sqlalchemy import Column, Integer, String, Boolean, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
 
Base = declarative_base()
 
 
class IncidentPreventionHistory(Base):
    __tablename__ = "incident_prevention_history"
 
    # =========================
    # PRIMARY / FK
    # =========================
    history_id = Column(Integer, primary_key=True, autoincrement=True)
    ip_id = Column(Integer, nullable=True)
    incident_id = Column(Integer, nullable=True)
 
    # =========================
    # COMMON (MAJOR + MINOR)
    # =========================
    category = Column(String(50), nullable=True)  # Major / Minor
    status = Column(String(50), nullable=True)
 
    was_incident_avoidable = Column(Boolean, nullable=True)
 
    avoid_better_supervision = Column(Boolean, nullable=True)
    avoid_imparting_training = Column(Boolean, nullable=True)
    avoid_work_permit_system = Column(Boolean, nullable=True)
    avoid_better_equipment = Column(Boolean, nullable=True)
    avoid_maintenance_procedure = Column(Boolean, nullable=True)
    avoid_other_information = Column(Boolean, nullable=True)
 
    avoid_operating_procedure = Column(Boolean, nullable=True)
    avoid_proper_planning_time = Column(Boolean, nullable=True)
    avoid_ppe = Column(Boolean, nullable=True)
    avoid_management_control = Column(Boolean, nullable=True)
    avoid_inspection_testing = Column(Boolean, nullable=True)
 
    # =========================
    # MINOR INCIDENT CHUNK
    # =========================
    minor_prepared_by_name = Column(String(150), nullable=True)
    minor_prepared_by_designation = Column(String(150), nullable=True)
 
    minor_recommendations = Column(Text, nullable=True)
    minor_engineer_corrective_actions_taken = Column(Text, nullable=True)
    minor_prepared_by_corrective_action = Column(Text, nullable=True)
    minor_corrective_actions = Column(Text, nullable=True)
    
    minor_prepared_by_remarks = Column(Text, nullable=True)
    minor_preventive_action_taken = Column(Text, nullable=True)
 

    minor_allotted_engineer_name = Column(String(150), nullable=True)
    minor_allotted_engineer_designation = Column(String(150), nullable=True)
 
    minor_approved_by_name = Column(String(150), nullable=True)
    minor_approved_by_station_incharge = Column(String(150), nullable=True)
    minor_approved_by_remarks = Column(Text, nullable=True)
 
    minor_evidence_document_path = Column(String(255), nullable=True)
 
    # =========================
    # MAJOR INCIDENT CHUNK
    # =========================
    major_prepared_by_name = Column(String(150), nullable=True)
    major_prepared_by_designation = Column(String(150), nullable=True)
 
    major_immediate_actions_taken = Column(Text, nullable=True)
    major_recommendations = Column(Text, nullable=True)
 
 
    major_prepared_by_remarks_si= Column(Text, nullable=True)
    major_hse_head_remarks = Column(Text, nullable=True)
    
    major_evidence_document_path = Column(String(255), nullable=True)

    minor_evidence_documents_multi = Column(Text, nullable=True)
    major_evidence_documents_multi = Column(Text, nullable=True)
 
    # =========================
    # SYSTEM
    # =========================
    created_by = Column(String(100), nullable=True)
    updated_by = Column(String(100), nullable=True)
 
    created_at = Column(DateTime, default=datetime.utcnow, nullable=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=True)
