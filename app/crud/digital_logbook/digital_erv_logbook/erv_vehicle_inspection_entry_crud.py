from sqlalchemy.orm import Session
from sqlalchemy import text
from datetime import datetime
from app.schemas.digital_logbook.digital_erv_logbook.erv_vehicle_inspection_entry_schema import (
    ERVVehicleInspectionCreate,
    ERVVehicleInspectionUpdate,
)

# ------------------------------------------------------------------------------
# INTERNAL HELPERS
# ------------------------------------------------------------------------------


def _log_erv_entry_history(db: Session, record: dict, action: str, user_id: int = None):
    """
    Archives a snapshot of the vehicle inspection entry record.
    SQL Query matches original string exactly.
    """
    history_record = dict(record)
    history_record["action_type"] = action

    # Remove dynamic name resolution fields if present
    history_record.pop("created_by_name", None)
    history_record.pop("updated_by_name", None)

    # For DELETE, track who deleted it and when.
    # For UPDATE, preserve the original record's update metadata for the snapshot.
    if action == "DELETE":
        history_record["updated_at"] = datetime.now()
        history_record["updated_by"] = (
            user_id if user_id else history_record.get("updated_by")
        )

    query = text(
        """
        INSERT INTO erv_vehicle_inspection_log_history (
            evi_id, category_master_id, inspection_date, vehicle_no, diesel,
            kilometer_reading, trail_run_kilometer, cleaning,
            head_lamp_condition, siren_condition, vhf_set_condition,
            brake_condition, tyre_condition, battery_voltage_condition,
            hydraulic_oil_level, hydraulic_tank_line_condition,
            rto_condition, ball_valve_condition, number_of_hose_pipe,
            hose_pipe_condition, any_observation, remarks,
            driver_signature, technician_signature, shift_in_charge_signature,
            created_at, created_by, updated_at, updated_by, action_type
        ) VALUES (
            :evi_id, :category_master_id, :inspection_date, :vehicle_no, :diesel,
            :kilometer_reading, :trail_run_kilometer, :cleaning,
            :head_lamp_condition, :siren_condition, :vhf_set_condition,
            :brake_condition, :tyre_condition, :battery_voltage_condition,
            :hydraulic_oil_level, :hydraulic_tank_line_condition,
            :rto_condition, :ball_valve_condition, :number_of_hose_pipe,
            :hose_pipe_condition, :any_observation, :remarks,
            :driver_signature, :technician_signature, :shift_in_charge_signature,
            :created_at, :created_by, :updated_at, :updated_by, :action_type
        )
    """
    )
    db.execute(query, history_record)


def _clean_entry_signatures(data: dict):
    """Strips whitespace from signature fields if present."""
    sigs = ["driver_signature", "technician_signature", "shift_in_charge_signature"]
    for sig in sigs:
        if sig in data and data[sig]:
            data[sig] = data[sig].strip()
    return data


# ------------------------------------------------------------------------------
# MAIN CRUD OPERATIONS
# ------------------------------------------------------------------------------


def _process_entry_result(db: Session, result):
    """Dynamic resolution of user names without storing them in the table."""
    if not result:
        return None
    d = dict(result)

    # Names are fetched in the SQL query using subqueries or joins,
    # but we handle fallback here if needed.
    return d


def get_erv_vehicle_entries_by_master_id(db: Session, master_id: int):
    """Fetches all inspection entries for a master logbook with dynamic names."""
    query = text(
        """
        SELECT 
            evi.*,
            (SELECT TRIM(CONCAT(first_name, ' ', last_name)) FROM users WHERE user_id = evi.created_by) as created_by_name,
            (SELECT TRIM(CONCAT(first_name, ' ', last_name)) FROM users WHERE user_id = evi.updated_by) as updated_by_name,
            COALESCE(evi.created_at, CURRENT_TIMESTAMP) as created_at, 
            COALESCE(CAST(evi.created_by AS INTEGER), 0) as created_by, 
            COALESCE(evi.updated_at, CURRENT_TIMESTAMP) as updated_at, 
            COALESCE(CAST(evi.updated_by AS INTEGER), 0) as updated_by
        FROM erv_vehicle_inspection_log evi
        WHERE evi.category_master_id = :mid
        ORDER BY evi.created_at ASC
    """
    )
    results = db.execute(query, {"mid": master_id}).mappings().all()
    return [_process_entry_result(db, r) for r in results]


def get_erv_vehicle_inspection_by_id(db: Session, evi_id: int):
    """Fetches a single inspection entry with dynamic name resolution."""
    query = text(
        """
        SELECT 
            evi.*,
            (SELECT TRIM(CONCAT(first_name, ' ', last_name)) FROM users WHERE user_id = evi.created_by) as created_by_name,
            (SELECT TRIM(CONCAT(first_name, ' ', last_name)) FROM users WHERE user_id = evi.updated_by) as updated_by_name,
            COALESCE(evi.created_at, CURRENT_TIMESTAMP) as created_at, 
            COALESCE(CAST(evi.created_by AS INTEGER), 0) as created_by, 
            COALESCE(evi.updated_at, CURRENT_TIMESTAMP) as updated_at, 
            COALESCE(CAST(evi.updated_by AS INTEGER), 0) as updated_by
        FROM erv_vehicle_inspection_log evi
        WHERE evi.evi_id = :evi_id
    """
    )
    result = db.execute(query, {"evi_id": evi_id}).mappings().first()
    return _process_entry_result(db, result)


def create_erv_vehicle_inspection(
    db: Session, payload: ERVVehicleInspectionCreate, user_id: int
):
    """Creates a new inspection entry using manual INSERT logic."""
    # Ensure all fields are dumped (even if None) to satisfy static SQL placeholders
    d = payload.model_dump()
    d = _clean_entry_signatures(d)

    d["created_by"] = d.get("created_by") or user_id
    d["updated_by"] = d.get("updated_by") or user_id
    d["created_at"] = d.get("created_at") or datetime.now()
    d["updated_at"] = d.get("updated_at") or datetime.now()

    query = text(
        """
        INSERT INTO erv_vehicle_inspection_log (
            category_master_id, inspection_date, vehicle_no, diesel,
            kilometer_reading, trail_run_kilometer, cleaning, head_lamp_condition,
            siren_condition, vhf_set_condition, brake_condition, tyre_condition,
            battery_voltage_condition, hydraulic_oil_level, hydraulic_tank_line_condition, 
            rto_condition, ball_valve_condition, number_of_hose_pipe, hose_pipe_condition, 
            any_observation, remarks, driver_signature, technician_signature, 
            shift_in_charge_signature, created_at, created_by, updated_at, updated_by
        ) VALUES (
            :category_master_id, :inspection_date, :vehicle_no, :diesel,
            :kilometer_reading, :trail_run_kilometer, :cleaning, :head_lamp_condition,
            :siren_condition, :vhf_set_condition, :brake_condition, :tyre_condition,
            :battery_voltage_condition, :hydraulic_oil_level, :hydraulic_tank_line_condition,
            :rto_condition, :ball_valve_condition, :number_of_hose_pipe, :hose_pipe_condition,
            :any_observation, :remarks, :driver_signature, :technician_signature,
            :shift_in_charge_signature, :created_at, :created_by, :updated_at, :updated_by
        ) RETURNING evi_id
    """
    )

    result = db.execute(query, d)
    db.commit()
    return result.scalar()


def update_erv_vehicle_inspection(
    db: Session, evi_id: int, payload: ERVVehicleInspectionUpdate, user_id: int
):
    """Updates an inspection entry and archives history."""
    current_data = get_erv_vehicle_inspection_by_id(db, evi_id)
    if not current_data:
        return False

    _log_erv_entry_history(db, dict(current_data), "UPDATE")

    update_data = payload.model_dump(exclude_unset=True)
    update_data = _clean_entry_signatures(update_data)

    for field in ["ms_logbook_id", "technician_id", "evi_id"]:
        update_data.pop(field, None)

    if not update_data:
        db.commit()
        return True

    set_clause_parts = []
    params = {"evi_id": evi_id}

    for key, value in update_data.items():
        set_clause_parts.append(f"{key} = :{key}")
        params[key] = value

    if "updated_by" not in update_data:
        params["updated_by"] = user_id
        set_clause_parts.append("updated_by = :updated_by")

    if "updated_at" not in update_data:
        set_clause_parts.append("updated_at = CURRENT_TIMESTAMP")

    query = text(
        f"UPDATE erv_vehicle_inspection_log SET {', '.join(set_clause_parts)} WHERE evi_id = :evi_id"
    )
    db.execute(query, params)
    db.commit()
    return True


def delete_erv_vehicle_inspection(db: Session, evi_id: int, user_id: int):
    """Performs an archival delete for an entry."""
    current_data = get_erv_vehicle_inspection_by_id(db, evi_id)
    if not current_data:
        return False

    _log_erv_entry_history(db, dict(current_data), "DELETE", user_id=user_id)

    query = text("DELETE FROM erv_vehicle_inspection_log WHERE evi_id = :evi_id")
    result = db.execute(query, {"evi_id": evi_id})
    db.commit()
    return result.rowcount > 0


def get_erv_vehicle_inspection_history(db: Session, evi_id: int):
    """Fetches archival history for a specific entry."""
    query = text(
        """
        SELECT 
            history_id, evi_id, category_master_id, inspection_date,
            vehicle_no, diesel, kilometer_reading, trail_run_kilometer,
            cleaning, head_lamp_condition, siren_condition, vhf_set_condition,
            brake_condition, tyre_condition, battery_voltage_condition,
            hydraulic_oil_level, hydraulic_tank_line_condition, rto_condition,
            ball_valve_condition, number_of_hose_pipe, hose_pipe_condition,
            any_observation, remarks, driver_signature, technician_signature,
            shift_in_charge_signature, action_type, created_at, created_by,
            (SELECT TRIM(CONCAT(first_name, ' ', last_name)) FROM users WHERE user_id = created_by) as created_by_name,
            updated_at, updated_by,
            (SELECT TRIM(CONCAT(first_name, ' ', last_name)) FROM users WHERE user_id = updated_by) as updated_by_name
        FROM erv_vehicle_inspection_log_history 
        WHERE evi_id = :evi_id
        ORDER BY updated_at DESC
    """
    )
    results = db.execute(query, {"evi_id": evi_id}).mappings().all()
    return [_process_entry_result(db, r) for r in results]
