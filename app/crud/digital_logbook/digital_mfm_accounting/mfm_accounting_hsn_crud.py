# app/crud/mfm_accounting_hsn_crud.py
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.schemas.digital_logbook.digital_mfm_accounting.mfm_accounting_hsn_schema import (
    MFMAccountingHSNCreate,
    MFMAccountingHSNUpdate
)


def create_mfm_accounting_hsn(db: Session, payload: MFMAccountingHSNCreate):
    query = text("""
        INSERT INTO mfm_accounting_hsn (
            station, station_in_charge, shift, start_time, status,
            document_number, otr_no, mfm_number, receiving_company, entry_date,
            tank_no, product, mrpl_batch_no, pmhbl_batch_no,
            open_vol_kl_amb, open_vol_kl_15c, open_mass_mt,
            open_density_amb, open_density_15c, open_temp, open_date, open_time,
            close_vol_kl_amb, close_vol_kl_15c, close_mass_mt,
            close_density_amb, close_density_15c, close_temp, close_date, close_time,
            remarks,
            sign_open_pmhbl,sign_open_pmhbl_time, sign_open_hpcl,sign_open_hpcl_time, sign_close_pmhbl,sign_close_pmhbl_time, sign_close_hpcl,sign_close_hpcl_time,
            name_open_pmhbl, name_open_hpcl, name_close_pmhbl, name_close_hpcl,
            quality_tranfered_amb_total,
            quality_tranfered_15c_total,
            quality_tranfered_mass_total   ,created_at,created_by ,updated_at ,updated_by

        )
        VALUES (
            :station, :station_in_charge, :shift, :start_time, :status,
            :document_number, :otr_no, :mfm_number, :receiving_company, :entry_date,
            :tank_no, :product, :mrpl_batch_no, :pmhbl_batch_no,
            :open_vol_kl_amb, :open_vol_kl_15c, :open_mass_mt,
            :open_density_amb, :open_density_15c, :open_temp, :open_date, :open_time,
            :close_vol_kl_amb, :close_vol_kl_15c, :close_mass_mt,
            :close_density_amb, :close_density_15c, :close_temp, :close_date, :close_time,
            :remarks,
            :sign_open_pmhbl,:sign_open_pmhbl_time, :sign_open_hpcl,:sign_open_hpcl_time, :sign_close_pmhbl,:sign_close_pmhbl_time, :sign_close_hpcl,:sign_close_hpcl_time,
            :name_open_pmhbl, :name_open_hpcl, :name_close_pmhbl, :name_close_hpcl,
            :quality_tranfered_amb_total,
            :quality_tranfered_15c_total,
            :quality_tranfered_mass_total,:created_at,:created_by ,:updated_at ,:updated_by

        )
        RETURNING mfm_acc_hsn_id
    """)

    result = db.execute(query, payload.model_dump())
    db.commit()
    return result.fetchone()[0]


def update_mfm_accounting_hsn(
    db: Session,
    mfm_acc_hsn_id: int,
    payload: MFMAccountingHSNUpdate
):
    data = payload.model_dump(exclude_unset=True)
    if not data:
        return False

    set_clause = ", ".join([f"{k} = :{k}" for k in data.keys()])
    data["mfm_acc_hsn_id"] = mfm_acc_hsn_id

    query = text(f"""
        UPDATE mfm_accounting_hsn
        SET {set_clause}
        WHERE mfm_acc_hsn_id = :mfm_acc_hsn_id
    """)

    db.execute(query, data)
    db.commit()
    return True


def delete_mfm_accounting_hsn(db: Session, mfm_acc_hsn_id: int):
    query = text("""
        DELETE FROM mfm_accounting_hsn
        WHERE mfm_acc_hsn_id = :mfm_acc_hsn_id
    """)
    result = db.execute(query, {"mfm_acc_hsn_id": mfm_acc_hsn_id})
    db.commit()
    return result.rowcount > 0
