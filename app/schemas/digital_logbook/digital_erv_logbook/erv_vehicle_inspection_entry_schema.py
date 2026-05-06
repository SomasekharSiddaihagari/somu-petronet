from pydantic import BaseModel, ConfigDict, Field
from typing import Optional
from app.utils.schema_validators import FlexDate, FlexDatetime


class ERVVehicleInspectionBase(BaseModel):
    category_master_id: int
    inspection_date: Optional[FlexDate] = None
    vehicle_no: Optional[str] = None
    diesel: Optional[str] = None
    kilometer_reading: Optional[float] = None
    trail_run_kilometer: Optional[float] = None

    cleaning: Optional[str] = None
    head_lamp_condition: Optional[str] = None
    siren_condition: Optional[str] = None
    vhf_set_condition: Optional[str] = None
    brake_condition: Optional[str] = None
    tyre_condition: Optional[str] = None
    battery_voltage_condition: Optional[str] = None
    hydraulic_oil_level: Optional[str] = None
    hydraulic_tank_line_condition: Optional[str] = None
    rto_condition: Optional[str] = None
    ball_valve_condition: Optional[str] = None
    number_of_hose_pipe: Optional[int] = None
    hose_pipe_condition: Optional[str] = None

    any_observation: Optional[str] = None
    remarks: Optional[str] = None

    driver_signature: Optional[str] = None
    technician_signature: Optional[str] = None
    shift_in_charge_signature: Optional[str] = None

    # Audit Fields
    created_at: Optional[FlexDatetime] = None
    created_by: Optional[int] = None
    updated_at: Optional[FlexDatetime] = None
    updated_by: Optional[int] = None

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)


class ERVVehicleInspectionResponse(ERVVehicleInspectionBase):
    evi_id: int
    created_by_name: Optional[str] = None
    updated_by_name: Optional[str] = None


class ERVVehicleInspectionCreate(ERVVehicleInspectionBase):
    inspection_date: FlexDate
    vehicle_no: str
    diesel: str
    kilometer_reading: float
    trail_run_kilometer: float
    cleaning: str
    head_lamp_condition: str
    siren_condition: str
    vhf_set_condition: str
    brake_condition: str
    tyre_condition: str
    battery_voltage_condition: str
    hydraulic_oil_level: str
    hydraulic_tank_line_condition: str
    rto_condition: str
    ball_valve_condition: str
    number_of_hose_pipe: int
    hose_pipe_condition: str


class ERVVehicleInspectionUpdate(ERVVehicleInspectionBase):
    category_master_id: Optional[int] = None
