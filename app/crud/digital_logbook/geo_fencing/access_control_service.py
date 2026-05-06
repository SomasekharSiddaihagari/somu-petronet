from requests import Session
from app.schemas.digital_logbook.geo_fencing.common import AccessControlCreateSchema, AccessControlUpdateSchema
from app.utils.sql_utils import fetch_one, execute
from app.utils.sql_utils import fetch_one, execute
from sqlalchemy import text


def create_access_control(db: Session, data: AccessControlCreateSchema):
    payload = data.model_dump()

    query = text("""
        INSERT INTO access_control_station (
            station_id,
            station_name,
            ip_from,
            ip_to,
            lat,
            lon,
            radius,
            is_active
        )
        VALUES (
            :station_id,
            :station_name,
            :ip_from,
            :ip_to,
            :latitude,
            :longitude,
            :radius,
            :is_active
        )
        RETURNING
            id,
            station_id,
            station_name,
            ip_from,
            ip_to,
            lat  AS latitude,
            lon  AS longitude,
            radius,
            is_active,
            created_at,
            updated_at
    """)

    result = db.execute(query, payload)
    row = result.mappings().first()

    db.commit()

    return row


def update_access_control(
    db: Session,
    rule_id: int,
    data: AccessControlUpdateSchema
):
    payload = data.model_dump(exclude_unset=True)
    payload["id"] = rule_id

    query = text("""
        UPDATE access_control_station
        SET
            station_id = COALESCE(:station_id, station_id),
            station_name = COALESCE(:station_name, station_name),
            ip_from = COALESCE(:ip_from, ip_from),
            ip_to = COALESCE(:ip_to, ip_to),
            lat = COALESCE(:latitude, lat),
            lon = COALESCE(:longitude, lon),
            radius = COALESCE(:radius, radius),
            is_active = COALESCE(:is_active, is_active),
            updated_at = NOW()
        WHERE id = :id
        RETURNING
            id,
            station_id,
            station_name,
            ip_from,
            ip_to,
            lat  AS latitude,
            lon  AS longitude,
            radius,
            is_active,
            created_at,
            updated_at
    """)

    result = db.execute(query, payload)
    row = result.mappings().first()

    if not row:
        raise ValueError("Access control rule not found")

    db.commit()

    return row
