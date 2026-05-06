from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.crud.digital_logbook.digital_logbook_mlr.mlr_digital_logbook_entry_crud import create_mlr_entry, delete_mlr_entry, update_mlr_entry
from app.database import get_db
from app.schemas.digital_logbook.digital_logbook_mlr.mlr_digital_logbook_entry_schemas import MlrDigitalLogBookEntryCreate, MlrDigitalLogBookEntryUpdate
from app.utils.access_service import validate_token

router = APIRouter(
    prefix="/mlr-logbook-entry",
    tags=["MLR Digital Logbook Entry"],dependencies=[Depends(validate_token)]
)


@router.post("", response_model=dict)
def create_entry(payload: MlrDigitalLogBookEntryCreate, db: Session = Depends(get_db)):
    entry_id = create_mlr_entry(db, payload)
    return {
        "message": "MLR logbook entry created successfully",
        "mlr_entry_id": entry_id
    }


@router.put("/{entry_id}", response_model=dict)
def update_entry(
    entry_id: int,
    payload: MlrDigitalLogBookEntryUpdate,
    db: Session = Depends(get_db)
):
    update_mlr_entry(db, entry_id, payload)
    return {"message": "MLR logbook entry updated successfully"}


@router.delete("/{entry_id}", response_model=dict)
def delete_entry(entry_id: int, db: Session = Depends(get_db)):
    delete_mlr_entry(db, entry_id)
    return {"message": "MLR logbook entry deleted successfully"}
