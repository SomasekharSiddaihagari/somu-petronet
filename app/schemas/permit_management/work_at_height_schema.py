from pydantic import BaseModel
from typing import Optional
from datetime import date, time


class WorkAtHeightPermitBase(BaseModel):
    serial_number: Optional[str] = None
    section_contractor_name: Optional[str] = None
    nature_of_work: Optional[str] = None

    work_from_time: Optional[time] = None
    work_from_date: Optional[date] = None
    work_to_time: Optional[time] = None
    work_to_date: Optional[date] = None

    location: Optional[str] = None

    jsa_id: Optional[int] = None

    sc1_equipment_work_area_inspected: Optional[str] = None
    sc2_surrounding_area_checked: Optional[str] = None
    sc3_sewers_manholes_covered: Optional[str] = None
    sc4_scaffolds_ladders_checked: Optional[str] = None
    sc5_materials_fall_protected: Optional[str] = None
    sc6_isi_marked_belts_helmets: Optional[str] = None
    sc7_contractor_fit_for_height: Optional[str] = None
    sc8_instructions_given: Optional[str] = None
    sc9_proper_illumination: Optional[str] = None
    sc10_adequate_platform_space: Optional[str] = None
    sc11_proper_exit_means: Optional[str] = None
    sc12_precautionary_tags_boards: Optional[str] = None
    sc13_portable_equipment_earthed: Optional[str] = None
    sc14_elcb_switches_provided: Optional[str] = None
    sc14_additional_safety_measures: Optional[str] = None
    sc15_standby_supervision_provided: Optional[str] = None
    sc16_workers_trained_safety_belts: Optional[str] = None
    sc17_operations_incharge_informed: Optional[str] = None
    sc18_area_cordoned_off: Optional[str] = None
    sc19_precautions_against_public_traffic: Optional[str] = None
    sc20_fire_extinguisher_provided: Optional[str] = None
    sc20_condition_fav_elevation_work: Optional[str] = None

    special_instructions: Optional[str] = None
    additional_remarks: Optional[str] = None

    # Issuer
    issuer_designation: Optional[str] = None
    issuer_name: Optional[str] = None
    issuer_signature: Optional[str] = None
    issuer_userid: Optional[int] = None

    # Requestor
    requestor_name: Optional[str] = None
    requestor_designation: Optional[str] = None
    requestor_signature: Optional[str] = None

    # Receiver
    receiver_role: Optional[str] = None
    receiver_name: Optional[str] = None
    receiver_designation: Optional[str] = None
    receiver_signature: Optional[str] = None
    receiver_userid: Optional[int] = None

    electrical_isolation_required: Optional[bool] = None
    electrical_energization_required: Optional[bool] = None
    toolbox_talk_required: Optional[bool] = None

    # Renewal
    renewal_from_date: Optional[date] = None
    renewal_from_time: Optional[time] = None
    renewal_to_date: Optional[date] = None
    renewal_to_time: Optional[time] = None

    renewal_issuer_name: Optional[str] = None
    renewal_issuer_designation: Optional[str] = None
    renewal_issuer_signature: Optional[str] = None

    renewal_requestor_name: Optional[str] = None
    renewal_requestor_designation: Optional[str] = None
    renewal_requestor_signature: Optional[str] = None

    renewal_receiver_name: Optional[str] = None
    renewal_receiver_designation: Optional[str] = None
    renewal_receiver_signature: Optional[str] = None

    renewal_toolbox_talk: Optional[bool] = None

    # Closure
    closure_issuer_designation: Optional[str] = None
    closure_issuer_name: Optional[str] = None
    closure_issuer_signature: Optional[str] = None
    closure_issuer_userid: Optional[int] = None

    closure_requestor_name: Optional[str] = None
    closure_requestor_designation: Optional[str] = None
    closure_requestor_signature: Optional[str] = None
    closure_requestor_userid: Optional[int] = None

    closure_receiver_role: Optional[str] = None
    closure_receiver_name: Optional[str] = None
    closure_receiver_signature: Optional[str] = None
    closure_receiver_userid: Optional[int] = None

    job_completion_time: Optional[time] = None
    job_completion_date: Optional[date] = None
    work_status: Optional[str] = None

    status: Optional[str] = None
    created_by: Optional[int] = None
    updated_by: Optional[int] = None


class WorkAtHeightPermitCreate(WorkAtHeightPermitBase):
    created_by: int
    jsa_id: Optional[int] = None


class WorkAtHeightPermitUpdate(WorkAtHeightPermitBase):
    pass