from sqlalchemy import Column, Integer, String, Date, Time, DateTime, Boolean, Text
from app.database import Base
from datetime import datetime


class WorkAtHeightPermit(Base):
    __tablename__ = "work_at_height_permit_history"

    history_id = Column(Integer, primary_key=True, autoincrement=True)
    whp_id = Column(Integer, nullable=True)
    jsa_id = Column(Integer, nullable=True)

    # =================================================
    # PERMIT VALIDITY & WORK INFORMATION
    # =================================================
    serial_number = Column(String(150), nullable=True)
    contractor_id = Column(Integer, nullable=True)
    engineer_id = Column(Integer, nullable=True)
    section_contractor_name = Column(String(255), nullable=True)

    nature_of_work = Column(Text, nullable=True)

    work_from_time = Column(Time, nullable=True)
    work_from_date = Column(Date, nullable=True)
    work_to_time = Column(Time, nullable=True)
    work_to_date = Column(Date, nullable=True)

    location = Column(String(255), nullable=True)
   

    # =================================================
    # SAFETY CHECKLIST (DONE / N/A)
    # Store as: 'Done' / 'N/A' / NULL
    # =================================================
    sc1_equipment_work_area_inspected = Column(String(20), nullable=True)
    sc2_surrounding_area_checked = Column(String(20), nullable=True)
    sc3_sewers_manholes_covered = Column(String(20), nullable=True)
    sc4_scaffolds_ladders_checked = Column(String(20), nullable=True)
    sc5_materials_fall_protected = Column(String(20), nullable=True)
    sc6_isi_marked_belts_helmets = Column(String(20), nullable=True)
    sc7_contractor_fit_for_height = Column(String(20), nullable=True)
    sc8_instructions_given = Column(String(20), nullable=True)
    sc9_proper_illumination = Column(String(20), nullable=True)
    sc10_adequate_platform_space = Column(String(20), nullable=True)
    sc11_proper_exit_means = Column(String(20), nullable=True)
    sc12_precautionary_tags_boards = Column(String(20), nullable=True)
    sc13_portable_equipment_earthed = Column(String(20), nullable=True)
    sc14_additional_safety_measures = Column(String(20), nullable=True)
    sc15_standby_supervision_provided = Column(String(20), nullable=True)
    sc16_workers_trained_safety_belts = Column(String(20), nullable=True) #changed
    sc17_operations_incharge_informed = Column(String(20), nullable=True)
    sc18_area_cordoned_off = Column(String(20), nullable=True)
    sc19_precautions_against_public_traffic = Column(String(20), nullable=True)
    sc20_condition_fav_elevation_work = Column(String(20), nullable=True) #changed

    # =================================================
    # SPECIAL INSTRUCTIONS
    # =================================================
    special_instructions = Column(Text, nullable=True)

    # =================================================
    # ADDITIONAL REMARKS
    # =================================================
    additional_remarks = Column(Text, nullable=True)

    # =================================================
    # AUTHORIZATION SIGNATURES
    # =================================================
    requestor_name = Column(String(150), nullable=True)
    requestor_designation = Column(String(150), nullable=True)
    requestor_signature = Column(String(255), nullable=True)

    issuer_name = Column(String(150), nullable=True)
    issuer_designation = Column(String(150), nullable=True)
    issuer_signature = Column(String(255), nullable=True)

    receiver_name = Column(String(150), nullable=True)
    receiver_designation = Column(String(150), nullable=True)
    receiver_signature = Column(String(255), nullable=True)

    # =================================================
    # ELECTRICAL / TOOLBOX FLAGS
    # =================================================
    electrical_isolation_required = Column(Boolean, nullable=True)
    electrical_energization_required = Column(Boolean, nullable=True)
    toolbox_talk_required = Column(Boolean, nullable=True)

    # =================================================
    # PERMIT RENEWAL RECORD (FLATTENED SUMMARY)
    # (Full grid can be normalized later if needed)
    # =================================================
    renewal_from_date = Column(Date, nullable=True)
    renewal_from_time = Column(Time, nullable=True)
    renewal_to_date = Column(Date, nullable=True)
    renewal_to_time = Column(Time, nullable=True)

    renewal_requestor_name = Column(String(150), nullable=True)
    renewal_requestor_designation = Column(String(150), nullable=True)
    renewal_requestor_signature = Column(String(255), nullable=True)

    renewal_issuer_name = Column(String(150), nullable=True)
    renewal_issuer_designation = Column(String(150), nullable=True)
    renewal_issuer_signature = Column(String(255), nullable=True)

    renewal_receiver_name = Column(String(150), nullable=True)
    renewal_receiver_designation = Column(String(150), nullable=True)
    renewal_receiver_signature = Column(String(255), nullable=True)

    renewal_toolbox_talk = Column(Boolean, nullable=True)

    # =================================================
    # CLOSURE SIGNATURES
    # =================================================
    closure_requestor_name = Column(String(150), nullable=True)
    closure_requestor_designation = Column(String(150), nullable=True)
    closure_requestor_signature = Column(String(255), nullable=True)

    closure_issuer_name = Column(String(150), nullable=True)
    closure_issuer_designation = Column(String(150), nullable=True)
    closure_issuer_signature = Column(String(255), nullable=True)

    closure_receiver_name = Column(String(150), nullable=True)
    closure_receiver_designation = Column(String(150), nullable=True)
    closure_receiver_signature = Column(String(255), nullable=True)

    # =================================================
    # JOB COMPLETION CONFIRMATION
    # =================================================
    job_completion_time = Column(Time, nullable=True)
    job_completion_date = Column(Date, nullable=True)
    work_status = Column(Text, nullable=True)

    # =================================================
    # SYSTEM
    # =================================================
    status = Column(String(50), nullable=True)  # Draft / Submitted / Approved / Closed
    created_by = Column(String(100), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=True)
    updated_by = Column(String(100), nullable=True)
    updated_at = Column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=True
    )
