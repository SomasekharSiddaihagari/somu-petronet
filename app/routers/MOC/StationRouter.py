from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.schemas.MOC.StationSchema import StationBase
from app.crud.MOC.StationCrud import get_all_stations
from app.utils.UserAuthUtils import verify_access_token
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.database import get_db





router = APIRouter(prefix="/api/stations", tags=["Stations"])

@router.get("DD", response_model=List[StationBase], summary="Get all station list")
def fetch_all_stations(
    db: Session = Depends(get_db),
    current_user: str = Depends(verify_access_token)
):
    try:
        stations = get_all_stations(db)
        return stations  # ✅ FastAPI automatically converts list[dict] -> JSON
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/GetAllUsersByStation")
def get_all_users_by_station(
    station_id: int,
    db: Session = Depends(get_db),
):
    try:
        query = text("""
            SELECT DISTINCT
                u.user_id,
                u.username,
                u.first_name,
                u.last_name,
                r.role_id,
                r.role_name
            FROM users u
            JOIN role_permissions rp
                ON rp.user_id = u.user_id
            JOIN roles r
                ON r.role_id = rp.role_id
            WHERE u.station_id = :station_id
              AND u.is_deleted = false
            ORDER BY r.role_id, u.first_name
        """)

        result = db.execute(query, {"station_id": station_id}).fetchall()

        roles_dict = {}

        for row in result:
            role_id = row.role_id
            role_name = row.role_name

            f_name = row.first_name
            l_name = row.last_name

            # fallback from username if missing
            if not f_name:
                clean_name = row.username.split('@')[0].replace('_', ' ').replace('.', ' ')
                parts = clean_name.split()
                if len(parts) > 0:
                    f_name = parts[0].capitalize()
                if len(parts) > 1:
                    l_name = " ".join(parts[1:]).title()

            user_data = {
                "user_id": row.user_id,
                "username": row.username,
                "first_name": f_name,
                "last_name": l_name
            }

            # Create role bucket if not exists
            if role_id not in roles_dict:
                roles_dict[role_id] = {
                    "role_id": role_id,
                    "role_name": role_name,
                    "users": []
                }

            roles_dict[role_id]["users"].append(user_data)

        return {
            "statusCode": "0000",
            "statusMessage": "Success",
            "data": {
                "station_id": station_id,
                "roles": list(roles_dict.values())
            }
        }

    except Exception as e:
        print("GET USERS BY STATION ERROR:", str(e))
        raise HTTPException(
            status_code=500,
            detail={
                "statusCode": "9999",
                "statusMessage": str(e),
                "data": {}
            }
        )
