from sqlalchemy import Column, Integer, String, Float, Text, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
 
Base = declarative_base()
 
class MFMLogNERPage2Master(Base):
    __tablename__ = "mfm_log_ner_page2_master"
 
    mfm_log_ner_paget_two_id = Column(Integer, primary_key=True, autoincrement=True)
    master_log_id = Column(Integer, ForeignKey("mfm_log_ner_master.mfm_log_ner_id"), nullable=True)
 
    # -------------------------
    # SHIFT A (07:00 - 15:00)
    # -------------------------
    shift_a_101a_prev = Column(Float, nullable=True)
    shift_a_101a_curr = Column(Float, nullable=True)
    shift_a_101a_total = Column(Float, nullable=True)
 
    shift_a_101b_prev = Column(Float, nullable=True)
    shift_a_101b_curr = Column(Float, nullable=True)
    shift_a_101b_total = Column(Float, nullable=True)
 
    shift_a_101c_prev = Column(Float, nullable=True)
    shift_a_101c_curr = Column(Float, nullable=True)
    shift_a_101c_total = Column(Float, nullable=True)
 
    shift_a_sumpump_prev = Column(Float, nullable=True)
    shift_a_sumpump_curr = Column(Float, nullable=True)
    shift_a_sumpump_total = Column(Float, nullable=True)
 
    shift_a_net_shift = Column(Float, nullable=True)
    shift_a_gross_shift = Column(Float, nullable=True)
    shift_a_sump_level_int = Column(Float, nullable=True)
    shift_a_sump_level_fin = Column(Float, nullable=True)
 
    shift_a_line_mlr_ner_batch = Column(String(100), nullable=True)
    shift_a_line_mlr_ner_qty = Column(Float, nullable=True)
 
    shift_a_line_ner_hsn_batch = Column(String(100), nullable=True)
    shift_a_line_ner_hsn_qty = Column(Float, nullable=True)
 
    shift_a_shutdown_prev = Column(Float, nullable=True)
    shift_a_shutdown_curr = Column(Float, nullable=True)
    shift_a_shutdown_total = Column(Float, nullable=True)
 
    shift_a_shift_engg = Column(String(100), nullable=True)
    shift_a_shutdown_details = Column(Text, nullable=True)
 
    # -------------------------
    # SHIFT B (15:00 - 23:00)
    # -------------------------
    shift_b_101a_prev = Column(Float, nullable=True)
    shift_b_101a_curr = Column(Float, nullable=True)
    shift_b_101a_total = Column(Float, nullable=True)
 
    shift_b_101b_prev = Column(Float, nullable=True)
    shift_b_101b_curr = Column(Float, nullable=True)
    shift_b_101b_total = Column(Float, nullable=True)
 
    shift_b_101c_prev = Column(Float, nullable=True)
    shift_b_101c_curr = Column(Float, nullable=True)
    shift_b_101c_total = Column(Float, nullable=True)
 
    shift_b_sumpump_prev = Column(Float, nullable=True)
    shift_b_sumpump_curr = Column(Float, nullable=True)
    shift_b_sumpump_total = Column(Float, nullable=True)
 
    shift_b_net_shift = Column(Float, nullable=True)
    shift_b_gross_shift = Column(Float, nullable=True)
    shift_b_sump_level_int = Column(Float, nullable=True)
    shift_b_sump_level_fin = Column(Float, nullable=True)
 
    shift_b_line_mlr_ner_batch = Column(String(100), nullable=True)
    shift_b_line_mlr_ner_qty = Column(Float, nullable=True)
 
    shift_b_line_ner_hsn_batch = Column(String(100), nullable=True)
    shift_b_line_ner_hsn_qty = Column(Float, nullable=True)
 
    shift_b_shutdown_prev = Column(Float, nullable=True)
    shift_b_shutdown_curr = Column(Float, nullable=True)
    shift_b_shutdown_total = Column(Float, nullable=True)
 
    shift_b_shift_engg = Column(String(100), nullable=True)
    shift_b_shutdown_remarks = Column(Text, nullable=True)
 
    # -------------------------
    # SHIFT C (23:00 - 07:00)
    # -------------------------
    shift_c_101a_prev = Column(Float, nullable=True)
    shift_c_101a_curr = Column(Float, nullable=True)
    shift_c_101a_total = Column(Float, nullable=True)
 
    shift_c_101b_prev = Column(Float, nullable=True)
    shift_c_101b_curr = Column(Float, nullable=True)
    shift_c_101b_total = Column(Float, nullable=True)
 
    shift_c_101c_prev = Column(Float, nullable=True)
    shift_c_101c_curr = Column(Float, nullable=True)
    shift_c_101c_total = Column(Float, nullable=True)
 
    shift_c_sumpump_prev = Column(Float, nullable=True)
    shift_c_sumpump_curr = Column(Float, nullable=True)
    shift_c_sumpump_total = Column(Float, nullable=True)
 
    shift_c_net_shift = Column(Float, nullable=True)
    shift_c_gross_shift = Column(Float, nullable=True)
    shift_c_sump_level_int = Column(Float, nullable=True)
    shift_c_sump_level_fin = Column(Float, nullable=True)
 
    shift_c_line_mlr_ner_batch = Column(String(100), nullable=True)
    shift_c_line_mlr_ner_qty = Column(Float, nullable=True)
 
    shift_c_line_ner_hsn_batch = Column(String(100), nullable=True)
    shift_c_line_ner_hsn_qty = Column(Float, nullable=True)
 
    shift_c_shutdown_prev = Column(Float, nullable=True)
    shift_c_shutdown_curr = Column(Float, nullable=True)
    shift_c_shutdown_total = Column(Float, nullable=True)
 
    shift_c_shift_engg = Column(String(100), nullable=True)
    shift_c_shutdown_remarks = Column(Text, nullable=True)
 
    # -------------------------
    # POWER & INTERFACE SUMMARY (Bottom Section)
    # -------------------------
    power_day = Column(Float, nullable=True)
    power_month = Column(Float, nullable=True)
    power_year = Column(Float, nullable=True)
 
    pltd_day = Column(Float, nullable=True)
    pltd_month = Column(Float, nullable=True)
    pltd_year = Column(Float, nullable=True)
    
    interface_details = Column(Text, nullable=True)
    

    net_day = Column(Float, nullable=True)
    net_month = Column(Float, nullable=True)
    net_year = Column(Float, nullable=True)

    gross_day = Column(Float, nullable=True)
    gross_month = Column(Float, nullable=True)
    gross_year = Column(Float, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=True)