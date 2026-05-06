from sqlalchemy import Column, Date, Integer, String, Boolean, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
 
Base = declarative_base()
 
 
class IncidentPrevention(Base):
    __tablename__ = "incident_prevention"
 
    # =========================
    # PRIMARY / FK
    # =========================
    ip_id = Column(Integer, primary_key=True, autoincrement=True)
    incident_id = Column(Integer, nullable=True)  # FK to incident_report.incident_id
 
    # =========================
    # COMMON (MAJOR + MINOR)
    # =========================
    category = Column(String(50), nullable=True)  # Major / Minor
    status = Column(String(50), nullable=True)
 
    # 25. AVOIDABILITY
    was_incident_avoidable = Column(Boolean, nullable=True)
 
    # 26. COULD HAVE BEEN AVOIDED BY (COMMON)
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
    # Prepared By (Minor)
    minor_prepared_by_name = Column(String(150), nullable=True)
    minor_prepared_by_designation = Column(String(150), nullable=True)
 
    # Recommendations & Actions (Minor)
    minor_recommendations = Column(Text, nullable=True)
    minor_engineer_corrective_actions_taken = Column(Text, nullable=True)
    minor_prepared_by_corrective_action = Column(Text, nullable=True)
    minor_corrective_actions = Column(Text, nullable=True)
        # Remarks (Minor)
    minor_prepared_by_remarks = Column(Text, nullable=True)
 
    minor_preventive_action_taken = Column(Text, nullable=True)
 

    # Responsible Engineer (Minor)
    minor_allotted_responsible_id = Column(Integer, nullable=True)  
    minor_alloted_engineer_name = Column(String(150), nullable=True)
 
    # Approval (Minor)
    minor_approved_by_name = Column(String(150), nullable=True)
    minor_approved_by_station_incharge = Column(String(150), nullable=True)
    minor_approved_by_remarks = Column(Text, nullable=True)
 
    # Evidence (Minor)
    minor_evidence_document_path = Column(String(255), nullable=True)
 
    # =========================
    # MAJOR INCIDENT CHUNK
    # =========================
    # Prepared By (Major)
    major_prepared_by_name = Column(String(150), nullable=True)
    major_prepared_by_designation = Column(String(150), nullable=True)
 
    # Immediate Actions & Recommendations (Major)
    major_immediate_actions_taken = Column(Text, nullable=True)
    major_recommendations = Column(Text, nullable=True)
 

    # Remarks (Major / Management)
    major_prepared_by_remarks_si = Column(Text, nullable=True)
    major_hse_head_remarks = Column(Text, nullable=True)
    
    # Evidence (Major)
    major_evidence_document_path = Column(String(255), nullable=True)

    minor_evidence_documents_multi = Column(Text, nullable=True)
    major_evidence_documents_multi = Column(Text, nullable=True)
 
    # =========================
    # SYSTEM
    # =========================
    created_by = Column(Integer, nullable=True)
    updated_by = Column(Integer, nullable=True)
 
    created_at = Column(
    DateTime,
    default=datetime.utcnow,     # ORM side   # DB side (🔥 important)
    nullable=True
    )
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=True)


     # SIC
    minor_sic_name = Column(String(150), nullable=True)
    minor_sic_updated_date = Column(Date, nullable=True)

    # Allotted Engineer
    minor_allotted_engineer_id = Column(Integer, nullable=True) 
    minor_alloted_engineer_name = Column(String(150), nullable=True)
    minor_alloted_eng_updated_date = Column(Date, nullable=True)

    # Final Approval
    minor_final_approve_name = Column(String(150), nullable=True)
    minor_final_approved_date = Column(Date, nullable=True)






    # =====================================================
    # 🔥 MAJOR WORKFLOW AUDIT FIELDS
    # =====================================================
    
    # 0. Team Leader
    major_team_leader_by = Column(String(150), nullable=True)
    major_team_leader_date = Column(Date, nullable=True)
    
    # 1. Team Acknowledgement
    major_team_acknowledged_by = Column(String(150), nullable=True)
    major_team_acknowledged_date = Column(Date, nullable=True)
    
    # 2. Investigation Report Submitted
    major_report_filled_by = Column(String(150), nullable=True)
    major_report_filled_date = Column(Date, nullable=True)
    
    # 3. Team Review
    major_investigation_ack_by = Column(String(150), nullable=True)
    major_investigation_ack_date = Column(Date, nullable=True)
    
    # 🔥 NEW — Safety Officer
    major_safety_officer_by = Column(String(150), nullable=True)
    major_safety_officer_date = Column(Date, nullable=True)
    
    # 4. MD Review
    major_md_review_by = Column(String(150), nullable=True)
    major_md_review_date = Column(Date, nullable=True)
    
    # 5. HSE Head Review
    major_hse_review_by = Column(String(150), nullable=True)
    major_hse_review_date = Column(Date, nullable=True)
    
    # 6. CAPA Filled
    major_capa_filled_by = Column(String(150), nullable=True)
    major_capa_filled_date = Column(Date, nullable=True)
    
    # 7. HSE Head CAPA Review
    major_hse_capa_review_by = Column(String(150), nullable=True)
    major_hse_capa_review_date = Column(Date, nullable=True)
    
    # 8. Final Closure
    major_closure_by = Column(String(150), nullable=True)
    major_closure_date = Column(Date, nullable=True)




