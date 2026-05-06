from sqlalchemy import Column, Integer, String, Date, Time, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
 
Base = declarative_base()
 
class WorkAtHeightElectricalEnergizationPermit(Base):
    __tablename__ = "work_at_height_electrical_energization_permit"
 
    whpep_id = Column(Integer, primary_key=True, autoincrement=True)
 
    # ---------------------------------
    # FK TO WORK AT HEIGHT PERMIT (UPDATED PK NAME)
    # ---------------------------------
    whp_id = Column(
        Integer,
        ForeignKey("work_at_height_permit.whp_id"),
        nullable=True
    )
 
    # =================================================
    # REQUEST FOR ENERGIZATION
    # =================================================
    work_permit_number = Column(String(150), nullable=True)
 
    work_clearance_time = Column(Time, nullable=True)
    work_clearance_date = Column(Date, nullable=True)
 
    name_of_equipment_circuit = Column(String(255), nullable=True)
 
    department_section_area = Column(String(255), nullable=True)
 
    equipment_number_to_be_energized = Column(String(255), nullable=True)
 
    cross_reference_of_other_permit = Column(String(150), nullable=True)

    # =================================================
    # ELECTRICAL certificate
    # =================================================

    equipment_circuit_no = Column(String, nullable=True)
    plant = Column(String, nullable=True)

    work_clearance_from_time = Column(Time, nullable=True)
    work_clearance_from_date = Column(Date, nullable=True)

    energization_method = Column(String, nullable=True)

    loto_tag_device_no = Column(String, nullable=True)

    authorized_person_name = Column(String, nullable=True)
    designation = Column(String, nullable=True)

    signature = Column(String, nullable=True)

 
    # =================================================
    # ISSUER
    # =================================================
    issuer_name = Column(String(150), nullable=True)
    issuer_designation = Column(String(150), nullable=True)
    issuer_signature = Column(String(255), nullable=True)
 
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