# app/crud/hse/capa_document_change_crud.py
from sqlalchemy.orm import Session
from sqlalchemy.sql import text
from fastapi import HTTPException

from app.schemas.hse.capa_document_change_schema import (
    CapaDocumentChangeCreate,
    CapaDocumentChangeUpdate
)


# =========================
# CREATE
# =========================
def create_capa_document_change(
    db: Session,
    data: CapaDocumentChangeCreate
):
    payload = data.model_dump()

    sql = text("""
        INSERT INTO capa_document_change (
            capa_id,
            document_code,
            changes_in_brief
        )
        VALUES (
            :capa_id,
            :document_code,
            :changes_in_brief
        )
        RETURNING capa_doc_id
    """)

    res = db.execute(sql, payload)
    db.commit()
    return {"capa_doc_id": res.scalar()}


# =========================
# UPDATE
# =========================
def update_capa_document_change(
    db: Session,
    capa_doc_id: int,
    data: CapaDocumentChangeUpdate
):
    payload = data.model_dump(exclude_unset=True)

    if not payload:
        raise HTTPException(
            status_code=400,
            detail="No fields provided for update"
        )

    payload["capa_doc_id"] = capa_doc_id

    set_clause = ", ".join(
        [f"{k}=:{k}" for k in payload if k != "capa_doc_id"]
    )

    sql = text(f"""
        UPDATE capa_document_change
        SET {set_clause}
        WHERE capa_doc_id = :capa_doc_id
    """)

    db.execute(sql, payload)
    db.commit()
    return True


# =========================
# GET ALL
# =========================
def get_all_capa_document_changes(db: Session):
    rows = db.execute(
        text("""
            SELECT *
            FROM capa_document_change
            ORDER BY created_at DESC
        """)
    ).mappings().all()

    return {
        "count": len(rows),
        "data": rows
    }


# =========================
# DELETE
# =========================
def delete_capa_document_change(
    db: Session,
    capa_doc_id: int
):
    # Check if record exists
    check_sql = text("""
        SELECT capa_doc_id
        FROM capa_document_change
        WHERE capa_doc_id = :capa_doc_id
    """)

    result = db.execute(check_sql, {"capa_doc_id": capa_doc_id}).fetchone()

    if not result:
        raise HTTPException(
            status_code=404,
            detail="CAPA document change not found"
        )

    # Delete record
    delete_sql = text("""
        DELETE FROM capa_document_change
        WHERE capa_doc_id = :capa_doc_id
    """)

    db.execute(delete_sql, {"capa_doc_id": capa_doc_id})
    db.commit()

    return True
