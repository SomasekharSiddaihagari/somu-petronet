from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import select
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

from app.database import get_db
from app.models.permit_management_models.job_safety_analysis_jsa.job_safety_analysis import JobSafetyAnalysis
from app.models.permit_management_models.job_safety_analysis_jsa.job_safety_analysis_step import JobSafetyAnalysisStep

router = APIRouter(prefix="/jsa/{jsa_id}/steps", tags=["JSA Steps"])


# ─────────────────────────────────────────────
# SCHEMAS
# ─────────────────────────────────────────────

class StepBase(BaseModel):
    row_no: Optional[int] = None
    job_steps: Optional[str] = None
    potential_hazards: Optional[str] = None
    hazard_control_measures: Optional[str] = None
    ppe_required: Optional[str] = None


class StepCreate(StepBase):
    pass


class StepUpdate(StepBase):
    pass


class StepOut(StepBase):
    step_id: int
    jsa_id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class BulkStepCreate(BaseModel):
    steps: List[StepCreate]


class BulkStepOut(BaseModel):
    created: int
    steps: List[StepOut]


# ─────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────

def _get_jsa_or_404(jsa_id: int, db: Session) -> JobSafetyAnalysis:
    jsa = db.get(JobSafetyAnalysis, jsa_id)
    if not jsa:
        raise HTTPException(status_code=404, detail=f"JSA {jsa_id} not found")
    return jsa


def _get_step_or_404(step_id: int, jsa_id: int, db: Session) -> JobSafetyAnalysisStep:
    step = db.execute(
        select(JobSafetyAnalysisStep).where(
            JobSafetyAnalysisStep.step_id == step_id,
            JobSafetyAnalysisStep.jsa_id == jsa_id,
        )
    ).scalars().first()
    if not step:
        raise HTTPException(
            status_code=404,
            detail=f"Step {step_id} not found under JSA {jsa_id}",
        )
    return step


# ─────────────────────────────────────────────
# ROUTES
# ─────────────────────────────────────────────

@router.post("", response_model=StepOut, status_code=status.HTTP_201_CREATED)
def create_step(jsa_id: int, payload: StepCreate, db: Session = Depends(get_db)):
    """Add a single step to a JSA."""
    _get_jsa_or_404(jsa_id, db)
    step = JobSafetyAnalysisStep(**payload.model_dump(), jsa_id=jsa_id)
    db.add(step)
    db.commit()
    db.refresh(step)
    return step




@router.get("", response_model=List[StepOut])
def list_steps(jsa_id: int, db: Session = Depends(get_db)):
    """List all steps for a JSA, ordered by row_no."""
    _get_jsa_or_404(jsa_id, db)
    steps = db.execute(
        select(JobSafetyAnalysisStep)
        .where(JobSafetyAnalysisStep.jsa_id == jsa_id)
        .order_by(JobSafetyAnalysisStep.row_no)
    ).scalars().all()
    return steps


@router.get("/{step_id}", response_model=StepOut)
def get_step(step_id: int, db: Session = Depends(get_db)):
    """Get a single step."""
    step = db.get(JobSafetyAnalysisStep, step_id)
    if not step:
        raise HTTPException(status_code=404, detail=f"Step {step_id} not found")
    return step


@router.put("/{step_id}", response_model=StepOut)
def update_step(
    jsa_id: int, step_id: int, payload: StepUpdate, db: Session = Depends(get_db)
):
    """Full update of a step."""
    step = _get_step_or_404(step_id, jsa_id, db)
    for field, value in payload.model_dump().items():
        setattr(step, field, value)
    db.commit()
    db.refresh(step)
    return step




@router.delete("/{step_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_step(jsa_id: int, step_id: int, db: Session = Depends(get_db)):
    """Delete a single step."""
    step = _get_step_or_404(step_id, jsa_id, db)
    db.delete(step)
    db.commit()

