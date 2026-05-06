# app/utils/time_utils.py

from datetime import timezone
import pytz

IST = pytz.timezone("Asia/Kolkata")

def to_ist(dt):
    if dt is None:
        return None
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(IST)
