# app/routers/hse/capa_document_change_router.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.hse.capa_document_change_schema import (
    CapaDocumentChangeCreate,
    CapaDocumentChangeUpdate
)
from app.crud.hse.capa_document_change_crud import (
    create_capa_document_change,
    update_capa_document_change,
    get_all_capa_document_changes
)
from app.crud.hse.capa_document_change_crud import (
    delete_capa_document_change
)

router = APIRouter(
    prefix="/hse/capa-document-change",
    tags=["HSE - CAPA Document Change"]
)


@router.post("/create")
def create_doc_change(
    data: CapaDocumentChangeCreate,
    db: Session = Depends(get_db)
):
    return create_capa_document_change(db, data)


@router.put("/update/{capa_doc_id}")
def update_doc_change(
    capa_doc_id: int,
    data: CapaDocumentChangeUpdate,
    db: Session = Depends(get_db)
):
    update_capa_document_change(db, capa_doc_id, data)
    return {"message": "CAPA document change updated successfully"}


@router.get("/get-all")
def get_all(db: Session = Depends(get_db)):
    return get_all_capa_document_changes(db)


@router.delete("/delete/{capa_doc_id}")
def delete_doc_change(
    capa_doc_id: int,
    db: Session = Depends(get_db)
):
    delete_capa_document_change(db, capa_doc_id)
    return {"message": "CAPA document change deleted successfully"}
