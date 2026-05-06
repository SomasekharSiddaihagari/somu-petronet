from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.sql import text
from pydantic import BaseModel
from typing import Optional
from datetime import date
from app.database import get_db


# =====================================================
# SCHEMA
# =====================================================

class DiscussionChildCreate(BaseModel):
    discussion_id: int
    issues_discussed: Optional[str] = None
    action_taken: Optional[str] = None
    completed_on: Optional[date] = None
    action_by: Optional[str] = None
    target_date: Optional[date] = None


class DiscussionChildUpdate(BaseModel):
    issues_discussed: Optional[str] = None
    action_taken: Optional[str] = None
    completed_on: Optional[date] = None
    action_by: Optional[str] = None
    target_date: Optional[date] = None


# =====================================================
# ROUTER
# =====================================================

router = APIRouter(
    prefix="/api/hse/safety-committee-minutes-discussion-child",
    tags=["HSE Safety Committee Minutes Discussion Child"]
)


@router.post("/create")
def create_discussion_child(data: DiscussionChildCreate, db: Session = Depends(get_db)):
    # check parent discussion exists
    existing_discussion = db.execute(
        text("SELECT id FROM safety_committee_minutes_discussions WHERE id = :discussion_id"),
        {"discussion_id": data.discussion_id}
    ).fetchone()

    if not existing_discussion:
        raise HTTPException(status_code=404, detail="Parent discussion not found")

    payload = data.model_dump()

    sql = text("""
        INSERT INTO safety_committee_minutes_discussion_child (
            discussion_id,
            issues_discussed,
            action_taken,
            completed_on,
            action_by,
            target_date
        ) VALUES (
            :discussion_id,
            :issues_discussed,
            :action_taken,
            :completed_on,
            :action_by,
            :target_date
        ) RETURNING scmdc_id, discussion_id
    """)

    result = db.execute(sql, payload).fetchone()
    db.commit()

    return {
        "status": "success",
        "scmdc_id": result.scmdc_id,
        "discussion_id": result.discussion_id,
        "message": "Discussion child created successfully"
    }


@router.put("/update/{scmdc_id}")
def update_discussion_child(scmdc_id: int, data: DiscussionChildUpdate, db: Session = Depends(get_db)):
    existing = db.execute(
        text("SELECT scmdc_id FROM safety_committee_minutes_discussion_child WHERE scmdc_id = :scmdc_id"),
        {"scmdc_id": scmdc_id}
    ).fetchone()

    if not existing:
        raise HTTPException(status_code=404, detail="Discussion child not found")

    payload = data.model_dump(exclude_unset=True)
    if not payload:
        return {"message": "No fields to update"}

    set_clause = ", ".join([f"{k} = :{k}" for k in payload.keys()])
    sql = text(f"""
        UPDATE safety_committee_minutes_discussion_child
        SET {set_clause}
        WHERE scmdc_id = :scmdc_id
    """)

    payload["scmdc_id"] = scmdc_id
    db.execute(sql, payload)
    db.commit()

    return {
        "status": "success",
        "message": "Discussion child updated successfully"
    }


@router.get("/get/{scmdc_id}")
def get_discussion_child_by_id(scmdc_id: int, db: Session = Depends(get_db)):
    result = db.execute(
        text("SELECT * FROM safety_committee_minutes_discussion_child WHERE scmdc_id = :scmdc_id"),
        {"scmdc_id": scmdc_id}
    ).mappings().first()

    if not result:
        raise HTTPException(status_code=404, detail="Discussion child not found")

    return {
        "status": "success",
        "data": dict(result)
    }