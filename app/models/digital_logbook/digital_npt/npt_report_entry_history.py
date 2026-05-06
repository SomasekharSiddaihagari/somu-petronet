from sqlalchemy import Column, Integer, String, Date, Time, DateTime, ForeignKey, Text, func
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
 
Base = declarative_base()
 
class NPTReportEntry(Base):
    __tablename__ = "npt_report_entry_history"

    history_id = Column(Integer, primary_key=True, autoincrement=True)
    npe_id = Column(Integer, nullable=True)

    # ----------------------------
    # FK TO MASTER
    # ----------------------------
    master_id = Column(
        Integer,
        nullable=True
    )
 
    # ----------------------------
    # PATROL ENTRY FIELDS
    # ----------------------------
    patrol_date = Column(Date, nullable=True)
 
    start_time = Column(Time, nullable=True)
    start_point = Column(String(150), nullable=True)
 
    end_time = Column(Time, nullable=True)
    end_point = Column(String(150), nullable=True)
 
    team_member = Column(String(150), nullable=True)
 
    report_time = Column(Time, nullable=True)
    point_at_reporting_time = Column(String(255), nullable=True)
 
    engg_sign = Column(String(150), nullable=True)
 
    # ----------------------------
    # REMARKS
    # ----------------------------
    remarks = Column(Text, nullable=True)
    action_type = Column(String(20), nullable=True)
 
    # ----------------------------
    # SYSTEM
    # ----------------------------
    created_at = Column(DateTime, server_default=func.now(), nullable=True)
    created_by = Column(Integer, nullable=True)
    updated_at = Column(DateTime,nullable=True)
    updated_by = Column(Integer, nullable=True)