from collections import defaultdict
from sqlalchemy.orm import Session
from sqlalchemy.sql import text


# =================================================
# NEW FIELDS BLOCK — added to all master SELECTs
# jsa_id,
# sc14_additional_safety_measures,
# sc20_condition_fav_elevation_work,
# requestor_name, requestor_designation, requestor_signature,
# receiver_designation,
# renewal_requestor_name, renewal_requestor_designation, renewal_requestor_signature,
# closure_requestor_name, closure_requestor_designation, closure_requestor_signature,
# updated_by
# =================================================

NEW_FIELDS = """
            whp.jsa_id,
            whp.sc14_additional_safety_measures,
            whp.sc20_condition_fav_elevation_work,
            whp.requestor_name,
            whp.requestor_designation,
            whp.requestor_signature,
            whp.receiver_designation,
            whp.renewal_requestor_name,
            whp.renewal_requestor_designation,
            whp.renewal_requestor_signature,
            whp.closure_requestor_name,
            whp.closure_requestor_designation,
            whp.closure_requestor_signature,
            whp.updated_by
"""


def get_all_work_at_height_permits(db: Session):
    query = text(f"""
        SELECT
            whp.whp_id,
            whp.serial_number,
            'Work At Height' AS type_of_permit,
            whp.section_contractor_name,
            whp.nature_of_work,
            whp.work_from_time,
            whp.work_from_date,
            whp.work_to_time,
            whp.work_to_date,
            whp.location,

            whp.sc1_equipment_work_area_inspected,
            whp.sc2_surrounding_area_checked,
            whp.sc3_sewers_manholes_covered,
            whp.sc4_scaffolds_ladders_checked,
            whp.sc5_materials_fall_protected,
            whp.sc6_isi_marked_belts_helmets,
            whp.sc7_contractor_fit_for_height,
            whp.sc8_instructions_given,
            whp.sc9_proper_illumination,
            whp.sc10_adequate_platform_space,
            whp.sc11_proper_exit_means,
            whp.sc12_precautionary_tags_boards,
            whp.sc13_portable_equipment_earthed,
            whp.sc14_elcb_switches_provided,
            whp.sc15_standby_supervision_provided,
            whp.sc16_workers_trained_safety_belts,
            whp.sc17_operations_incharge_informed,
            whp.sc18_area_cordoned_off,
            whp.sc19_precautions_against_public_traffic,
            whp.sc20_fire_extinguisher_provided,

            whp.special_instructions,
            whp.additional_remarks,

            whp.issuer_designation,
            whp.issuer_name,
            whp.issuer_signature,

            whp.receiver_role,
            whp.receiver_name,
            whp.receiver_signature,

            whp.electrical_isolation_required,
            whp.electrical_energization_required,
            whp.toolbox_talk_required,

            whp.renewal_from_date,
            whp.renewal_from_time,
            whp.renewal_to_date,
            whp.renewal_to_time,

            whp.renewal_issuer_name,
            whp.renewal_issuer_designation,
            whp.renewal_issuer_signature,

            whp.renewal_receiver_name,
            whp.renewal_receiver_designation,
            whp.renewal_receiver_signature,

            whp.renewal_toolbox_talk,

            whp.closure_issuer_designation,
            whp.closure_issuer_name,
            whp.closure_issuer_signature,

            whp.closure_receiver_role,
            whp.closure_receiver_name,
            whp.closure_receiver_signature,

            whp.job_completion_time,
            whp.job_completion_date,
            whp.work_status,

            whp.status,
            whp.created_by,
            whp.created_at,
            whp.updated_at,

            s.station_name,

            {NEW_FIELDS}
        FROM work_at_height_permit whp
        LEFT JOIN users u ON CAST(whp.created_by AS INTEGER) = u.user_id
        LEFT JOIN station s ON u.station_id = s.station_id
        ORDER BY whp.whp_id DESC
    """)

    return db.execute(query).mappings().all()


def get_work_at_height_permit_by_id(db: Session, whp_id: int):

    master_query = text(f"""
        SELECT
            whp.whp_id,
            whp.serial_number,
            whp.section_contractor_name,
            whp.nature_of_work,
            whp.work_from_time,
            whp.work_from_date,
            whp.work_to_time,
            whp.work_to_date,
            whp.location,

            whp.sc1_equipment_work_area_inspected,
            whp.sc2_surrounding_area_checked,
            whp.sc3_sewers_manholes_covered,
            whp.sc4_scaffolds_ladders_checked,
            whp.sc5_materials_fall_protected,
            whp.sc6_isi_marked_belts_helmets,
            whp.sc7_contractor_fit_for_height,
            whp.sc8_instructions_given,
            whp.sc9_proper_illumination,
            whp.sc10_adequate_platform_space,
            whp.sc11_proper_exit_means,
            whp.sc12_precautionary_tags_boards,
            whp.sc13_portable_equipment_earthed,
            whp.sc14_elcb_switches_provided,
            whp.sc15_standby_supervision_provided,
            whp.sc16_workers_trained_safety_belts,
            whp.sc17_operations_incharge_informed,
            whp.sc18_area_cordoned_off,
            whp.sc19_precautions_against_public_traffic,
            whp.sc20_fire_extinguisher_provided,

            whp.special_instructions,
            whp.additional_remarks,

            whp.issuer_designation,
            whp.issuer_name,
            whp.issuer_signature,
            whp.issuer_userid,

            whp.requestor_name,
            whp.requestor_designation,
            whp.requestor_signature,

            whp.receiver_role,
            whp.receiver_name,
            whp.receiver_designation,
            whp.receiver_signature,
            whp.receiver_userid,

            whp.electrical_isolation_required,
            whp.electrical_energization_required,
            whp.toolbox_talk_required,

            whp.renewal_from_date,
            whp.renewal_from_time,
            whp.renewal_to_date,
            whp.renewal_to_time,

            whp.renewal_issuer_name,
            whp.renewal_issuer_designation,
            whp.renewal_issuer_signature,

            whp.renewal_requestor_name,
            whp.renewal_requestor_designation,
            whp.renewal_requestor_signature,

            whp.renewal_receiver_name,
            whp.renewal_receiver_designation,
            whp.renewal_receiver_signature,

            whp.renewal_toolbox_talk,

            whp.closure_issuer_designation,
            whp.closure_issuer_name,
            whp.closure_issuer_signature,
            whp.closure_issuer_userid,

            whp.closure_requestor_name,
            whp.closure_requestor_designation,
            whp.closure_requestor_signature,
            whp.closure_requestor_userid,

            whp.closure_receiver_role,
            whp.closure_receiver_name,
            whp.closure_receiver_signature,
            whp.closure_receiver_userid,

            whp.job_completion_time,
            whp.job_completion_date,
            whp.work_status,

            whp.status,
            whp.created_by,
            whp.updated_by,
            whp.created_at,
            whp.updated_at,

            s.station_name,


            {NEW_FIELDS}
        FROM work_at_height_permit whp
        LEFT JOIN users u ON CAST(whp.created_by AS INTEGER) = u.user_id
        LEFT JOIN station s ON u.station_id = s.station_id
        WHERE whp.whp_id = :whp_id
    """)

    master = db.execute(master_query, {"whp_id": whp_id}).mappings().first()

    if not master:
        return None

    # ── Toolbox Talks ────────────────────────────────────────
    toolbox_query = text("""
        SELECT
            whtt_id,
            work_at_height_permit_id,
            cross_reference_of_other_permit,
            work_clearance_time,
            work_clearance_date,
            contractor_engineer_name,
            work_installation_unit_facility_name,
            tbt_delivered_by,
            contract_supervisor_name,
            topics_issues_discussed,
            other_points_raised,
            created_by,
            created_at,
            updated_at
        FROM work_at_height_toolbox_talk
        WHERE work_at_height_permit_id = :whp_id
        ORDER BY whtt_id ASC
    """)

    toolbox_talks = db.execute(toolbox_query, {"whp_id": whp_id}).mappings().all()

    toolbox_talks_with_participants = []

    if toolbox_talks:
        whtt_ids = [t["whtt_id"] for t in toolbox_talks]

        participants_query = text("""
            SELECT
                whttp_id,
                toolbox_talk_id,
                participant_name,
                participant_signature,
                created_at
            FROM work_at_height_toolbox_talk_participant
            WHERE toolbox_talk_id = ANY(:whtt_ids)
            ORDER BY whttp_id ASC
        """)

        participants = db.execute(
            participants_query, {"whtt_ids": whtt_ids}
        ).mappings().all()

        participants_map = defaultdict(list)
        for p in participants:
            participants_map[p["toolbox_talk_id"]].append(dict(p))

        for talk in toolbox_talks:
            talk_dict = dict(talk)
            talk_dict["participants"] = participants_map.get(talk_dict["whtt_id"], [])
            toolbox_talks_with_participants.append(talk_dict)

    # ── Electrical Isolation Permits ─────────────────────────
    isolation_query = text("""
        SELECT
            whpis_id,
            whp_id,
            work_permit_number,
            work_clearance_time,
            work_clearance_date,
            cross_reference_of_other_permit,
            department_section_area,
            equipment_number_to_be_isolated,
            name_of_equipment_circuit,
            description_of_work,

            equipment_circuit_no,
            plant,
            work_clearance_from_time,
            work_clearance_from_date,
            loto_tag_device_no,
            authorized_person_name,
            designation,
            signature,
            isolation_method,

            issuer_name,
            issuer_designation,
            issuer_signature,
            created_by,
            created_at,
            updated_at

        FROM work_at_height_electrical_isolation_permit
        WHERE whp_id = :whp_id
        ORDER BY whpis_id ASC
    """)

    isolation_permits = db.execute(isolation_query, {"whp_id": whp_id}).mappings().all()

    # ── Electrical Energization Permits ──────────────────────
    energization_query = text("""
        SELECT
            whpep_id,
            whp_id,
            work_permit_number,
            work_clearance_time,
            work_clearance_date,
            name_of_equipment_circuit,
            department_section_area,
            equipment_number_to_be_energized,
            cross_reference_of_other_permit,

            equipment_circuit_no,
            plant,
            work_clearance_from_time,
            work_clearance_from_date,
            loto_tag_device_no,
            authorized_person_name,
            designation,
            signature,
            energization_method,

            issuer_name,
            issuer_designation,
            issuer_signature,
            created_by,
            created_at,
            updated_at

        FROM work_at_height_electrical_energization_permit
        WHERE whp_id = :whp_id
        ORDER BY whpep_id ASC
    """)

    energization_permits = db.execute(energization_query, {"whp_id": whp_id}).mappings().all()

    result = dict(master)
    result["toolbox_talks"] = toolbox_talks_with_participants
    result["isolation_permits"] = [dict(r) for r in isolation_permits]
    result["energization_permits"] = [dict(r) for r in energization_permits]

    return result


def get_work_at_height_permits_by_user_id(db: Session, user_id: int):

    master_query = text(f"""
        SELECT
            whp.whp_id,
            whp.serial_number,
            whp.section_contractor_name,
            whp.nature_of_work,
            whp.work_from_time,
            whp.work_from_date,
            whp.work_to_time,
            whp.work_to_date,
            whp.location,

            whp.sc1_equipment_work_area_inspected,
            whp.sc2_surrounding_area_checked,
            whp.sc3_sewers_manholes_covered,
            whp.sc4_scaffolds_ladders_checked,
            whp.sc5_materials_fall_protected,
            whp.sc6_isi_marked_belts_helmets,
            whp.sc7_contractor_fit_for_height,
            whp.sc8_instructions_given,
            whp.sc9_proper_illumination,
            whp.sc10_adequate_platform_space,
            whp.sc11_proper_exit_means,
            whp.sc12_precautionary_tags_boards,
            whp.sc13_portable_equipment_earthed,
            whp.sc14_elcb_switches_provided,
            whp.sc15_standby_supervision_provided,
            whp.sc16_workers_trained_safety_belts,
            whp.sc17_operations_incharge_informed,
            whp.sc18_area_cordoned_off,
            whp.sc19_precautions_against_public_traffic,
            whp.sc20_fire_extinguisher_provided,

            whp.special_instructions,
            whp.additional_remarks,

            whp.issuer_designation,
            whp.issuer_name,
            whp.issuer_signature,
            whp.issuer_userid,

            whp.requestor_name,
            whp.requestor_designation,
            whp.requestor_signature,

            whp.receiver_role,
            whp.receiver_name,
            whp.receiver_designation,
            whp.receiver_signature,
            whp.receiver_userid,

            whp.electrical_isolation_required,
            whp.electrical_energization_required,
            whp.toolbox_talk_required,

            whp.renewal_from_date,
            whp.renewal_from_time,
            whp.renewal_to_date,
            whp.renewal_to_time,

            whp.renewal_issuer_name,
            whp.renewal_issuer_designation,
            whp.renewal_issuer_signature,

            whp.renewal_requestor_name,
            whp.renewal_requestor_designation,
            whp.renewal_requestor_signature,

            whp.renewal_receiver_name,
            whp.renewal_receiver_designation,
            whp.renewal_receiver_signature,

            whp.renewal_toolbox_talk,

            whp.closure_issuer_designation,
            whp.closure_issuer_name,
            whp.closure_issuer_signature,
            whp.closure_issuer_userid,

            whp.closure_requestor_name,
            whp.closure_requestor_designation,
            whp.closure_requestor_signature,
            whp.closure_requestor_userid,

            whp.closure_receiver_role,
            whp.closure_receiver_name,
            whp.closure_receiver_signature,
            whp.closure_receiver_userid,

            whp.job_completion_time,
            whp.job_completion_date,
            whp.work_status,

            whp.status,
            whp.created_by,
            whp.updated_by,
            whp.created_at,
            whp.updated_at,

            s.station_name,

            {NEW_FIELDS}
        FROM work_at_height_permit whp
        LEFT JOIN users u ON CAST(whp.created_by AS INTEGER) = u.user_id
        LEFT JOIN station s ON u.station_id = s.station_id
        WHERE u.user_id = :user_id
        ORDER BY whp.whp_id DESC
    """)

    records = db.execute(master_query, {"user_id": user_id}).mappings().all()

    if not records:
        return []

    whp_ids = [r["whp_id"] for r in records]

    # ── Toolbox Talks ────────────────────────────────────────
    toolbox_query = text("""
        SELECT
            whtt_id, work_at_height_permit_id,
            cross_reference_of_other_permit, work_clearance_time,
            work_clearance_date, contractor_engineer_name,
            work_installation_unit_facility_name, tbt_delivered_by,
            contract_supervisor_name, topics_issues_discussed,
            other_points_raised, created_by, created_at, updated_at
        FROM work_at_height_toolbox_talk
        WHERE work_at_height_permit_id = ANY(:whp_ids)
        ORDER BY whtt_id ASC
    """)

    toolbox_talks = db.execute(toolbox_query, {"whp_ids": whp_ids}).mappings().all()

    participants_map = defaultdict(list)

    if toolbox_talks:
        whtt_ids = [t["whtt_id"] for t in toolbox_talks]

        participants_query = text("""
            SELECT whttp_id, toolbox_talk_id, participant_name,
                   participant_signature, created_at
            FROM work_at_height_toolbox_talk_participant
            WHERE toolbox_talk_id = ANY(:whtt_ids)
            ORDER BY whttp_id ASC
        """)

        participants = db.execute(
            participants_query, {"whtt_ids": whtt_ids}
        ).mappings().all()

        for p in participants:
            participants_map[p["toolbox_talk_id"]].append(dict(p))

    talks_map = defaultdict(list)
    for talk in toolbox_talks:
        talk_dict = dict(talk)
        talk_dict["participants"] = participants_map.get(talk_dict["whtt_id"], [])
        talks_map[talk_dict["work_at_height_permit_id"]].append(talk_dict)

    # ── Isolation ────────────────────────────────────────────
    isolation_query = text("""
        SELECT
            whpis_id,
            whp_id,
            work_permit_number,
            work_clearance_time,
            work_clearance_date,
            cross_reference_of_other_permit,
            department_section_area,
            equipment_number_to_be_isolated,
            name_of_equipment_circuit,
            description_of_work,

            equipment_circuit_no,
            plant,
            work_clearance_from_time,
            work_clearance_from_date,
            loto_tag_device_no,
            authorized_person_name,
            designation,
            signature,
            isolation_method,

            issuer_name,
            issuer_designation,
            issuer_signature,
            created_by,
            created_at,
            updated_at

        FROM work_at_height_electrical_isolation_permit
        WHERE whp_id = ANY(:whp_ids)
        ORDER BY whpis_id ASC
    """)

    isolation_permits = db.execute(isolation_query, {"whp_ids": whp_ids}).mappings().all()

    isolation_map = defaultdict(list)
    for ip in isolation_permits:
        isolation_map[ip["whp_id"]].append(dict(ip))

    # ── Energization ─────────────────────────────────────────
    energization_query = text("""
        SELECT
            whpep_id,
            whp_id,
            work_permit_number,
            work_clearance_time,
            work_clearance_date,
            name_of_equipment_circuit,
            department_section_area,
            equipment_number_to_be_energized,
            cross_reference_of_other_permit,

            equipment_circuit_no,
            plant,
            work_clearance_from_time,
            work_clearance_from_date,
            loto_tag_device_no,
            authorized_person_name,
            designation,
            signature,
            energization_method,

            issuer_name,
            issuer_designation,
            issuer_signature,
            created_by,
            created_at,
            updated_at

        FROM work_at_height_electrical_energization_permit
        WHERE whp_id = ANY(:whp_ids)
        ORDER BY whpep_id ASC
    """)

    energization_permits = db.execute(energization_query, {"whp_ids": whp_ids}).mappings().all()

    energization_map = defaultdict(list)
    for ep in energization_permits:
        energization_map[ep["whp_id"]].append(dict(ep))

    results = []
    for record in records:
        r = dict(record)
        wid = r["whp_id"]
        r["toolbox_talks"] = talks_map.get(wid, [])
        r["isolation_permits"] = isolation_map.get(wid, [])
        r["energization_permits"] = energization_map.get(wid, [])
        results.append(r)

    return results


def get_all_work_at_height_full(db: Session):

    master_query = text("""
        SELECT
            whp.*,
            'Work at Height' AS type_of_permit,
            s.station_name
        FROM work_at_height_permit whp
        LEFT JOIN users u ON CAST(whp.created_by AS INTEGER) = u.user_id
        LEFT JOIN station s ON u.station_id = s.station_id
        ORDER BY whp.whp_id DESC
    """)
    # ✅ get_all_work_at_height_full uses whp.* so all new columns
    # are already included automatically — no change needed here

    records = db.execute(master_query).mappings().all()

    if not records:
        return []

    whp_ids = [r["whp_id"] for r in records]

    toolbox_query = text("""
        SELECT *
        FROM work_at_height_toolbox_talk
        WHERE work_at_height_permit_id = ANY(:whp_ids)
        ORDER BY whtt_id ASC
    """)

    toolbox_talks = db.execute(toolbox_query, {"whp_ids": whp_ids}).mappings().all()

    participants_map = defaultdict(list)

    if toolbox_talks:
        whtt_ids = [t["whtt_id"] for t in toolbox_talks]

        participants_query = text("""
            SELECT *
            FROM work_at_height_toolbox_talk_participant
            WHERE toolbox_talk_id = ANY(:whtt_ids)
        """)

        participants = db.execute(
            participants_query, {"whtt_ids": whtt_ids}
        ).mappings().all()

        for p in participants:
            participants_map[p["toolbox_talk_id"]].append(dict(p))

    talks_map = defaultdict(list)
    for talk in toolbox_talks:
        talk_dict = dict(talk)
        talk_dict["participants"] = participants_map.get(talk_dict["whtt_id"], [])
        talks_map[talk_dict["work_at_height_permit_id"]].append(talk_dict)

    isolation_query = text("""
        SELECT *
        FROM work_at_height_electrical_isolation_permit
        WHERE whp_id = ANY(:whp_ids)
    """)

    isolation = db.execute(isolation_query, {"whp_ids": whp_ids}).mappings().all()

    isolation_map = defaultdict(list)
    for i in isolation:
        isolation_map[i["whp_id"]].append(dict(i))

    energization_query = text("""
        SELECT *
        FROM work_at_height_electrical_energization_permit
        WHERE whp_id = ANY(:whp_ids)
    """)

    energization = db.execute(energization_query, {"whp_ids": whp_ids}).mappings().all()

    energization_map = defaultdict(list)
    for e in energization:
        energization_map[e["whp_id"]].append(dict(e))

    results = []
    for r in records:
        row = dict(r)
        wid = row["whp_id"]
        row["toolbox_talks"] = talks_map.get(wid, [])
        row["isolation_permits"] = isolation_map.get(wid, [])
        row["energization_permits"] = energization_map.get(wid, [])
        results.append(row)

    return results