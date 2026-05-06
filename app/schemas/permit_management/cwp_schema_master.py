from pydantic import BaseModel
from typing import Optional
from datetime import date, time


class CompositeWorkPermitBase(BaseModel):
    serial_number: Optional[str] = None
    location: Optional[str] = None
    issued_to: Optional[str] = None
    description_of_work: Optional[str] = None

    work_from_time: Optional[time] = None
    work_from_date: Optional[date] = None
    work_to_time: Optional[time] = None
    work_to_date: Optional[date] = None

    jsa_id: Optional[int] = None
    jsa_ref_no: Optional[str] = None
    job_type: Optional[str] = None
    cross_reference_permits: Optional[str] = None
    isolation_certificate_ref: Optional[str] = None

    a1_equipment_area_inspected: Optional[str] = None
    a1_sub_equipment: Optional[bool] = False
    a1_sub_work_area: Optional[bool] = False

    a2_surrounding_area_checked: Optional[str] = None

    a3_sewers_manholes_covered: Optional[str] = None
    a3_sub_sewers: Optional[bool] = False
    a3_sub_manholes: Optional[bool] = False
    a3_sub_cbd: Optional[bool] = False
    a3_sub_hot_surface: Optional[bool] = False
    a3_sub_other: Optional[bool] = False
    a3_sub_other_text: Optional[str] = None

    a4_hazards_considered: Optional[str] = None
    a5_equipment_drained: Optional[str] = None

    a6_equipment_steamed_purged: Optional[str] = None
    a6_sub_steamed: Optional[bool] = False
    a6_sub_purged: Optional[bool] = False

    a7_equipment_blinded_isolated: Optional[str] = None
    a7_sub_blinded: Optional[bool] = False
    a7_sub_disconnected: Optional[bool] = False
    a7_sub_closed: Optional[bool] = False
    a7_sub_isolated: Optional[bool] = False
    a7_sub_wedge_opened: Optional[bool] = False

    a8_equipment_water_flushed: Optional[str] = None

    a9_iron_sulphide_removed: Optional[str] = None
    a9_sub_sulphide_removed: Optional[bool] = False
    a9_sub_kept_wet: Optional[bool] = False

    a10_equipment_electrically_isolated: Optional[str] = None

    a11_gas_test: Optional[str] = None
    a11_val_hcs_percent: Optional[str] = None
    a11_val_toxic_gas_ppm: Optional[str] = None
    a11_val_o2_percent: Optional[str] = None

    a12_fire_extinguisher_provided: Optional[str] = None
    a12_sub_running_water_hose: Optional[bool] = False
    a12_sub_fire_extinguisher: Optional[bool] = False
    a12_sub_fire_water_system: Optional[bool] = False

    a13_area_cordoned: Optional[str] = None
    a14_ventilation_lighting: Optional[str] = None

    b1_escape_provided: Optional[str] = None

    b2_standby_personnel: Optional[str] = None
    b2_sub_process: Optional[bool] = False
    b2_sub_maint: Optional[bool] = False
    b2_sub_contractor: Optional[bool] = False
    b2_sub_fire_dept: Optional[bool] = False

    b3_check_oil_gas_trapped: Optional[str] = None
    b4_shield_against_spark: Optional[str] = None
    b5_portable_equipment_grounded: Optional[str] = None
    b6_standby_for_confined_space: Optional[str] = None

    c1_peso_spark_elimination: Optional[str] = None
    c1_sub_mobile_equipment: Optional[bool] = False
    c1_sub_vehicle_provided: Optional[bool] = False

    d1_excavation_clearance_obtained: Optional[str] = None
    d1_sub_excavation: Optional[bool] = False
    d1_sub_road_cutting: Optional[bool] = False
    d1_sub_dyke_cutting: Optional[bool] = False

    hazard_lack_of_o2: Optional[bool] = False
    hazard_lack_of_h2s: Optional[bool] = False
    hazard_toxic_gases: Optional[bool] = False
    hazard_combustible_gases: Optional[bool] = False
    hazard_pyrophoric_iron: Optional[bool] = False
    hazard_corrosive_chemicals: Optional[bool] = False
    hazard_steam_condensate: Optional[bool] = False
    hazard_other: Optional[bool] = False
    hazard_other_text: Optional[str] = None

    ppe_helmet: Optional[bool] = False
    ppe_safety_shoes: Optional[bool] = False
    ppe_hand_gloves: Optional[bool] = False
    ppe_boiler_suit: Optional[bool] = False
    ppe_cotton_coverall: Optional[bool] = False
    ppe_face_shield: Optional[bool] = False
    ppe_fresh_air_mask: Optional[bool] = False
    ppe_dust_respirator: Optional[bool] = False
    ppe_apron: Optional[bool] = False
    ppe_goggles: Optional[bool] = False
    ppe_earmuff: Optional[bool] = False
    ppe_lifeline: Optional[bool] = False
    ppe_safety_belt: Optional[bool] = False
    ppe_airline: Optional[bool] = False
    ppe_other: Optional[bool] = False
    ppe_other_text: Optional[str] = None

    additional_requirements_precautions: Optional[str] = None

    requestor_name: Optional[str] = None
    requestor_designation: Optional[str] = None
    requestor_signature: Optional[str] = None

    issuer_name: Optional[str] = None
    issuer_designation: Optional[str] = None
    issuer_signature: Optional[str] = None
    issuer_userid: Optional[int] = None

    receiver_name: Optional[str] = None
    receiver_designation: Optional[str] = None
    receiver_signature: Optional[str] = None
    receiver_userid: Optional[int] = None

    electrical_isolation_required: Optional[bool] = None
    electrical_energization_required: Optional[bool] = None
    toolbox_talk_completed: Optional[bool] = None

    gas_test_from_time: Optional[time] = None
    gas_test_to_time: Optional[time] = None
    gas_test_from_date: Optional[date] = None
    gas_test_to_date: Optional[date] = None

    gas_hcs_percent: Optional[str] = None
    gas_toxic_ppm: Optional[str] = None
    gas_o2_percent: Optional[str] = None
    gas_additional_precautions: Optional[str] = None

    gas_requestor_name: Optional[str] = None
    gas_requestor_designation: Optional[str] = None
    gas_requestor_signature: Optional[str] = None
    gas_requestor_userid: Optional[int] = None

    gas_issuer_name: Optional[str] = None
    gas_issuer_designation: Optional[str] = None
    gas_issuer_signature: Optional[str] = None
    gas_issuer_userid: Optional[int] = None

    gas_receiver_name: Optional[str] = None
    gas_receiver_designation: Optional[str] = None
    gas_receiver_signature: Optional[str] = None
    gas_receiver_userid: Optional[int] = None

    closure_requestor_name: Optional[str] = None
    closure_requestor_designation: Optional[str] = None
    closure_requestor_signature: Optional[str] = None
    closure_requestor_userid: Optional[int] = None

    closure_issuer_name: Optional[str] = None
    closure_issuer_designation: Optional[str] = None
    closure_issuer_signature: Optional[str] = None
    closure_issuer_userid: Optional[int] = None

    closure_receiver_name: Optional[str] = None
    closure_receiver_designation: Optional[str] = None
    closure_receiver_signature: Optional[str] = None
    closure_receiver_userid: Optional[int] = None

    status: Optional[str] = None
    created_by: Optional[int] = None
    updated_by: Optional[int] = None


class CompositeWorkPermitCreate(CompositeWorkPermitBase):
    created_by: int


class CompositeWorkPermitUpdate(CompositeWorkPermitBase):
    pass