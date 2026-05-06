from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.crud.digital_logbook.digital_logbook_linewalker.supervisor_entry_crud import create_supervisor_entry, delete_supervisor_entry, update_supervisor_entry
from app.database import get_db
from app.schemas.digital_logbook.digital_logbook_linewalker.supervisor_entry_schemas import SupervisorEntryCreate, SupervisorEntryUpdate
from app.utils.access_service import validate_token


router = APIRouter(
    prefix="/supervisor-entry",
    tags=["Line Walker Supervisor Entry"],dependencies=[Depends(validate_token)]
)


@router.post("")
def create_entry(payload: SupervisorEntryCreate, db: Session = Depends(get_db)):
    return {"sup_entry_id": create_supervisor_entry(db, payload)}


@router.put("/{sup_entry_id}")
def update_entry(
    sup_entry_id: int,
    payload: SupervisorEntryUpdate,
    db: Session = Depends(get_db)
):
    update_supervisor_entry(db, sup_entry_id, payload)
    return {"message": "Updated successfully"}


@router.delete("/{sup_entry_id}")
def delete_entry(sup_entry_id: int, db: Session = Depends(get_db)):
    delete_supervisor_entry(db, sup_entry_id)
    return {"message": "Deleted successfully"}
