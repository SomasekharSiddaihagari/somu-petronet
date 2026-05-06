from sqlalchemy.orm import Session
from sqlalchemy.sql import text

from app.schemas.claim.allowance_claim_schema import AllowanceAdmissionChildCreate, AllowanceAdmissionChildUpdate, AllowanceClaimCreate, AllowanceClaimUpdate
from app.schemas.claim.out_of_pocket_claim_entry_schema import OutOfPocketClaimEntryCreate, OutOfPocketClaimEntryUpdate








# =================================================
# CREATE ENTRY (INSERT + HISTORY)
# =================================================
def create_out_of_pocket_entry(
    db: Session,
    data: OutOfPocketClaimEntryCreate
):
    query = text("""
        INSERT INTO out_of_pocket_claim_entry (
            out_of_pocket_claim_id,
            entry_type,
            hours,
            claim_date,
            amount,
            justification
        )
        VALUES (
            :out_of_pocket_claim_id,
            :entry_type,
            :hours,
            :claim_date,
            :amount,
            :justification
        )
        RETURNING out_of_pocket_claim_entry_id
    """)

    entry_id = db.execute(query, data.model_dump()).scalar()

    insert_out_of_pocket_entry_history(db, entry_id)
    db.commit()

    return entry_id


# =================================================
# UPDATE ENTRY (UPDATE + HISTORY)
# =================================================
def update_out_of_pocket_entry(
    db: Session,
    out_of_pocket_claim_entry_id: int,
    data: OutOfPocketClaimEntryUpdate
):
    update_fields = data.model_dump(exclude_unset=True)

    if not update_fields:
        return False

    set_clause = ", ".join(f"{k} = :{k}" for k in update_fields)

    query = text(f"""
        UPDATE out_of_pocket_claim_entry
        SET {set_clause}
        WHERE out_of_pocket_claim_entry_id = :out_of_pocket_claim_entry_id
    """)

    update_fields["out_of_pocket_claim_entry_id"] = out_of_pocket_claim_entry_id
    db.execute(query, update_fields)

    insert_out_of_pocket_entry_history(db, out_of_pocket_claim_entry_id)
    db.commit()

    return True


# =================================================
# INSERT HISTORY SNAPSHOT
# =================================================
def insert_out_of_pocket_entry_history(
    db: Session,
    out_of_pocket_claim_entry_id: int
):
    history_query = text("""
        INSERT INTO out_of_pocket_claim_entry_history (
            out_of_pocket_claim_entry_id,
            out_of_pocket_claim_id,
            entry_type,
            hours,
            claim_date,
            amount,
            justification,
            created_at
        )
        SELECT
            out_of_pocket_claim_entry_id,
            out_of_pocket_claim_id,
            entry_type,
            hours,
            claim_date,
            amount,
            justification,
            NOW()
        FROM out_of_pocket_claim_entry
        WHERE out_of_pocket_claim_entry_id = :id
    """)

    db.execute(history_query, {"id": out_of_pocket_claim_entry_id})



# =================================================
# ALLOWANCE CLAIM
# =================================================
def create_allowance_claim(db: Session, data: AllowanceClaimCreate):
    query = text("""
        INSERT INTO allowance_claim (
            ra_claim_id,
            employee_name,
            employee_id,
            department,
            designation,
            station,
            grade,

            from_location,
            to_location,
            effective_transfer_date,
            claim_date,

            travel_from,
            travel_to,
            travel_mode,
            travel_date,
            number_of_passengers,
            travel_amount,
            travel_remarks,
            travel_documents,
            include_travel,

            displacement_city,
            no_of_days_claimed,
            displacement_rate,
            displacement_amount,
            maximum_eligible_days,
            displacement_remarks,
            displacement_documents,
            include_displacement,

            basic_pay_monthly,
            dearness_allowance_monthly,
            eligible_settling_amount,
            settling_remarks,
            settling_documents,
            include_settling,
            settling_no_of_days,
            t_house_hold_rate,
            vehicle_rate,

            transport_mode,
            transport_distance_km,
            freight_amount,
            goods_transport_remarks,
            goods_transport_documents,
            include_goods_transport,
            amount_claimed_household_transport,

            amount_claimed_packaging,
            packaging_vendor,
            packaging_bill_no,
            packaging_remarks,
            packaging_documents,
            include_packaging,
            maximum_eligible_amount_packaging,

            insurance_company,
            policy_no,
            insurance_amount,
            insurance_start_date,
            insurance_end_date,
            insurance_remarks,
            insurance_documents,
            include_insurance,

            vehicle_type,
            vehicle_registration_no,
            vehicle_transport_mode,
            vehicle_transport_amount,
            vehicle_transport_remarks,
            vehicle_transport_documents,
            include_vehicle_transport,
            vehicle_transport_distance_km,

            total_travel,
            total_displacement,
            total_settling,
            total_goods_transport,
            total_packaging,
            total_insurance,
            total_vehicle_transport,
            total_admission,
            grand_total,

            remarks,
            status,
            created_by,
            created_at,
            updated_by,
            updated_at
        )
        VALUES (
            :ra_claim_id,
            :employee_name,
            :employee_id,
            :department,
            :designation,
            :station,
            :grade,

            :from_location,
            :to_location,
            :effective_transfer_date,
            :claim_date,

            :travel_from,
            :travel_to,
            :travel_mode,
            :travel_date,
            :number_of_passengers,
            :travel_amount,
            :travel_remarks,
            :travel_documents,
            :include_travel,

            :displacement_city,
            :no_of_days_claimed,
            :displacement_rate,
            :displacement_amount,
            :maximum_eligible_days,
            :displacement_remarks,
            :displacement_documents,
            :include_displacement,

            :basic_pay_monthly,
            :dearness_allowance_monthly,
            :eligible_settling_amount,
            :settling_remarks,
            :settling_documents,
            :include_settling,
            :settling_no_of_days,
            :t_house_hold_rate,
            :vehicle_rate,

            :transport_mode,
            :transport_distance_km,
            :freight_amount,
            :goods_transport_remarks,
            :goods_transport_documents,
            :include_goods_transport,
            :amount_claimed_household_transport,

            :amount_claimed_packaging,
            :packaging_vendor,
            :packaging_bill_no,
            :packaging_remarks,
            :packaging_documents,
            :include_packaging,
            :maximum_eligible_amount_packaging,

            :insurance_company,
            :policy_no,
            :insurance_amount,
            :insurance_start_date,
            :insurance_end_date,
            :insurance_remarks,
            :insurance_documents,
            :include_insurance,

            :vehicle_type,
            :vehicle_registration_no,
            :vehicle_transport_mode,
            :vehicle_transport_amount,
            :vehicle_transport_remarks,
            :vehicle_transport_documents,
            :include_vehicle_transport,
            :vehicle_transport_distance_km,

            :total_travel,
            :total_displacement,
            :total_settling,
            :total_goods_transport,
            :total_packaging,
            :total_insurance,
            :total_vehicle_transport,
            :total_admission,
            :grand_total,

            :remarks,
            :status,
            :created_by,
            NOW(),
            :updated_by,
            NOW()
        )
        RETURNING allowance_claim_id
    """)

    claim_id = db.execute(query, data.model_dump(exclude_none=False)).scalar()
    insert_allowance_claim_history(db, claim_id)
    db.commit()
    return claim_id



from sqlalchemy.sql import text
from sqlalchemy.orm import Session
from fastapi import HTTPException

def update_allowance_claim(
    db: Session,
    allowance_claim_id: int,
    data: AllowanceClaimUpdate
):
    fields = data.model_dump(exclude_unset=True)

    # 🚨 IMPORTANT CHECK
    if not fields:
        raise HTTPException(
            status_code=400,
            detail="No valid fields provided for update"
        )

    set_clause = ", ".join(f"{key} = :{key}" for key in fields.keys())

    query = text(f"""
        UPDATE allowance_claim
        SET {set_clause}
        WHERE allowance_claim_id = :allowance_claim_id
    """)

    fields["allowance_claim_id"] = allowance_claim_id

    db.execute(query, fields)

    insert_allowance_claim_history(db, allowance_claim_id)

    db.commit()
    return True


def insert_allowance_claim_history(db: Session, allowance_claim_id: int):
    db.execute(text("""
        INSERT INTO allowance_claim_history (
            allowance_claim_id,
            ra_claim_id,
            employee_name,
            employee_id,
            department,
            designation,
            station,
            grade,

            from_location,
            to_location,
            effective_transfer_date,
            claim_date,

            travel_from,
            travel_to,
            travel_mode,
            travel_date,
            number_of_passengers,
            travel_amount,
            travel_remarks,
            travel_documents,
            include_travel,

            settling_no_of_days,
            t_house_hold_rate,
            vehicle_rate,

            displacement_city,
            maximum_eligible_days,
            no_of_days_claimed,
            displacement_rate,
            displacement_amount,
            displacement_remarks,
            displacement_documents,
            include_displacement,

            basic_pay_monthly,
            dearness_allowance_monthly,
            eligible_settling_amount,
            settling_remarks,
            settling_documents,
            include_settling,

            transport_mode,
            transport_distance_km,
            freight_amount,
            goods_transport_remarks,
            goods_transport_documents,
            include_goods_transport,
            amount_claimed_household_transport,

            amount_claimed_packaging,
            packaging_vendor,
            packaging_bill_no,
            packaging_remarks,
            packaging_documents,
            include_packaging,
            maximum_eligible_amount_packaging,

            insurance_company,
            policy_no,
            insurance_amount,
            insurance_start_date,
            insurance_end_date,
            insurance_remarks,
            insurance_documents,
            include_insurance,

            vehicle_type,
            vehicle_registration_no,
            vehicle_transport_mode,
            vehicle_transport_amount,
            vehicle_transport_remarks,
            vehicle_transport_documents,
            include_vehicle_transport,
            vehicle_transport_distance_km,

            total_travel,
            total_displacement,
            total_settling,
            total_goods_transport,
            total_packaging,
            total_insurance,
            total_vehicle_transport,
            total_admission,
            grand_total,

            remarks,
            status,

            updated_by_supervisor,
            updated_by_supervisor_name,
            supervisor_comment,

            updated_by_hr,
            updated_by_hr_name,
            hr_comment,

            updated_by_finance,
            updated_by_finance_name,
            finance_comment,

            created_at
        )
        SELECT
            allowance_claim_id,
            ra_claim_id,
            employee_name,
            employee_id,
            department,
            designation,
            station,
            grade,

            from_location,
            to_location,
            effective_transfer_date,
            claim_date,

            travel_from,
            travel_to,
            travel_mode,
            travel_date,
            number_of_passengers,
            travel_amount,
            travel_remarks,
            travel_documents,
            include_travel,

            settling_no_of_days,
            t_house_hold_rate,
            vehicle_rate,

            displacement_city,
            maximum_eligible_days,
            no_of_days_claimed,
            displacement_rate,
            displacement_amount,
            displacement_remarks,
            displacement_documents,
            include_displacement,

            basic_pay_monthly,
            dearness_allowance_monthly,
            eligible_settling_amount,
            settling_remarks,
            settling_documents,
            include_settling,

            transport_mode,
            transport_distance_km,
            freight_amount,
            goods_transport_remarks,
            goods_transport_documents,
            include_goods_transport,
            amount_claimed_household_transport,

            amount_claimed_packaging,
            packaging_vendor,
            packaging_bill_no,
            packaging_remarks,
            packaging_documents,
            include_packaging,
            maximum_eligible_amount_packaging,

            insurance_company,
            policy_no,
            insurance_amount,
            insurance_start_date,
            insurance_end_date,
            insurance_remarks,
            insurance_documents,
            include_insurance,

            vehicle_type,
            vehicle_registration_no,
            vehicle_transport_mode,
            vehicle_transport_amount,
            vehicle_transport_remarks,
            vehicle_transport_documents,
            include_vehicle_transport,
            vehicle_transport_distance_km,

            total_travel,
            total_displacement,
            total_settling,
            total_goods_transport,
            total_packaging,
            total_insurance,
            total_vehicle_transport,
            total_admission,
            grand_total,

            remarks,
            status,

            updated_by_supervisor,
            updated_by_supervisor_name,
            supervisor_comment,

            updated_by_hr,
            updated_by_hr_name,
            hr_comment,

            updated_by_finance,
            updated_by_finance_name,
            finance_comment,

            NOW()
        FROM allowance_claim
        WHERE allowance_claim_id = :id
    """), {"id": allowance_claim_id})
# =================================================
# ALLOWANCE ADMISSION CHILD
# =================================================
def create_admission_child(db: Session, data: AllowanceAdmissionChildCreate):
    entry_id = db.execute(text("""
        INSERT INTO allowance_admission_child (
            allowance_claim_id,
            child_name,
            relationship,
            class_studying,
            school_name,
            amount_claimed,
            remarks,
            document_names,
            user_id,
            station_id,
            city_class,
            city_name

        )
        VALUES (
            :allowance_claim_id,
            :child_name,
            :relationship,
            :class_studying,
            :school_name,
            :amount_claimed,
            :remarks,
            :document_names,
            :user_id,
            :station_id,
            :city_class,
            :city_name
        )
        RETURNING allowance_admission_child_id
    """), data.model_dump()).scalar()

    insert_admission_child_history(db, entry_id)
    db.commit()
    return entry_id



def update_admission_child(db: Session, child_id: int, data: AllowanceAdmissionChildUpdate):
    fields = data.model_dump(exclude_unset=True, exclude_none=True)

    if not fields:
        return False

    set_clause = ", ".join(f"{k} = :{k}" for k in fields)

    db.execute(text(f"""
        UPDATE allowance_admission_child
        SET {set_clause}
        WHERE allowance_admission_child_id = :id
    """), {**fields, "id": child_id})

    insert_admission_child_history(db, child_id)
    db.commit()
    return True



def insert_admission_child_history(db: Session, child_id: int):
    db.execute(text("""
        INSERT INTO allowance_admission_child_history (
            allowance_admission_child_id,
            allowance_claim_id,
            child_name,
            relationship,
            class_studying,
            school_name,
            amount_claimed,
            remarks,
            user_id,
            station_id,
            city_class,
            city_name,
            document_names,
            created_at
        )
        SELECT
            allowance_admission_child_id,
            allowance_claim_id,
            child_name,
            relationship,
            class_studying,
            school_name,
            amount_claimed,
            remarks,
            user_id,
            station_id,
            city_class,
            city_name,
            document_names,
            NOW()
        FROM allowance_admission_child
        WHERE allowance_admission_child_id = :id
    """), {"id": child_id})


def get_employee_children_by_user_id(
    db: Session,
    user_id: int
):
    query = text("""
        SELECT
            ef_id,
            full_name
        FROM employee_family
        WHERE user_id = :user_id
          AND LOWER(relation) IN ('child', 'children', 'son', 'daughter')
          AND COALESCE(status, 'ACTIVE') != 'INACTIVE'
        ORDER BY full_name
    """)

    result = db.execute(query, {"user_id": user_id}).mappings().all()
    return result


