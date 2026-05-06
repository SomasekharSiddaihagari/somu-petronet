from sqlalchemy.orm import Session
from sqlalchemy.sql import text
from collections import defaultdict

def get_all_cwp(db: Session):
    query = text("""
        SELECT
            cwp.cwp_id,
            cwp.serial_number,
            'Composite Work' AS type_of_permit,     
            cwp.location,
            cwp.issued_to,
            cwp.description_of_work,
            cwp.work_from_time,
            cwp.work_from_date,
            cwp.work_to_time,
            cwp.work_to_date,
            cwp.jsa_id,
            cwp.jsa_ref_no,
            cwp.job_type,
            cwp.cross_reference_permits,
            cwp.isolation_certificate_ref,

            cwp.a1_equipment_area_inspected,
            cwp.a1_sub_equipment,
            cwp.a1_sub_work_area,
            cwp.a2_surrounding_area_checked,
            cwp.a3_sewers_manholes_covered,
            cwp.a3_sub_sewers,
            cwp.a3_sub_manholes,
            cwp.a3_sub_cbd,
            cwp.a3_sub_hot_surface,
            cwp.a3_sub_other,
            cwp.a3_sub_other_text,
            cwp.a4_hazards_considered,
            cwp.a5_equipment_drained,
            cwp.a6_equipment_steamed_purged,
            cwp.a6_sub_steamed,
            cwp.a6_sub_purged,
            cwp.a7_equipment_blinded_isolated,
            cwp.a7_sub_blinded,
            cwp.a7_sub_disconnected,
            cwp.a7_sub_closed,
            cwp.a7_sub_isolated,
            cwp.a7_sub_wedge_opened,
            cwp.a8_equipment_water_flushed,
            cwp.a9_iron_sulphide_removed,
            cwp.a9_sub_sulphide_removed,
            cwp.a9_sub_kept_wet,
            cwp.a10_equipment_electrically_isolated,
            cwp.a11_gas_test,
            cwp.a11_val_hcs_percent,
            cwp.a11_val_toxic_gas_ppm,
            cwp.a11_val_o2_percent,
            cwp.a12_fire_extinguisher_provided,
            cwp.a12_sub_running_water_hose,
            cwp.a12_sub_fire_extinguisher,
            cwp.a12_sub_fire_water_system,
            cwp.a13_area_cordoned,
            cwp.a14_ventilation_lighting,

            cwp.b1_escape_provided,
            cwp.b2_standby_personnel,
            cwp.b2_sub_process,
            cwp.b2_sub_maint,
            cwp.b2_sub_contractor,
            cwp.b2_sub_fire_dept,
            cwp.b3_check_oil_gas_trapped,
            cwp.b4_shield_against_spark,
            cwp.b5_portable_equipment_grounded,
            cwp.b6_standby_for_confined_space,

            cwp.c1_peso_spark_elimination,
            cwp.c1_sub_mobile_equipment,
            cwp.c1_sub_vehicle_provided,

            cwp.d1_excavation_clearance_obtained,
            cwp.d1_sub_excavation,
            cwp.d1_sub_road_cutting,
            cwp.d1_sub_dyke_cutting,

            cwp.hazard_lack_of_o2,
            cwp.hazard_lack_of_h2s,
            cwp.hazard_toxic_gases,
            cwp.hazard_combustible_gases,
            cwp.hazard_pyrophoric_iron,
            cwp.hazard_corrosive_chemicals,
            cwp.hazard_steam_condensate,
            cwp.hazard_other,
            cwp.hazard_other_text,

            cwp.ppe_helmet,
            cwp.ppe_safety_shoes,
            cwp.ppe_hand_gloves,
            cwp.ppe_boiler_suit,
            cwp.ppe_cotton_coverall,
            cwp.ppe_face_shield,
            cwp.ppe_fresh_air_mask,
            cwp.ppe_dust_respirator,
            cwp.ppe_apron,
            cwp.ppe_goggles,
            cwp.ppe_earmuff,
            cwp.ppe_lifeline,
            cwp.ppe_safety_belt,
            cwp.ppe_airline,
            cwp.ppe_other,
            cwp.ppe_other_text,

            cwp.additional_requirements_precautions,

            cwp.requestor_name,
            cwp.requestor_designation,
            cwp.requestor_signature,

            cwp.issuer_name,
            cwp.issuer_designation,
            cwp.issuer_signature,

            cwp.receiver_name,
            cwp.receiver_designation,
            cwp.receiver_signature,

            cwp.electrical_isolation_required,
            cwp.electrical_energization_required,

            cwp.toolbox_talk_completed,

            cwp.gas_test_from_time,
            cwp.gas_test_to_time,
            cwp.gas_test_from_date,
            cwp.gas_test_to_date,
            cwp.gas_hcs_percent,
            cwp.gas_toxic_ppm,
            cwp.gas_o2_percent,
            cwp.gas_additional_precautions,

            cwp.gas_requestor_name,
            cwp.gas_requestor_designation,
            cwp.gas_requestor_signature,

            cwp.gas_issuer_name,
            cwp.gas_issuer_designation,
            cwp.gas_issuer_signature,

            cwp.gas_receiver_name,
            cwp.gas_receiver_designation,
            cwp.gas_receiver_signature,

            cwp.closure_requestor_name,
            cwp.closure_requestor_designation,
            cwp.closure_requestor_signature,

            cwp.closure_issuer_name,
            cwp.closure_issuer_designation,
            cwp.closure_issuer_signature,

            cwp.closure_receiver_name,
            cwp.closure_receiver_designation,
            cwp.closure_receiver_signature,

            cwp.status,
            cwp.created_by,
            cwp.updated_by,
            cwp.created_at,
            cwp.updated_at,

            s.station_name
        FROM composite_work_permit cwp
        LEFT JOIN users u ON cwp.created_by = CAST(u.user_id AS VARCHAR)
        LEFT JOIN station s ON u.station_id = s.station_id
        ORDER BY cwp.cwp_id DESC
    """)

    return db.execute(query).mappings().all()


def get_cwp_by_id(db: Session, cwp_id: int):

    # ── Master ──────────────────────────────────────────────
    master_query = text("""
        SELECT
            cwp.cwp_id,
            cwp.serial_number,
            cwp.location,
            cwp.issued_to,
            cwp.description_of_work,
            cwp.work_from_time,
            cwp.work_from_date,
            cwp.work_to_time,
            cwp.work_to_date,
            cwp.jsa_id,
            cwp.jsa_ref_no,
            cwp.job_type,
            cwp.cross_reference_permits,
            cwp.isolation_certificate_ref,

            cwp.a1_equipment_area_inspected,
            cwp.a1_sub_equipment,
            cwp.a1_sub_work_area,
            cwp.a2_surrounding_area_checked,
            cwp.a3_sewers_manholes_covered,
            cwp.a3_sub_sewers,
            cwp.a3_sub_manholes,
            cwp.a3_sub_cbd,
            cwp.a3_sub_hot_surface,
            cwp.a3_sub_other,
            cwp.a3_sub_other_text,
            cwp.a4_hazards_considered,
            cwp.a5_equipment_drained,
            cwp.a6_equipment_steamed_purged,
            cwp.a6_sub_steamed,
            cwp.a6_sub_purged,
            cwp.a7_equipment_blinded_isolated,
            cwp.a7_sub_blinded,
            cwp.a7_sub_disconnected,
            cwp.a7_sub_closed,
            cwp.a7_sub_isolated,
            cwp.a7_sub_wedge_opened,
            cwp.a8_equipment_water_flushed,
            cwp.a9_iron_sulphide_removed,
            cwp.a9_sub_sulphide_removed,
            cwp.a9_sub_kept_wet,
            cwp.a10_equipment_electrically_isolated,
            cwp.a11_gas_test,
            cwp.a11_val_hcs_percent,
            cwp.a11_val_toxic_gas_ppm,
            cwp.a11_val_o2_percent,
            cwp.a12_fire_extinguisher_provided,
            cwp.a12_sub_running_water_hose,
            cwp.a12_sub_fire_extinguisher,
            cwp.a12_sub_fire_water_system,
            cwp.a13_area_cordoned,
            cwp.a14_ventilation_lighting,

            cwp.b1_escape_provided,
            cwp.b2_standby_personnel,
            cwp.b2_sub_process,
            cwp.b2_sub_maint,
            cwp.b2_sub_contractor,
            cwp.b2_sub_fire_dept,
            cwp.b3_check_oil_gas_trapped,
            cwp.b4_shield_against_spark,
            cwp.b5_portable_equipment_grounded,
            cwp.b6_standby_for_confined_space,

            cwp.c1_peso_spark_elimination,
            cwp.c1_sub_mobile_equipment,
            cwp.c1_sub_vehicle_provided,

            cwp.d1_excavation_clearance_obtained,
            cwp.d1_sub_excavation,
            cwp.d1_sub_road_cutting,
            cwp.d1_sub_dyke_cutting,

            cwp.hazard_lack_of_o2,
            cwp.hazard_lack_of_h2s,
            cwp.hazard_toxic_gases,
            cwp.hazard_combustible_gases,
            cwp.hazard_pyrophoric_iron,
            cwp.hazard_corrosive_chemicals,
            cwp.hazard_steam_condensate,
            cwp.hazard_other,
            cwp.hazard_other_text,

            cwp.ppe_helmet,
            cwp.ppe_safety_shoes,
            cwp.ppe_hand_gloves,
            cwp.ppe_boiler_suit,
            cwp.ppe_cotton_coverall,
            cwp.ppe_face_shield,
            cwp.ppe_fresh_air_mask,
            cwp.ppe_dust_respirator,
            cwp.ppe_apron,
            cwp.ppe_goggles,
            cwp.ppe_earmuff,
            cwp.ppe_lifeline,
            cwp.ppe_safety_belt,
            cwp.ppe_airline,
            cwp.ppe_other,
            cwp.ppe_other_text,

            cwp.additional_requirements_precautions,

            cwp.requestor_name,
            cwp.requestor_designation,
            cwp.requestor_signature,

            cwp.issuer_name,
            cwp.issuer_designation,
            cwp.issuer_signature,
            cwp.issuer_userid,

            cwp.receiver_name,
            cwp.receiver_designation,
            cwp.receiver_signature,
            cwp.receiver_userid,

            cwp.electrical_isolation_required,
            cwp.electrical_energization_required,

            cwp.toolbox_talk_completed,

            cwp.gas_test_from_time,
            cwp.gas_test_to_time,
            cwp.gas_test_from_date,
            cwp.gas_test_to_date,
            cwp.gas_hcs_percent,
            cwp.gas_toxic_ppm,
            cwp.gas_o2_percent,
            cwp.gas_additional_precautions,

            cwp.gas_requestor_name,
            cwp.gas_requestor_designation,
            cwp.gas_requestor_signature,
            cwp.gas_requestor_userid,

            cwp.gas_issuer_name,
            cwp.gas_issuer_designation,
            cwp.gas_issuer_signature,
            cwp.gas_issuer_userid,

            cwp.gas_receiver_name,
            cwp.gas_receiver_designation,
            cwp.gas_receiver_signature,
            cwp.gas_receiver_userid,

            cwp.closure_requestor_name,
            cwp.closure_requestor_designation,
            cwp.closure_requestor_signature,
            cwp.closure_requestor_userid,

            cwp.closure_issuer_name,
            cwp.closure_issuer_designation,
            cwp.closure_issuer_signature,
            cwp.closure_issuer_userid,

            cwp.closure_receiver_name,
            cwp.closure_receiver_designation,
            cwp.closure_receiver_signature,
            cwp.closure_receiver_userid,

            cwp.status,
            cwp.created_by,
            cwp.updated_by,
            cwp.created_at,
            cwp.updated_at
        FROM composite_work_permit cwp
        LEFT JOIN users u ON cwp.created_by = CAST(u.user_id AS VARCHAR)
        LEFT JOIN station s ON u.station_id = s.station_id
        WHERE cwp.cwp_id = :cwp_id
    """)

    master = db.execute(master_query, {"cwp_id": cwp_id}).mappings().first()

    if not master:
        return None

    # ── Toolbox Talks ────────────────────────────────────────
    toolbox_query = text("""
        SELECT
            ctt_id,
            composite_work_permit_id,
            cross_reference_of_other_permit,
            work_clearance_time,
            work_clearance_date,
            contractor_engineer_name,
            work_installation_unit_facility_name,
            tbt_delivered_by,
            contract_supervisor_name,
            topics_issues_discussed,
            other_points_raised,
            status,
            created_by,
            created_at,
            updated_at
        FROM composite_toolbox_talk
        WHERE composite_work_permit_id = :cwp_id
        ORDER BY ctt_id ASC
    """)

    toolbox_talks = db.execute(
        toolbox_query, {"cwp_id": cwp_id}
    ).mappings().all()

    # ── Toolbox Talk Participants ────────────────────────────
    toolbox_talks_with_participants = []

    if toolbox_talks:
        ctt_ids = [t["ctt_id"] for t in toolbox_talks]

        participants_query = text("""
            SELECT
                cttp_id,
                toolbox_talk_id,
                participant_name,
                participant_signature,
                created_at
            FROM composite_toolbox_talk_participant
            WHERE toolbox_talk_id = ANY(:ctt_ids)
            ORDER BY cttp_id ASC
        """)

        participants = db.execute(
            participants_query, {"ctt_ids": ctt_ids}
        ).mappings().all()

        participants_map = defaultdict(list)
        for p in participants:
            participants_map[p["toolbox_talk_id"]].append(dict(p))

        for talk in toolbox_talks:
            talk_dict = dict(talk)
            talk_dict["participants"] = participants_map.get(talk_dict["ctt_id"], [])
            toolbox_talks_with_participants.append(talk_dict)
    
    # ── Electrical Isolation Permits ─────────────────────────
    isolation_query = text("""
        SELECT
            ceip_id,
            composite_work_permit_id,
            work_permit_number,
            work_clearance_time,
            work_clearance_date,
            cross_reference_of_other_permit,
            department_section_area,
            equipment_number_to_be_isolated,
            name_of_equipment_circuit,
            description_of_work,
            issuer_name,
            issuer_designation,
            issuer_signature,
            status,
            created_by,
            created_at,
            updated_at,
            equipment_circuit_no,
            plant,
            work_clearance_from_time,
            work_clearance_from_date,
            isolation_method,
            loto_tag_device_no,
            authorized_person_name,
            designation,
            signature
        FROM composite_electrical_isolation_permit
        WHERE composite_work_permit_id = :cwp_id
        ORDER BY ceip_id ASC
    """)

    isolation_permits = db.execute(
        isolation_query, {"cwp_id": cwp_id}
    ).mappings().all()

    # ── Electrical Energization Permits ──────────────────────
    energization_query = text("""
        SELECT
            ceep_id,
            composite_work_permit_id,
            work_permit_number,
            work_clearance_time,
            work_clearance_date,
            name_of_equipment_circuit,
            department_section_area,
            equipment_number_to_be_energized,
            cross_reference_of_other_permit,
            issuer_name,
            issuer_designation,
            issuer_signature,
            status,
            created_by,
            created_at,
            updated_at,
            equipment_circuit_no,
            plant,
            work_clearance_from_time,
            work_clearance_from_date,
            energization_method,
            loto_tag_device_no,
            authorized_person_name,
            designation,
            signature
        FROM composite_electrical_energization_permit
        WHERE composite_work_permit_id = :cwp_id
        ORDER BY ceep_id ASC
    """)

    energization_permits = db.execute(
        energization_query, {"cwp_id": cwp_id}
    ).mappings().all()

    # ── Merge & return ───────────────────────────────────────
    result = dict(master)
    result["toolbox_talks"] = toolbox_talks_with_participants
    result["isolation_permits"] = [dict(r) for r in isolation_permits]
    result["energization_permits"] = [dict(r) for r in energization_permits]

    return result


def get_cwp_by_user_id(db: Session, user_id: int):

    # ── Master ──────────────────────────────────────────────
    master_query = text("""
        SELECT
            cwp.cwp_id,
            cwp.serial_number,
            cwp.location,
            cwp.issued_to,
            cwp.description_of_work,
            cwp.work_from_time,
            cwp.work_from_date,
            cwp.work_to_time,
            cwp.work_to_date,
            cwp.jsa_id,
            cwp.jsa_ref_no,
            cwp.job_type,
            cwp.cross_reference_permits,
            cwp.isolation_certificate_ref,

            cwp.a1_equipment_area_inspected,
            cwp.a1_sub_equipment,
            cwp.a1_sub_work_area,
            cwp.a2_surrounding_area_checked,
            cwp.a3_sewers_manholes_covered,
            cwp.a3_sub_sewers,
            cwp.a3_sub_manholes,
            cwp.a3_sub_cbd,
            cwp.a3_sub_hot_surface,
            cwp.a3_sub_other,
            cwp.a3_sub_other_text,
            cwp.a4_hazards_considered,
            cwp.a5_equipment_drained,
            cwp.a6_equipment_steamed_purged,
            cwp.a6_sub_steamed,
            cwp.a6_sub_purged,
            cwp.a7_equipment_blinded_isolated,
            cwp.a7_sub_blinded,
            cwp.a7_sub_disconnected,
            cwp.a7_sub_closed,
            cwp.a7_sub_isolated,
            cwp.a7_sub_wedge_opened,
            cwp.a8_equipment_water_flushed,
            cwp.a9_iron_sulphide_removed,
            cwp.a9_sub_sulphide_removed,
            cwp.a9_sub_kept_wet,
            cwp.a10_equipment_electrically_isolated,
            cwp.a11_gas_test,
            cwp.a11_val_hcs_percent,
            cwp.a11_val_toxic_gas_ppm,
            cwp.a11_val_o2_percent,
            cwp.a12_fire_extinguisher_provided,
            cwp.a12_sub_running_water_hose,
            cwp.a12_sub_fire_extinguisher,
            cwp.a12_sub_fire_water_system,
            cwp.a13_area_cordoned,
            cwp.a14_ventilation_lighting,

            cwp.b1_escape_provided,
            cwp.b2_standby_personnel,
            cwp.b2_sub_process,
            cwp.b2_sub_maint,
            cwp.b2_sub_contractor,
            cwp.b2_sub_fire_dept,
            cwp.b3_check_oil_gas_trapped,
            cwp.b4_shield_against_spark,
            cwp.b5_portable_equipment_grounded,
            cwp.b6_standby_for_confined_space,

            cwp.c1_peso_spark_elimination,
            cwp.c1_sub_mobile_equipment,
            cwp.c1_sub_vehicle_provided,

            cwp.d1_excavation_clearance_obtained,
            cwp.d1_sub_excavation,
            cwp.d1_sub_road_cutting,
            cwp.d1_sub_dyke_cutting,

            cwp.hazard_lack_of_o2,
            cwp.hazard_lack_of_h2s,
            cwp.hazard_toxic_gases,
            cwp.hazard_combustible_gases,
            cwp.hazard_pyrophoric_iron,
            cwp.hazard_corrosive_chemicals,
            cwp.hazard_steam_condensate,
            cwp.hazard_other,
            cwp.hazard_other_text,

            cwp.ppe_helmet,
            cwp.ppe_safety_shoes,
            cwp.ppe_hand_gloves,
            cwp.ppe_boiler_suit,
            cwp.ppe_cotton_coverall,
            cwp.ppe_face_shield,
            cwp.ppe_fresh_air_mask,
            cwp.ppe_dust_respirator,
            cwp.ppe_apron,
            cwp.ppe_goggles,
            cwp.ppe_earmuff,
            cwp.ppe_lifeline,
            cwp.ppe_safety_belt,
            cwp.ppe_airline,
            cwp.ppe_other,
            cwp.ppe_other_text,

            cwp.additional_requirements_precautions,

            cwp.requestor_name,
            cwp.requestor_designation,
            cwp.requestor_signature,

            cwp.issuer_name,
            cwp.issuer_designation,
            cwp.issuer_signature,
            cwp.issuer_userid,

            cwp.receiver_name,
            cwp.receiver_designation,
            cwp.receiver_signature,
            cwp.receiver_userid,

            cwp.electrical_isolation_required,
            cwp.electrical_energization_required,

            cwp.toolbox_talk_completed,

            cwp.gas_test_from_time,
            cwp.gas_test_to_time,
            cwp.gas_test_from_date,
            cwp.gas_test_to_date,
            cwp.gas_hcs_percent,
            cwp.gas_toxic_ppm,
            cwp.gas_o2_percent,
            cwp.gas_additional_precautions,

            cwp.gas_requestor_name,
            cwp.gas_requestor_designation,
            cwp.gas_requestor_signature,
            cwp.gas_requestor_userid,

            cwp.gas_issuer_name,
            cwp.gas_issuer_designation,
            cwp.gas_issuer_signature,
            cwp.gas_issuer_userid,

            cwp.gas_receiver_name,
            cwp.gas_receiver_designation,
            cwp.gas_receiver_signature,
            cwp.gas_receiver_userid,

            cwp.closure_requestor_name,
            cwp.closure_requestor_designation,
            cwp.closure_requestor_signature,
            cwp.closure_requestor_userid,

            cwp.closure_issuer_name,
            cwp.closure_issuer_designation,
            cwp.closure_issuer_signature,
            cwp.closure_issuer_userid,

            cwp.closure_receiver_name,
            cwp.closure_receiver_designation,
            cwp.closure_receiver_signature,
            cwp.closure_receiver_userid,

            cwp.status,
            cwp.created_by,
            cwp.updated_by,
            cwp.created_at,
            cwp.updated_at
        FROM composite_work_permit cwp
        LEFT JOIN users u ON cwp.created_by = CAST(u.user_id AS VARCHAR)
        LEFT JOIN station s ON u.station_id = s.station_id
        WHERE u.user_id = :user_id
        ORDER BY cwp.cwp_id DESC
    """)

    records = db.execute(master_query, {"user_id": user_id}).mappings().all()

    if not records:
        return []

    # ── Collect all cwp_ids ──────────────────────────────────
    cwp_ids = [r["cwp_id"] for r in records]

    # ── Toolbox Talks for all CWPs ───────────────────────────
    toolbox_query = text("""
        SELECT
            ctt_id,
            composite_work_permit_id,
            cross_reference_of_other_permit,
            work_clearance_time,
            work_clearance_date,
            contractor_engineer_name,
            work_installation_unit_facility_name,
            tbt_delivered_by,
            contract_supervisor_name,
            topics_issues_discussed,
            other_points_raised,
            status,
            created_by,
            created_at,
            updated_at
        FROM composite_toolbox_talk
        WHERE composite_work_permit_id = ANY(:cwp_ids)
        ORDER BY ctt_id ASC
    """)

    toolbox_talks = db.execute(
        toolbox_query, {"cwp_ids": cwp_ids}
    ).mappings().all()

    # ── Participants for all Toolbox Talks ───────────────────
    participants_map = defaultdict(list)

    if toolbox_talks:
        ctt_ids = [t["ctt_id"] for t in toolbox_talks]

        participants_query = text("""
            SELECT
                cttp_id,
                toolbox_talk_id,
                participant_name,
                participant_signature,
                created_at
            FROM composite_toolbox_talk_participant
            WHERE toolbox_talk_id = ANY(:ctt_ids)
            ORDER BY cttp_id ASC
        """)

        participants = db.execute(
            participants_query, {"ctt_ids": ctt_ids}
        ).mappings().all()

        for p in participants:
            participants_map[p["toolbox_talk_id"]].append(dict(p))

    # Group toolbox talks by cwp_id
    talks_map = defaultdict(list)
    for talk in toolbox_talks:
        talk_dict = dict(talk)
        talk_dict["participants"] = participants_map.get(talk_dict["ctt_id"], [])
        talks_map[talk_dict["composite_work_permit_id"]].append(talk_dict)

    # ── Isolation Permits for all CWPs ───────────────────────
    isolation_query = text("""
        SELECT
            ceip_id,
            composite_work_permit_id,
            work_permit_number,
            work_clearance_time,
            work_clearance_date,
            cross_reference_of_other_permit,
            department_section_area,
            equipment_number_to_be_isolated,
            name_of_equipment_circuit,
            description_of_work,
            issuer_name,
            issuer_designation,
            issuer_signature,
            status,
            created_by,
            created_at,
            updated_at,
            equipment_circuit_no,
            plant,
            work_clearance_from_time,
            work_clearance_from_date,
            isolation_method,
            loto_tag_device_no,
            authorized_person_name,
            designation,
            signature
        FROM composite_electrical_isolation_permit
        WHERE composite_work_permit_id = ANY(:cwp_ids)
        ORDER BY ceip_id ASC
    """)

    isolation_permits = db.execute(
        isolation_query, {"cwp_ids": cwp_ids}
    ).mappings().all()

    isolation_map = defaultdict(list)
    for ip in isolation_permits:
        isolation_map[ip["composite_work_permit_id"]].append(dict(ip))

    # ── Energization Permits for all CWPs ────────────────────
    energization_query = text("""
        SELECT
            ceep_id,
            composite_work_permit_id,
            work_permit_number,
            work_clearance_time,
            work_clearance_date,
            name_of_equipment_circuit,
            department_section_area,
            equipment_number_to_be_energized,
            cross_reference_of_other_permit,
            issuer_name,
            issuer_designation,
            issuer_signature,
            status,
            created_by,
            created_at,
            updated_at,
            equipment_circuit_no,
            plant,
            work_clearance_from_time,
            work_clearance_from_date,
            energization_method,
            loto_tag_device_no,
            authorized_person_name,
            designation,
            signature
        FROM composite_electrical_energization_permit
        WHERE composite_work_permit_id = ANY(:cwp_ids)
        ORDER BY ceep_id ASC
    """)

    energization_permits = db.execute(
        energization_query, {"cwp_ids": cwp_ids}
    ).mappings().all()

    energization_map = defaultdict(list)
    for ep in energization_permits:
        energization_map[ep["composite_work_permit_id"]].append(dict(ep))

    # ── Merge & return ───────────────────────────────────────
    results = []
    for record in records:
        r = dict(record)
        cid = r["cwp_id"]
        r["toolbox_talks"] = talks_map.get(cid, [])
        r["isolation_permits"] = isolation_map.get(cid, [])
        r["energization_permits"] = energization_map.get(cid, [])
        results.append(r)

    return results


def get_all_cwp_full(db: Session):

    # ── MASTER ──────────────────────────────────────────────
    master_query = text("""
        SELECT
            cwp.*,
            'Composite Work' AS type_of_permit,            
            s.station_name
        FROM composite_work_permit cwp
        LEFT JOIN users u ON cwp.created_by = CAST(u.user_id AS VARCHAR)
        LEFT JOIN station s ON u.station_id = s.station_id
        ORDER BY cwp.cwp_id DESC
    """)

    records = db.execute(master_query).mappings().all()

    if not records:
        return []

    # ── Collect IDs ─────────────────────────────────────────
    cwp_ids = [r["cwp_id"] for r in records]

    # ── TOOLBOX TALKS ───────────────────────────────────────
    toolbox_query = text("""
        SELECT *
        FROM composite_toolbox_talk
        WHERE composite_work_permit_id = ANY(:cwp_ids)
        ORDER BY ctt_id ASC
    """)

    toolbox_talks = db.execute(
        toolbox_query, {"cwp_ids": cwp_ids}
    ).mappings().all()

    # ── PARTICIPANTS ────────────────────────────────────────
    participants_map = defaultdict(list)

    if toolbox_talks:
        ctt_ids = [t["ctt_id"] for t in toolbox_talks]

        participants_query = text("""
            SELECT *
            FROM composite_toolbox_talk_participant
            WHERE toolbox_talk_id = ANY(:ctt_ids)
        """)

        participants = db.execute(
            participants_query, {"ctt_ids": ctt_ids}
        ).mappings().all()

        for p in participants:
            participants_map[p["toolbox_talk_id"]].append(dict(p))

    talks_map = defaultdict(list)
    for talk in toolbox_talks:
        talk_dict = dict(talk)
        talk_dict["participants"] = participants_map.get(talk_dict["ctt_id"], [])
        talks_map[talk_dict["composite_work_permit_id"]].append(talk_dict)

    # ── ISOLATION ───────────────────────────────────────────
    isolation_query = text("""
        SELECT *
        FROM composite_electrical_isolation_permit
        WHERE composite_work_permit_id = ANY(:cwp_ids)
    """)

    isolation = db.execute(
        isolation_query, {"cwp_ids": cwp_ids}
    ).mappings().all()

    isolation_map = defaultdict(list)
    for i in isolation:
        isolation_map[i["composite_work_permit_id"]].append(dict(i))

    # ── ENERGIZATION ────────────────────────────────────────
    energization_query = text("""
        SELECT *
        FROM composite_electrical_energization_permit
        WHERE composite_work_permit_id = ANY(:cwp_ids)
    """)

    energization = db.execute(
        energization_query, {"cwp_ids": cwp_ids}
    ).mappings().all()

    energization_map = defaultdict(list)
    for e in energization:
        energization_map[e["composite_work_permit_id"]].append(dict(e))

   # ── FINAL MERGE ─────────────────────────────────────────────
    results = []
    for r in records:
        row = dict(r)
        cid = row["cwp_id"]

        station_name = row.get("station_name")
        receiver_name = row.get("receiver_name")

        talks = talks_map.get(cid, [])
        
        isolation = isolation_map.get(cid, [])
        for ip in isolation:
            ip["station_name"] = station_name
            ip["receiver_name"] = receiver_name

        energization = energization_map.get(cid, [])
        for ep in energization:
            ep["station_name"] = station_name
            ep["receiver_name"] = receiver_name

        row["toolbox_talks"] = talks
        row["isolation_permits"] = isolation
        row["energization_permits"] = energization

        results.append(row)

    return results
