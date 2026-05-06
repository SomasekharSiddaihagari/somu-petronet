from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.crud.digital_logbook.digital_fire import fire_engine_test_entry_crud
from app.crud.digital_logbook.digital_fire import fire_engine_test_master_crud as crud

from app.database import get_db
from app.schemas.digital_logbook.digital_fire.fire_engine_test_entry_schemas import (
    FireEngineTestEntryCreate,
    FireEngineTestEntryUpdate
)
from app.utils.access_service import validate_token


router = APIRouter(
    prefix="/fire-engine-test-entry",
    tags=["Fire Engine Test Entry"],dependencies=[Depends(validate_token)]
)


@router.post("", status_code=status.HTTP_201_CREATED)
def create_entry(
    payload: FireEngineTestEntryCreate,
    db: Session = Depends(get_db)
):
    return fire_engine_test_entry_crud.create_fire_engine_test_entry(db, payload)


@router.get("/{fire_entry_id}")
def get_entry(
    fire_entry_id: int,
    db: Session = Depends(get_db)
):
    data = fire_engine_test_entry_crud.get_fire_engine_test_entry_by_id(db, fire_entry_id)
    if not data:
        raise HTTPException(status_code=404, detail="Entry not found")
    return data


@router.get("/master/{master_id}")
def get_entries_by_master(
    master_id: int,
    db: Session = Depends(get_db)
):
    return fire_engine_test_entry_crud.get_entries_by_master_id(db, master_id)


@router.put("/{fire_entry_id}")
def update_entry(
    fire_entry_id: int,
    payload: FireEngineTestEntryUpdate,
    db: Session = Depends(get_db)
):
    data = fire_engine_test_entry_crud.update_fire_engine_test_entry(
        db,
        fire_entry_id,
        payload
    )
    if not data:
        raise HTTPException(status_code=404, detail="Entry not found")
    return data


@router.delete("/{fire_entry_id}")
def delete_entry(
    fire_entry_id: int,
    db: Session = Depends(get_db)
):
    result = fire_engine_test_entry_crud.delete_fire_engine_test_entry(db, fire_entry_id)
    if not result:
        raise HTTPException(status_code=404, detail="Entry not found")

    return {"message": "Entry deleted successfully"}
