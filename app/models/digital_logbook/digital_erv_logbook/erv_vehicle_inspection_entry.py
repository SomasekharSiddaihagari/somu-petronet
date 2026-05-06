from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    Date,
    DateTime,
    ForeignKey,
    Text,
    func,
)
from app.database import Base


class ERVVehicleInspectionLog(Base):
    __tablename__ = "erv_vehicle_inspection_log"

    evi_id = Column(Integer, primary_key=True, autoincrement=True)

    category_master_id = Column(Integer, ForeignKey("erv_logbook_master.erv_id"), nullable=True)

    inspection_date = Column(Date, nullable=True)
    vehicle_no = Column(String(50), nullable=True)
    diesel = Column(String(50), nullable=True)

    kilometer_reading = Column(Float, nullable=True)
    trail_run_kilometer = Column(Float, nullable=True)

    cleaning = Column(String(100), nullable=True)
    head_lamp_condition = Column(String(100), nullable=True)

    siren_condition = Column(String(100), nullable=True)
    vhf_set_condition = Column(String(100), nullable=True)

    brake_condition = Column(String(100), nullable=True)
    tyre_condition = Column(String(100), nullable=True)

    battery_voltage_condition = Column(String(100), nullable=True)
    hydraulic_oil_level = Column(String(100), nullable=True)

    hydraulic_tank_line_condition = Column(String(100), nullable=True)
    rto_condition = Column(String(100), nullable=True)

    ball_valve_condition = Column(String(100), nullable=True)
    number_of_hose_pipe = Column(Integer, nullable=True)

    hose_pipe_condition = Column(String(100), nullable=True)

    any_observation = Column(Text, nullable=True)
    remarks = Column(Text, nullable=True)

    driver_signature = Column(String(255), nullable=True)
    technician_signature = Column(String(255), nullable=True)
    shift_in_charge_signature = Column(String(255), nullable=True)

    created_at = Column(DateTime, server_default=func.now())
    created_by = Column(Integer, nullable=True)
    updated_at = Column(DateTime, onupdate=func.now(), nullable=True)
    updated_by = Column(Integer, nullable=True)
