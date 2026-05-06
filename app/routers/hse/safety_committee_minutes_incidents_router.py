from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from pydantic import BaseModel
from typing import Optional
from app.database import get_db

router = APIRouter(prefix="/safety-committee-minutes-incidents", tags=["Safety Committee Minutes Incidents"])


class SafetyCommitteeMinutesIncidentCreate(BaseModel):
    scmm_id: int
    incident_id: int


class SafetyCommitteeMinutesIncidentUpdate(BaseModel):
    scmm_id: Optional[int] = None
    incident_id: Optional[int] = None


@router.post("/create", status_code=201)
def create_incident(payload: SafetyCommitteeMinutesIncidentCreate, db: Session = Depends(get_db)):
    # Check if scmm_id exists
    check = db.execute(
        text("SELECT scmm_id FROM safety_committee_minutes WHERE scmm_id = :scmm_id"),
        {"scmm_id": payload.scmm_id}
    ).fetchone()

    if not check:
        raise HTTPException(status_code=404, detail="Safety committee minutes not found")

    # Insert into main table
    result = db.execute(
        text("""
            INSERT INTO safety_committee_minutes_incidents (scmm_id, incident_id)
            VALUES (:scmm_id, :incident_id)
            RETURNING scmi_id, scmm_id, incident_id, created_at
        """),
        {
            "scmm_id": payload.scmm_id,
            "incident_id": payload.incident_id,
        }
    ).fetchone()

    # Insert into history table
    db.execute(
        text("""
            INSERT INTO safety_committee_minutes_incidents_history (scmi_id, scmm_id, incident_id)
            VALUES (:scmi_id, :scmm_id, :incident_id)
        """),
        {
            "scmi_id": result.scmi_id,
            "scmm_id": result.scmm_id,
            "incident_id": result.incident_id,
        }
    )

    db.commit()

    return {
        "scmi_id": result.scmi_id,
        "scmm_id": result.scmm_id,
        "incident_id": result.incident_id,
        "created_at": result.created_at,
    }


@router.put("/{scmi_id}")
def update_incident(scmi_id: int, payload: SafetyCommitteeMinutesIncidentUpdate, db: Session = Depends(get_db)):
    # Check if record exists
    existing = db.execute(
        text("""
            SELECT scmi_id, scmm_id, incident_id 
            FROM safety_committee_minutes_incidents 
            WHERE scmi_id = :scmi_id
        """),
        {"scmi_id": scmi_id}
    ).fetchone()

    if not existing:
        raise HTTPException(status_code=404, detail="Incident record not found")

    # Build dynamic SET clause based on provided fields
    fields = {k: v for k, v in payload.model_dump().items() if v is not None}

    if not fields:
        raise HTTPException(status_code=400, detail="No fields provided to update")

    # If scmm_id is being updated, validate it exists
    if "scmm_id" in fields:
        check = db.execute(
            text("SELECT scmm_id FROM safety_committee_minutes WHERE scmm_id = :scmm_id"),
            {"scmm_id": fields["scmm_id"]}
        ).fetchone()
        if not check:
            raise HTTPException(status_code=404, detail="Safety committee minutes not found")

    set_clause = ", ".join([f"{key} = :{key}" for key in fields])
    fields["scmi_id"] = scmi_id

    result = db.execute(
        text(f"""
            UPDATE safety_committee_minutes_incidents
            SET {set_clause}
            WHERE scmi_id = :scmi_id
            RETURNING scmi_id, scmm_id, incident_id, created_at
        """),
        fields
    ).fetchone()

    # Insert updated state into history table
    db.execute(
        text("""
            INSERT INTO safety_committee_minutes_incidents_history (scmi_id, scmm_id, incident_id)
            VALUES (:scmi_id, :scmm_id, :incident_id)
        """),
        {
            "scmi_id": result.scmi_id,
            "scmm_id": result.scmm_id,
            "incident_id": result.incident_id,
        }
    )

    db.commit()

    return {
        "scmi_id": result.scmi_id,
        "scmm_id": result.scmm_id,
        "incident_id": result.incident_id,
        "created_at": result.created_at,
    }