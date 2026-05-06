from fastapi import APIRouter, Depends, HTTPException
from requests import Session
from sqlalchemy import text
from app.crud.digital_logbook.geo_fencing.access_control_service import create_access_control, update_access_control
from app.database import get_db
from app.schemas.digital_logbook.geo_fencing.common import AccessControlCreateSchema, AccessControlResponseSchema, AccessControlUpdateSchema

router = APIRouter(
    prefix="/access-control",
    tags=["Access Control (IP / Geo) ( creat for ip and lat long for all station)"]
)

@router.post(
    "/access-control",
    response_model=AccessControlResponseSchema
)
def create_rule(payload: AccessControlCreateSchema, db=Depends(get_db)):
    return create_access_control(db, payload)




@router.put(
    "/{rule_id}",
    response_model=AccessControlResponseSchema,
    summary="Update IP / Geo access rule"
)



def update_rule(
    rule_id: int,
    payload: AccessControlUpdateSchema,
    db=Depends(get_db)
):
    try:
        return update_access_control(db, rule_id, payload)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/access-control-stations")
def get_all_access_control_stations(db: Session = Depends(get_db)):

    query = text("""
        SELECT
            id,
            station_id,
            station_name,
            ip_from,
            ip_to,
            lat,
            lon,
            radius,
            is_active,
            created_at,
            updated_at
        FROM access_control_station
        ORDER BY id DESC
    """)

    result = db.execute(query).mappings().all()

    return {
        "count": len(result),
        "data": result
    }


@router.delete(
    "/access-control-stations/{id}",
    summary="Delete access control station by ID"
)
def delete_access_control_station(
    id: int,
    db: Session = Depends(get_db)
):
    try:
        query = text("""
            DELETE FROM access_control_station
            WHERE id = :id
            RETURNING id
        """)

        result = db.execute(query, {"id": id}).fetchone()

        if not result:
            raise HTTPException(status_code=404, detail="Record not found")

        db.commit()

        return {
            "message": f"Access control station with id {id} deleted successfully"
        }

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))