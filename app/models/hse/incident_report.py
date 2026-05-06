from sqlalchemy import Column, Integer, String, Date, Time, Boolean, Text
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
 
Base = declarative_base()
 
 
class IncidentReport(Base):
    __tablename__ = "incident_report"
 
    # =========================
    # PRIMARY KEY
    # =========================
    incident_id = Column(Integer, primary_key=True, autoincrement=True)
 
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




     # SIC
    minor_sic_name = Column(String(150), nullable=True)
    minor_sic_updated_date = Column(Date, nullable=True)

    # Allotted Engineer
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


    # =========================
    # SYSTEM FIELDS
    # =========================
    status = Column(String(50), nullable=True)        # Draft / Submitted / etc
    created_by = Column(String(100), nullable=True)
    updated_by = Column(String(100), nullable=True)


    created_at = Column(
        Date,
        default=datetime.utcnow,
        nullable=True
    )
    updated_at = Column(
        Date,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=True
    )