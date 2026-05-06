# app/crud/mfm_accounting_dkn_crud.py
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.schemas.digital_logbook.digital_mfm_accounting.mfm_accounting_dkn_schema import (
    MFMAccountingDKNCreate,
    MFMAccountingDKNUpdate
)


def create_mfm_accounting_dkn(db: Session, payload: MFMAccountingDKNCreate):
    query = text("""
        INSERT INTO mfm_accounting_dkn (
            station, station_in_charge, shift, start_time,
            document_number, otr_no, mfm_number, receiving_company, log_date,
            tank_no, product, mrpl_batch_no, pmhbl_batch_no,
            opening_vol_kl_amb, opening_vol_kl_15c, opening_mass_mt,
            opening_weighted_amb_density, opening_weighted_temp, opening_weighted_15c_density,
            opening_date, opening_time,
            closing_vol_kl_amb, closing_vol_kl_15c, closing_mass_mt,
            closing_weighted_amb_density, closing_weighted_temp, closing_weighted_15c_density,
            closing_date, closing_time,
            qty_transferred_vol_kl, qty_transferred_mass_mt,
            qty_transferred_15c_total, qty_transferred_mass_total, qty_transferred_amb_total,
            hpcl_hsd_line_mov_seal, hpcl_hsd_line_mov_status,
            bpcl_hsd_line_mov_seal, bpcl_hsd_line_mov_status,
            iocl_hsd_line_mov_seal, iocl_hsd_line_mov_status,
            hpcl_hsd_line_hov_seal, hpcl_hsd_line_hov_status,
            bpcl_hsd_line_hov_seal, bpcl_hsd_line_hov_status,
            iocl_hsd_line_hov_seal, iocl_hsd_line_hov_status,
            mrpl_hsd_line_mov_seal, mrpl_hsd_line_mov_status,
            if_tank_101_mov_seal, if_tank_101_mov_status,
            if_tank_102_mov_seal, if_tank_102_mov_status,
            ms_header_line_mov_1415_seal, ms_header_line_mov_1415_status,
            ms_header_line_mov_1416_seal, ms_header_line_mov_1416_status,
            mrpl_hsd_dbvb_mov_seal, mrpl_hsd_dbvb_mov_status,
            remarks,
            opening_pmhbl_signature,
                 opening_pmhbl_signature_time, 
                 opening_mrpl_signature,
                 opening_mrpl_signature_time,
            closing_pmhbl_signature,
                 closing_pmhbl_signature_time,
                  closing_mrpl_signature,
                 closing_mrpl_signature_time,
            name_open_pmhbl, name_open_hpcl, name_close_pmhbl, name_close_hpcl   ,created_at,created_by ,updated_at ,updated_by

        )
        VALUES (
            :station, :station_in_charge, :shift, :start_time,
            :document_number, :otr_no, :mfm_number, :receiving_company, :log_date,
            :tank_no, :product, :mrpl_batch_no, :pmhbl_batch_no,
            :opening_vol_kl_amb, :opening_vol_kl_15c, :opening_mass_mt,
            :opening_weighted_amb_density, :opening_weighted_temp, :opening_weighted_15c_density,
            :opening_date, :opening_time,
            :closing_vol_kl_amb, :closing_vol_kl_15c, :closing_mass_mt,
            :closing_weighted_amb_density, :closing_weighted_temp, :closing_weighted_15c_density,
            :closing_date, :closing_time,
            :qty_transferred_vol_kl, :qty_transferred_mass_mt,
            :qty_transferred_15c_total, :qty_transferred_mass_total, :qty_transferred_amb_total,
            :hpcl_hsd_line_mov_seal, :hpcl_hsd_line_mov_status,
            :bpcl_hsd_line_mov_seal, :bpcl_hsd_line_mov_status,
            :iocl_hsd_line_mov_seal, :iocl_hsd_line_mov_status,
            :hpcl_hsd_line_hov_seal, :hpcl_hsd_line_hov_status,
            :bpcl_hsd_line_hov_seal, :bpcl_hsd_line_hov_status,
            :iocl_hsd_line_hov_seal, :iocl_hsd_line_hov_status,
            :mrpl_hsd_line_mov_seal, :mrpl_hsd_line_mov_status,
            :if_tank_101_mov_seal, :if_tank_101_mov_status,
            :if_tank_102_mov_seal, :if_tank_102_mov_status,
            :ms_header_line_mov_1415_seal, :ms_header_line_mov_1415_status,
            :ms_header_line_mov_1416_seal, :ms_header_line_mov_1416_status,
            :mrpl_hsd_dbvb_mov_seal, :mrpl_hsd_dbvb_mov_status,
            :remarks,
            :opening_pmhbl_signature,:opening_pmhbl_signature_time, :opening_mrpl_signature,:opening_mrpl_signature_time,
            :closing_pmhbl_signature,:closing_pmhbl_signature_time, :closing_mrpl_signature,:closing_mrpl_signature_time,
            :name_open_pmhbl, :name_open_hpcl, :name_close_pmhbl, :name_close_hpcl,:created_at,:created_by ,:updated_at ,:updated_by

        )
        RETURNING mfm_acc_dkn_id
    """)

    result = db.execute(query, payload.model_dump())
    db.commit()
    return result.fetchone()[0]


def update_mfm_accounting_dkn(db: Session, mfm_acc_dkn_id: int, payload: MFMAccountingDKNUpdate):
    data = payload.model_dump(exclude_unset=True)
    if not data:
        return False

    set_clause = ", ".join([f"{k} = :{k}" for k in data.keys()])
    data["mfm_acc_dkn_id"] = mfm_acc_dkn_id

    query = text(f"""
        UPDATE mfm_accounting_dkn
        SET {set_clause}
        WHERE mfm_acc_dkn_id = :mfm_acc_dkn_id
    """)

    db.execute(query, data)
    db.commit()
    return True


def delete_mfm_accounting_dkn(db: Session, mfm_acc_dkn_id: int):
    query = text("""
        DELETE FROM mfm_accounting_dkn
        WHERE mfm_acc_dkn_id = :mfm_acc_dkn_id
    """)
    result = db.execute(query, {"mfm_acc_dkn_id": mfm_acc_dkn_id})
    db.commit()
    return result.rowcount > 0
