from sqlalchemy import Column, Integer, String, Float, Date, DateTime, Text, func
from app.database import Base


class ERVVehicleInspectionLogHistory(Base):
    __tablename__ = "erv_vehicle_inspection_log_history"

    history_id = Column(Integer, primary_key=True, autoincrement=True)
    evi_id = Column(Integer, nullable=True)

    category_master_id = Column(Integer, nullable=True)

    inspection_date = Column(Date, nullable=True)
    vehicle_no = Column(String(50), nullable=True, server_default="")
    diesel = Column(String(50), nullable=True, server_default="")
    kilometer_reading = Column(Float, nullable=True, server_default="0")
    trail_run_kilometer = Column(Float, nullable=True, server_default="0")

    cleaning = Column(String(100), nullable=True, server_default="")
    head_lamp_condition = Column(String(100), nullable=True, server_default="")
    siren_condition = Column(String(100), nullable=True, server_default="")
    vhf_set_condition = Column(String(100), nullable=True, server_default="")
    brake_condition = Column(String(100), nullable=True, server_default="")
    tyre_condition = Column(String(100), nullable=True, server_default="")
    battery_voltage_condition = Column(String(100), nullable=True, server_default="")
    hydraulic_oil_level = Column(String(100), nullable=True, server_default="")
    hydraulic_tank_line_condition = Column(
        String(100), nullable=True, server_default=""
    )
    rto_condition = Column(String(100), nullable=True, server_default="")
    ball_valve_condition = Column(String(100), nullable=True, server_default="")
    number_of_hose_pipe = Column(Integer, nullable=True, server_default="0")
    hose_pipe_condition = Column(String(100), nullable=True, server_default="")

    any_observation = Column(Text, nullable=True, server_default="")
    remarks = Column(Text, nullable=True, server_default="")

    driver_signature = Column(String(255), nullable=True, server_default="")
    technician_signature = Column(String(255), nullable=True, server_default="")
    shift_in_charge_signature = Column(String(255), nullable=True, server_default="")

    action_type = Column(String(20), nullable=True)

    created_at = Column(DateTime, server_default=func.now())
    created_by = Column(Integer, nullable=True)
    updated_at = Column(DateTime, onupdate=func.now(), nullable=True)
    updated_by = Column(Integer, nullable=True)
