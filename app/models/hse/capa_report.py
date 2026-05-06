from sqlalchemy import (
    Column, Integer, String, Text, Date, DateTime, ForeignKey
)
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime
# from database import Base
Base = declarative_base()
 
class CapaReport(Base):
    __tablename__ = "capa_report"
 
    capa_report_id = Column(Integer, primary_key=True, autoincrement=True)
 
    # 🔗 Incident Link
    incident_id = Column(Integer, ForeignKey("incident_report.incident_id"), nullable=False)
 
    # Header Info (top blue bar)
    format_no = Column(String(50), nullable=True)
    revision_date = Column(String(50), nullable=True)
    report_no = Column(String(100), nullable=True)
 
    # CAPA Study Details
    department = Column(String(150), nullable=True)
    start_date = Column(Date, nullable=True)
    team_or_capa_study = Column(String(255), nullable=True)
    planned_completion_date = Column(Date, nullable=True)
    reference_no = Column(String(100), nullable=True)
 
    # Problem Statement
    problem_description = Column(Text, nullable=True)
 
    # Correction (Immediate Relief)
    correction_action = Column(Text, nullable=True)
    correction_target_date = Column(Date, nullable=True)
    correction_actual_date = Column(Date, nullable=True)
 
    # Root Cause Analysis
    root_cause_analysis = Column(Text, nullable=True)
 
    # Corrective Action
    corrective_action = Column(Text, nullable=True)
    corrective_target_date = Column(Date, nullable=True)
    corrective_actual_date = Column(Date, nullable=True)
 
    # Preventive Action
    preventive_action = Column(Text, nullable=True)
    preventive_target_date = Column(Date, nullable=True)
    preventive_actual_date = Column(Date, nullable=True)
 
    # 📎 Attach Document / Evidence (MAIN TABLE)
    evidence_file_name = Column(Text, nullable=True)
    evidence_file_path = Column(Text, nullable=True)
    evidence_file_type = Column(Text, nullable=True)
    evidence_uploaded_at = Column(DateTime, nullable=True)
 
    # Authorization
    prepared_by_name = Column(String(150), nullable=True)
    prepared_by_designation = Column(String(150), nullable=True)
    hse_head_id = Column(Integer, nullable=True)
    approved_by_name = Column(String(150), nullable=True)
    approved_by_designation = Column(String(150), nullable=True)
    created_by = Column(Integer, nullable=True)
    updated_by = Column(Integer, nullable=True)
    remarks = Column(Text, nullable=True)
 
    # Workflow
    status = Column(String(50), default="Draft")  
    # Draft / Submitted / Approved / Sent Back
 
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)
 
