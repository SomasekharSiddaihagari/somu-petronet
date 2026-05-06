from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime, date, time


class WorkAtHeightPermitSchema(BaseModel):
    whp_id: int

    serial_number: Optional[str]
    type_of_permit: Optional[str] = "Work At Height"
    section_contractor_name: Optional[str]
    nature_of_work: Optional[str]

    work_from_time: Optional[time]
    work_from_date: Optional[date]
    work_to_time: Optional[time]
    work_to_date: Optional[date]

    location: Optional[str]

    jsa_id: Optional[int] = None

    sc1_equipment_work_area_inspected: Optional[str]
    sc2_surrounding_area_checked: Optional[str]
    sc3_sewers_manholes_covered: Optional[str]
    sc4_scaffolds_ladders_checked: Optional[str]
    sc5_materials_fall_protected: Optional[str]
    sc6_isi_marked_belts_helmets: Optional[str]
    sc7_contractor_fit_for_height: Optional[str]
    sc8_instructions_given: Optional[str]
    sc9_proper_illumination: Optional[str]
    sc10_adequate_platform_space: Optional[str]
    sc11_proper_exit_means: Optional[str]
    sc12_precautionary_tags_boards: Optional[str]
    sc13_portable_equipment_earthed: Optional[str]
    sc14_elcb_switches_provided: Optional[str]
    sc14_additional_safety_measures: Optional[str] = None
    sc15_standby_supervision_provided: Optional[str]
    sc16_workers_trained_safety_belts: Optional[str]
    sc17_operations_incharge_informed: Optional[str]
    sc18_area_cordoned_off: Optional[str]
    sc19_precautions_against_public_traffic: Optional[str]
    sc20_fire_extinguisher_provided: Optional[str]
    sc20_condition_fav_elevation_work: Optional[str] = None

    station_name: Optional[str] = None

    special_instructions: Optional[str]
    additional_remarks: Optional[str]

    issuer_designation: Optional[str]
    issuer_name: Optional[str]
    issuer_signature: Optional[str]
    issuer_userid: Optional[int] = None

    requestor_name: Optional[str] = None
    requestor_designation: Optional[str] = None
    requestor_signature: Optional[str] = None

    receiver_role: Optional[str]
    receiver_name: Optional[str]
    receiver_designation: Optional[str] = None
    receiver_signature: Optional[str]
    receiver_userid: Optional[int] = None

    electrical_isolation_required: Optional[bool]
    electrical_energization_required: Optional[bool]
    toolbox_talk_required: Optional[bool]

    renewal_from_date: Optional[date]
    renewal_from_time: Optional[time]
    renewal_to_date: Optional[date]
    renewal_to_time: Optional[time]

    renewal_issuer_name: Optional[str]
    renewal_issuer_designation: Optional[str]
    renewal_issuer_signature: Optional[str]

    renewal_requestor_name: Optional[str] = None
    renewal_requestor_designation: Optional[str] = None
    renewal_requestor_signature: Optional[str] = None

    renewal_receiver_name: Optional[str]
    renewal_receiver_designation: Optional[str]
    renewal_receiver_signature: Optional[str]

    renewal_toolbox_talk: Optional[bool]

    closure_issuer_designation: Optional[str]
    closure_issuer_name: Optional[str]
    closure_issuer_signature: Optional[str]
    closure_issuer_userid: Optional[int] = None

    closure_requestor_name: Optional[str] = None
    closure_requestor_designation: Optional[str] = None
    closure_requestor_signature: Optional[str] = None
    closure_requestor_userid: Optional[int] = None

    closure_receiver_role: Optional[str]
    closure_receiver_name: Optional[str]
    closure_receiver_signature: Optional[str]
    closure_receiver_userid: Optional[int] = None

    job_completion_time: Optional[time]
    job_completion_date: Optional[date]
    work_status: Optional[str]

    status: Optional[str]
    created_by: Optional[str]
    updated_by: Optional[int] = None
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    class Config:
        orm_mode = True


# CHILD SCHEMAS

class WorkAtHeightToolboxTalkParticipantSchema(BaseModel):
    whttp_id: int
    toolbox_talk_id: Optional[int]
    participant_name: Optional[str]
    participant_signature: Optional[str]
    created_at: Optional[datetime]

    class Config:
        orm_mode = True


class WorkAtHeightToolboxTalkSchema(BaseModel):
    whtt_id: int
    work_at_height_permit_id: Optional[int]
    cross_reference_of_other_permit: Optional[str]
    work_clearance_time: Optional[time]
    work_clearance_date: Optional[date]
    contractor_engineer_name: Optional[str]
    work_installation_unit_facility_name: Optional[str]
    tbt_delivered_by: Optional[str]
    contract_supervisor_name: Optional[str]
    topics_issues_discussed: Optional[str]
    other_points_raised: Optional[str]
    created_by: Optional[str]
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
    participants: List["WorkAtHeightToolboxTalkParticipantSchema"] = []

    class Config:
        orm_mode = True


class WorkAtHeightIsolationPermitSchema(BaseModel):
    whpis_id: int
    whp_id: Optional[int]
    work_permit_number: Optional[str]
    work_clearance_time: Optional[time]
    work_clearance_date: Optional[date]
    cross_reference_of_other_permit: Optional[str]
    department_section_area: Optional[str]
    equipment_number_to_be_isolated: Optional[str]
    name_of_equipment_circuit: Optional[str]
    description_of_work: Optional[str]

    equipment_circuit_no: Optional[str]
    plant: Optional[str]
    work_clearance_from_time: Optional[time]
    work_clearance_from_date: Optional[date]
    loto_tag_device_no: Optional[str]
    authorized_person_name: Optional[str]
    designation: Optional[str]
    signature: Optional[str]
    isolation_method: Optional[str]

    issuer_name: Optional[str]
    issuer_designation: Optional[str]
    issuer_signature: Optional[str]
    created_by: Optional[str]
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    class Config:
        orm_mode = True


class WorkAtHeightEnergizationPermitSchema(BaseModel):
    whpep_id: int
    whp_id: Optional[int]
    work_permit_number: Optional[str]
    work_clearance_time: Optional[time]
    work_clearance_date: Optional[date]
    name_of_equipment_circuit: Optional[str]
    department_section_area: Optional[str]
    equipment_number_to_be_energized: Optional[str]
    cross_reference_of_other_permit: Optional[str]

    equipment_circuit_no: Optional[str]
    plant: Optional[str]
    work_clearance_from_time: Optional[time]
    work_clearance_from_date: Optional[date]
    loto_tag_device_no: Optional[str]
    authorized_person_name: Optional[str]
    designation: Optional[str]
    signature: Optional[str]
    energization_method: Optional[str]

    issuer_name: Optional[str]
    issuer_designation: Optional[str]
    issuer_signature: Optional[str]
    created_by: Optional[str]
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    class Config:
        orm_mode = True


class WorkAtHeightPermitDetailSchema(WorkAtHeightPermitSchema):
    toolbox_talks: List[WorkAtHeightToolboxTalkSchema] = []
    isolation_permits: List[WorkAtHeightIsolationPermitSchema] = []
    energization_permits: List[WorkAtHeightEnergizationPermitSchema] = []

    class Config:
        orm_mode = True