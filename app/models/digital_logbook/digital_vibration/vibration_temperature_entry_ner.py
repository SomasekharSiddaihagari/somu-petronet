from sqlalchemy import Column, Integer, String, Float, Date, Time, DateTime, ForeignKey, func
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
 
Base = declarative_base()
 
class VibrationTemperatureEntryNer(Base):
    __tablename__ = "vibration_temperature_entry_ner"
 
    vten_id = Column(Integer, primary_key=True, autoincrement=True)
 
    # ----------------------------
    # FK TO MASTER
    # ----------------------------
    master_id = Column(
        Integer,
        ForeignKey("vibration_temperature_master.vte_id"),
        nullable=True
    )
 
    # ----------------------------
    # BASIC
    # ----------------------------
    entry_date = Column(Date, nullable=True)
    entry_time = Column(Time, nullable=True)
    mlp101_a_b_c = Column(String(50), nullable=True)   # MLP101 A/B/C
 
    # =================================================
    # PART 1
    # =================================================
 
    # Pump Vibration
    pump_vib_de_x = Column(Float, nullable=True)
    pump_vib_de_y = Column(Float, nullable=True)
    pump_vib_nde_x = Column(Float, nullable=True)
    pump_vib_nde_y = Column(Float, nullable=True)
 
    # Pump Thrust
    pump_thrust_x = Column(Float, nullable=True)
    pump_thrust_y = Column(Float, nullable=True)
 
    # Motor Bearing Vibration
    motor_bearing_vib_de_x = Column(Float, nullable=True)
    motor_bearing_vib_de_y = Column(Float, nullable=True)
    motor_bearing_vib_nde_x = Column(Float, nullable=True)
    motor_bearing_vib_nde_y = Column(Float, nullable=True)
 
    # Motor Winding Temperature (CH1-3)
    motor_winding_ch1 = Column(Float, nullable=True)
    motor_winding_ch2 = Column(Float, nullable=True)
    motor_winding_ch3 = Column(Float, nullable=True)
 
    # =================================================
    # PART 2
    # =================================================
 
    # Motor Winding Temperature (CH4-6)
    motor_winding_ch4 = Column(Float, nullable=True)
    motor_winding_ch5 = Column(Float, nullable=True)
    motor_winding_ch6 = Column(Float, nullable=True)
 
    # Motor Bearing Temperature
    motor_bearing_temp_de = Column(Float, nullable=True)
    motor_bearing_temp_nde = Column(Float, nullable=True)
 
    # Pump Body Temperature
    pump_body_temperature = Column(Float, nullable=True)
 
    # Pump Bearing Temperature
    pump_bearing_temp_de_x = Column(Float, nullable=True)
    pump_bearing_temp_de_y = Column(Float, nullable=True)
    pump_bearing_temp_nde_x = Column(Float, nullable=True)
    pump_bearing_temp_nde_y = Column(Float, nullable=True)
    pump_bearing_thrust_x = Column(Float, nullable=True)
    pump_bearing_thrust_y = Column(Float, nullable=True)
 
    # ----------------------------
    # SYSTEM
    # ----------------------------
    created_at = Column(DateTime, server_default=func.now(), nullable=True)
    created_by = Column(Integer, nullable=True)
    updated_at = Column(DateTime,nullable=True)
    updated_by = Column(Integer, nullable=True)

   