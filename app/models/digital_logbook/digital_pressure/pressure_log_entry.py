from sqlalchemy import Column, Integer, String, Date, Time, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.database import Base


class PressureLogEntry(Base):
    __tablename__ = "pressure_log_entry"

    pressure_entry_id = Column(Integer, primary_key=True, autoincrement=True)

    pressure_id = Column(
        Integer,
        ForeignKey("pressure_log_master.pressure_id", ondelete="CASCADE"),
        nullable=True
    )
    


    # ======================
    # Mangalore
    # ======================

    sv1_in = Column(String(200), nullable=True)
    sv1_out = Column(String(200), nullable=True)

    sv2_in = Column(String(200), nullable=True)
    sv2_out = Column(String(200), nullable=True)

    sv3_in = Column(String(200), nullable=True)
    sv3_out = Column(String(200), nullable=True)

    # ======================
    # Neriya
    # ======================

    sv4_in = Column(String(200), nullable=True)
    sv4_out = Column(String(200), nullable=True)

    sv5_in = Column(String(200), nullable=True)
    sv5_out = Column(String(200), nullable=True)

    # ======================
    # Hassan
    # ======================

    sv6_in = Column(String(200), nullable=True)
    sv6_out = Column(String(200), nullable=True)

    sv7_in = Column(String(200), nullable=True)
    sv7_out = Column(String(200), nullable=True)

    sv8_in = Column(String(200), nullable=True)
    sv8_out = Column(String(200), nullable=True)

    # ======================
    # IP
    # ======================

    sv9_in = Column(String(200), nullable=True)
    sv9_out = Column(String(200), nullable=True)

    sv10_in = Column(String(200), nullable=True)
    sv10_out = Column(String(200), nullable=True)


    entry_date = Column(Date, nullable=True)
    entry_time = Column(Time, nullable=True)

    # ======================
    # Mangalore
    # ======================
    mangalore_1 = Column(String(200), nullable=True)
    mangalore_2 = Column(String(200), nullable=True)

    # ======================
    # Neriya
    # ======================
    neriya_1 = Column(String(200), nullable=True)
    neriya_2 = Column(String(200), nullable=True)
    neriya_3 = Column(String(200), nullable=True)

    # ======================
    # Hassan
    # ======================
    hassan_1 = Column(String(200), nullable=True)
    hassan_2 = Column(String(200), nullable=True)

    # ======================
    # IP
    # ======================
    ip_1 = Column(String(200), nullable=True)
    ip_2 = Column(String(200), nullable=True)

    # ======================
    # Devangonthi
    # ======================
    devangonthi_1 = Column(String(200), nullable=True)
    devangonthi_2 = Column(String(200), nullable=True)

    # ======================
    # Meta
    # ======================
    created_at = Column(DateTime, server_default=func.now(), nullable=True)
    updated_at = Column(DateTime,  nullable=True)
    created_by = Column(Integer, nullable=True)
    updated_by = Column(Integer, nullable=True)

