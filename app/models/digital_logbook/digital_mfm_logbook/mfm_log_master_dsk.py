from sqlalchemy import Column, Integer, String, Date, Time, Float, Text, DateTime

from sqlalchemy.sql import func

from app.database import Base
 
 
class MFMLogMaster(Base):

    __tablename__ = "mfm_log_master_dkn"

    mfm_log_dkn_id = Column(Integer, primary_key=True, autoincrement=True)

    # -------------------------

    # BASIC LOG INFO

    # -------------------------

    station = Column(String(50), nullable=True)

    station_in_charge = Column(String(100), nullable=True)
    document_no = Column(String(100), nullable=True)
    shift = Column(String(10), nullable=True)

    start_time = Column(Time, nullable=True)

    log_date = Column(Date, nullable=True)

    status = Column(String(20), nullable=True)
    plt_start_time = Column(Time, nullable=True)
    plt_end_time = Column(Time, nullable=True)
    # -------------------------

    # SHIFT HANDOVER / TAKEOVER

    # -------------------------

    shift_a_tank_taken_over = Column(String(100), nullable=True)

    shift_a_tank_handed_over = Column(String(100), nullable=True)
 
    shift_b_tank_taken_over = Column(String(100), nullable=True)

    shift_b_tank_handed_over = Column(String(100), nullable=True)
 
    shift_c_tank_taken_over = Column(String(100), nullable=True)

    shift_c_tank_handed_over = Column(String(100), nullable=True)
 
    # -------------------------

    # QUANTITY & RECEIPTS

    # -------------------------

    qty_pumped_from_mangalore = Column(Float, nullable=True)
 
    receipt_at_hassan = Column(Float, nullable=True)

    receipt_at_bangalore = Column(Float, nullable=True)
 
    qty_available_interface_tank_101 = Column(Float, nullable=True)

    qty_available_interface_tank_102 = Column(Float, nullable=True)
 
    loss_gain_101 = Column(Float, nullable=True)

    loss_gain_102 = Column(Float, nullable=True)
 
    qty_pumped_last_24hrs = Column(Float, nullable=True)

    qty_pumped_pl_t = Column(Float, nullable=True)

    qty_pumped_month = Column(Float, nullable=True)

    qty_pumped_year = Column(Float, nullable=True)
 
    # -------------------------

    # PRODUCT-WISE STOCK (TABLE)

    # -------------------------

    euro_hsd = Column(Float, nullable=True)

    bsv_hsd = Column(Float, nullable=True)

    sk_o = Column(Float, nullable=True)

    ms = Column(Float, nullable=True)

    total_product = Column(Float, nullable=True)
 
    # -------------------------

    # OPERATION HOURS & DIESEL

    # -------------------------

    hrs_operation_last_24hrs = Column(Float, nullable=True)

    hrs_operation_month = Column(Float, nullable=True)

    hrs_operation_year = Column(Float, nullable=True)
 
    sump_tank_dip_0700hrs = Column(Float, nullable=True)
 
    diesel_dg_tank = Column(Float, nullable=True)
 
    diesel_dg_set_tank = Column(Float, nullable=True)

    diesel_ffdu_3_ser_tank = Column(Float, nullable=True)

    diesel_ffdu_4_ser_tank = Column(Float, nullable=True)

    diesel_ffdu_5_ser_tank = Column(Float, nullable=True)
 
    # -------------------------

    # REMARKS & AUDIT

    # -------------------------

    remarks = Column(Text, nullable=True)
 
    created_at = Column(DateTime, server_default=func.now(), nullable=True)
    created_by = Column(Integer, nullable=True)
    updated_at = Column(DateTime,nullable=True)
    updated_by = Column(Integer, nullable=True)

    prevcumrunhour = Column(int, nullable=True)
    cummrunhour = Column(int, nullable=True)  

    acknowledge_id = Column(String(255), nullable=True)
    acknowledge_date = Column(DateTime, nullable=True)
    acknowledge_by = Column(Integer, nullable=True)
 