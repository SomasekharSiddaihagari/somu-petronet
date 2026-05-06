from pydoc import text
from pydantic import BaseModel
from typing import Optional


# =========================
# CREATE
# =========================
class IncidentCauseAnalysisCreate(BaseModel):
    incident_id: int   # FK

    cause_deviation_from_procedure: Optional[bool]
    cause_lack_of_job_knowledge: Optional[bool]
    cause_lack_of_supervision: Optional[bool]
    cause_improper_inspection: Optional[bool]
    cause_improper_maintenance: Optional[bool]
    cause_improper_material_handling: Optional[bool]
    cause_negligent_driving: Optional[bool]
    cause_not_using_ppe: Optional[bool]
    cause_equipment_failure: Optional[bool]
    cause_poor_design_layout: Optional[bool]
    cause_inadequate_facility: Optional[bool]
    cause_poor_house_keeping: Optional[bool]
    cause_natural_calamity: Optional[bool]
    cause_pilferage_sabotage: Optional[bool]

    leak_weld_from_equipment_lines: Optional[bool]
    leak_from_flange_gland: Optional[bool]
    leak_from_rotary_equipment: Optional[bool]
    leak_metallurgical_failure: Optional[bool]
    leak_due_to_improper_operation: Optional[bool]
    leak_due_to_improper_maintenance: Optional[bool]
    leak_normal_operation_venting_draining: Optional[bool]
    leak_any_other: Optional[bool]
    leak_any_other_description: Optional[str] = None

    ignition_near_to_hot_work: Optional[bool]
    ignition_near_to_furnace_flare: Optional[bool]
    ignition_auto_ignition: Optional[bool]
    ignition_loose_electrical_connection: Optional[bool]
    ignition_near_to_hot_surface: Optional[bool]
    ignition_static_electricity: Optional[bool]
    ignition_hammering_fall_of_object: Optional[bool]
    ignition_heat_due_to_friction: Optional[bool]
    ignition_lightning: Optional[bool]
    ignition_any_other_pyrophoric: Optional[bool]
    ignition_any_other_pyrophoric_description: Optional[str] = None

    status: Optional[str]
    created_by: Optional[str]


# =========================
# UPDATE (FULL)
# =========================
class IncidentCauseAnalysisUpdate(BaseModel):
    cause_deviation_from_procedure: Optional[bool]
    cause_lack_of_job_knowledge: Optional[bool]
    cause_lack_of_supervision: Optional[bool]
    cause_improper_inspection: Optional[bool]
    cause_improper_maintenance: Optional[bool]
    cause_improper_material_handling: Optional[bool]
    cause_negligent_driving: Optional[bool]
    cause_not_using_ppe: Optional[bool]
    cause_equipment_failure: Optional[bool]
    cause_poor_design_layout: Optional[bool]
    cause_inadequate_facility: Optional[bool]
    cause_poor_house_keeping: Optional[bool]
    cause_natural_calamity: Optional[bool]
    cause_pilferage_sabotage: Optional[bool]

    leak_weld_from_equipment_lines: Optional[bool]
    leak_from_flange_gland: Optional[bool]
    leak_from_rotary_equipment: Optional[bool]
    leak_metallurgical_failure: Optional[bool]
    leak_due_to_improper_operation: Optional[bool]
    leak_due_to_improper_maintenance: Optional[bool]
    leak_normal_operation_venting_draining: Optional[bool]
    leak_any_other: Optional[bool]
    leak_any_other_description: Optional[str] = None

    ignition_near_to_hot_work: Optional[bool]
    ignition_near_to_furnace_flare: Optional[bool]
    ignition_auto_ignition: Optional[bool]
    ignition_loose_electrical_connection: Optional[bool]
    ignition_near_to_hot_surface: Optional[bool]
    ignition_static_electricity: Optional[bool]
    ignition_hammering_fall_of_object: Optional[bool]
    ignition_heat_due_to_friction: Optional[bool]
    ignition_lightning: Optional[bool]
    ignition_any_other_pyrophoric: Optional[bool]
    ignition_any_other_pyrophoric_description: Optional[str] = None

    status: Optional[str]
    updated_by: Optional[str]
