from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
 
Base = declarative_base()
 
 
class IncidentCauseAnalysisHistory(Base):
    __tablename__ = "incident_cause_analysis_history"
 
    # =========================
    # PRIMARY KEY
    # =========================
    history_id = Column(Integer, primary_key=True, autoincrement=True)
    cause_id= Column(
        Integer, nullable=True
    )
    # =========================
    # FK TO INCIDENT REPORT
    # =========================
    incident_id = Column(Integer, nullable=True)  # FK to incident_report.incident_id
 
    # =================================================
    # 22. CAUSE OF THE INCIDENT (MAX 2)
    # =================================================
    cause_deviation_from_procedure = Column(Boolean, nullable=True)
    cause_lack_of_job_knowledge = Column(Boolean, nullable=True)
 
    cause_lack_of_supervision = Column(Boolean, nullable=True)
    cause_improper_inspection = Column(Boolean, nullable=True)
 
    cause_improper_maintenance = Column(Boolean, nullable=True)  # Mech / Elec / Inst
    cause_improper_material_handling = Column(Boolean, nullable=True)
 
    cause_negligent_driving = Column(Boolean, nullable=True)
    cause_not_using_ppe = Column(Boolean, nullable=True)
 
    cause_equipment_failure = Column(Boolean, nullable=True)
    cause_poor_design_layout = Column(Boolean, nullable=True)
 
    cause_inadequate_facility = Column(Boolean, nullable=True)
    cause_poor_house_keeping = Column(Boolean, nullable=True)
 
    cause_natural_calamity = Column(Boolean, nullable=True)
    cause_pilferage_sabotage = Column(Boolean, nullable=True)
 
    # =================================================
    # 23. CAUSE OF LEAKAGE - OIL, GAS OR CHEMICAL (ONE)
    # =================================================
    leak_weld_from_equipment_lines = Column(Boolean, nullable=True)
    leak_from_flange_gland = Column(Boolean, nullable=True)
 
    leak_from_rotary_equipment = Column(Boolean, nullable=True)
    leak_metallurgical_failure = Column(Boolean, nullable=True)
 
    leak_due_to_improper_operation = Column(Boolean, nullable=True)
    leak_due_to_improper_maintenance = Column(Boolean, nullable=True)
 
    leak_normal_operation_venting_draining = Column(Boolean, nullable=True)
    leak_any_other = Column(Boolean, nullable=True)
    leak_any_other_description = Column(Text, nullable=True)
 
    # =================================================
    # 24. CAUSE OF IGNITION LEADING TO FIRE (ONE)
    # =================================================
    ignition_near_to_hot_work = Column(Boolean, nullable=True)
    ignition_near_to_furnace_flare = Column(Boolean, nullable=True)
 
    ignition_auto_ignition = Column(Boolean, nullable=True)
    ignition_loose_electrical_connection = Column(Boolean, nullable=True)
 
    ignition_near_to_hot_surface = Column(Boolean, nullable=True)
    ignition_static_electricity = Column(Boolean, nullable=True)
 
    ignition_hammering_fall_of_object = Column(Boolean, nullable=True)
    ignition_heat_due_to_friction = Column(Boolean, nullable=True)
 
    ignition_lightning = Column(Boolean, nullable=True)
    ignition_any_other_pyrophoric = Column(Boolean, nullable=True)
    ignition_any_other_pyrophoric_description = Column(Text, nullable=True)
 
    # =========================
    # SYSTEM FIELDS
    # =========================
    status = Column(String(50), nullable=True)     # Draft / Submitted
    created_by = Column(String(100), nullable=True)
    updated_by = Column(String(100), nullable=True)
 
    created_at = Column(DateTime, default=datetime.utcnow, nullable=True)
    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=True
    )