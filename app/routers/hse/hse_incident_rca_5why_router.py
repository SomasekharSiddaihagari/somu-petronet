from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
 
from app.database import get_db
from app.schemas.hse.hse_incident_rca_5why_schema import (
    RCA5WhyCreate,
    RCA5WhyUpdate,
    RCA5WhyResponse,
    RCA5WhyListResponse
)
from app.crud.hse.hse_incident_rca_5why_crud import (
    create_rca_5why,
    update_rca_5why,
    get_all_rca_5why
)
 
router = APIRouter(
    prefix="/hse/incident-rca-5why",
    tags=["HSE - RCA 5 WHY"]
)
 
# =========================
# CREATE
# =========================
@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    response_model=RCA5WhyResponse
)
def create_rca(
    data: RCA5WhyCreate,
    db: Session = Depends(get_db)
):
    return create_rca_5why(db, data.dict())
 
 
# =========================
# UPDATE
# =========================
@router.put("/{rca_id}")
def update_rca(
    rca_id: int,
    data: RCA5WhyUpdate,
    db: Session = Depends(get_db)
):
    update_rca_5why(db, rca_id, data.dict())
    return {"message": "RCA 5-Why updated successfully"}
 
 
# =========================
# GET ALL
# =========================
@router.get(
    "",
    response_model=RCA5WhyListResponse
)
def get_all(
    db: Session = Depends(get_db)
):
    return get_all_rca_5why(db)
 
 
 
 
 
 