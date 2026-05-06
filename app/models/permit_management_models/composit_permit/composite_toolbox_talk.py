from sqlalchemy import Column, Integer, String, Date, Time, DateTime, ForeignKey, Text
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
 
Base = declarative_base()
 
class CompositeToolboxTalk(Base):
    __tablename__ = "composite_toolbox_talk"
 
    ctt_id = Column(Integer, primary_key=True, autoincrement=True)
 
    # ---------------------------------
    # FK TO COMPOSITE WORK PERMIT
    # ---------------------------------
    composite_work_permit_id = Column(
        Integer,
        ForeignKey("composite_work_permit.cwp_id"),
        nullable=True
    )
 
    # =================================================
    # WORK INFORMATION & PERSONNEL INFORMATION
    # =================================================
    cross_reference_of_other_permit = Column(String(150), nullable=True)
 
    work_clearance_time = Column(Time, nullable=True)
    work_clearance_date = Column(Date, nullable=True)
 
    contractor_engineer_name = Column(String(150), nullable=True)
    work_installation_unit_facility_name = Column(String(255), nullable=True)
 
    tbt_delivered_by = Column(String(150), nullable=True)
    contract_supervisor_name = Column(String(150), nullable=True)
 
    # =================================================
    # TOPICS / ISSUES DISCUSSED
    # =================================================
    topics_issues_discussed = Column(Text, nullable=True)
 
    # =================================================
    # OTHER POINTS / ISSUES RAISED BY PARTICIPANTS
    # =================================================
    other_points_raised = Column(Text, nullable=True)
    status = Column(String(50), nullable=True)
 
    # =================================================
    # SYSTEM
    # =================================================
    created_by = Column(String(100), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=True)
    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=True
    )