from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.crud.digital_logbook.digital_logbook_linewalker.line_walker_entry_crud import create_line_walker_entry, delete_line_walker_entry, update_line_walker_entry
from app.database import get_db
from app.schemas.digital_logbook.digital_logbook_linewalker.line_walker_entry_schemas import LineWalkerEntryCreate, LineWalkerEntryUpdate

from app.utils.access_service import validate_token

router = APIRouter(
    prefix="/line-walker-entry",
    tags=["Line Walker Entry"],dependencies=[Depends(validate_token)]
)


@router.post("")
def create_entry(payload: LineWalkerEntryCreate, db: Session = Depends(get_db)):
    return {"line_entry_id": create_line_walker_entry(db, payload)}


@router.put("/{line_entry_id}")
def update_entry(
    line_entry_id: int,
    payload: LineWalkerEntryUpdate,
    db: Session = Depends(get_db)
):
    update_line_walker_entry(db, line_entry_id, payload)
    return {"message": "Updated successfully"}


@router.delete("/{line_entry_id}")
def delete_entry(line_entry_id: int, db: Session = Depends(get_db)):
    delete_line_walker_entry(db, line_entry_id)
    return {"message": "Deleted successfully"}
