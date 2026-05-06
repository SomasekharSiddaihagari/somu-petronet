from sqlalchemy import Boolean, Column, Integer, String, DateTime, ForeignKey

from sqlalchemy.ext.declarative import declarative_base

from datetime import datetime
 
Base = declarative_base()
 
 
class IncidentInvestigationTeam(Base):

    __tablename__ = "incident_investigation_team"
 
    iit_id = Column(Integer, primary_key=True, autoincrement=True)
 
    # ---------------------------------

    # FK TO PREVENTION TABLE

    # ---------------------------------

    prevention_id = Column(

        Integer,

        ForeignKey("incident_prevention.ip_id"),

        nullable=True

    )
 
    # ---------------------------------

    # GRID FIELDS (FROM UI)

    # ---------------------------------
        # =========================
    # ROLE FLAGS
    # =========================
    is_leader = Column(Boolean, default=False)
    is_member = Column(Boolean, default=True)
 
    # =========================
    # ACK TRACKING
    # =========================
    leader_acknowledged = Column(Boolean, default=False)
    leader_acknowledged_at = Column(DateTime, nullable=True)
 
    member_acknowledged = Column(Boolean, default=False)
    member_acknowledged_at = Column(DateTime, nullable=True)
    sl_no = Column(Integer, nullable=True)
 
    member_name = Column(String(150), nullable=True)

    designation = Column(String(150), nullable=True)

    station = Column(String(150), nullable=True)
 
    # Role: Leader / Member

    role = Column(String(50), nullable=True)
    user_id = Column(Integer, nullable=True)  # To track who created/updated the record
    # ---------------------------------

    # SYSTEM

    # ---------------------------------

    created_by = Column(String(100), nullable=True)

    updated_by = Column(String(100), nullable=True)
 
    created_at = Column(DateTime, default=datetime.utcnow, nullable=True)

    updated_at = Column(

        DateTime,

        default=datetime.utcnow,

        onupdate=datetime.utcnow,

        nullable=True

    )

 