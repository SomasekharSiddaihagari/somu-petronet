from sqlalchemy.orm import Session
from sqlalchemy import text
from typing import List, Dict

def get_all_stations(db: Session) -> List[Dict]:
    try:
        sql = text("SELECT * FROM get_all_stations();")
        result = db.execute(sql)
        rows = result.fetchall()

        #  Convert each row to dict for JSON serialization
        stations = [
            {
                "station_id": row.station_id,
                "station_name": row.station_name,
                "station_code": row.station_code,
                "is_deleted": row.is_deleted
            }
            for row in rows
        ]

        return stations
    except Exception as e:
        db.rollback()
        return [{"error": str(e)}]
