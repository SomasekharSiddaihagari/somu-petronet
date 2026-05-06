from pydantic import BeforeValidator
from typing import Annotated, Any, Union
from datetime import date, datetime, time

def parse_flexible_datetime(v: Any) -> Any:
    if v is None or isinstance(v, (datetime, date, time)):
        return v
    if isinstance(v, str):
        v = v.replace('Z', '+00:00').strip()
        # Handle partial ISO strings like "2026-03-13T22"
        if 'T' in v and ':' not in v.split('T')[1]:
            v += ":00"
        try:
            return datetime.fromisoformat(v)
        except ValueError:
            return v
    return v

def validate_start_time(v: Any) -> Any:
    parsed = parse_flexible_datetime(v)
    if isinstance(parsed, datetime): return parsed.time()
    if isinstance(parsed, time): return parsed
    if isinstance(parsed, str):
        try: return time.fromisoformat(parsed)
        except ValueError: raise ValueError(f"Invalid time format: {parsed}")
    return parsed

def validate_logbook_date(v: Any) -> Any:
    parsed = parse_flexible_datetime(v)
    if isinstance(parsed, datetime): return parsed.date()
    if isinstance(parsed, date): return parsed
    if isinstance(parsed, str):
        try: return date.fromisoformat(parsed)
        except ValueError: raise ValueError(f"Invalid date format: {parsed}")
    return parsed

def validate_audit_datetime(v: Any) -> Any:
    parsed = parse_flexible_datetime(v)
    if isinstance(parsed, datetime): return parsed
    if isinstance(parsed, date): return datetime.combine(parsed, time.min)
    if isinstance(parsed, str):
        try: return datetime.fromisoformat(parsed)
        except ValueError: raise ValueError(f"Invalid datetime format: {parsed}")
    return parsed

def validate_float(v: Any) -> Any:
    if v is None or isinstance(v, float):
        return v
    if isinstance(v, str) and (v.strip() == "" or v.strip().lower() == "null"):
        return None
    try:
        return float(v)
    except (ValueError, TypeError):
        return v

def validate_int(v: Any) -> Any:
    if v is None or isinstance(v, int):
        return v
    if isinstance(v, str) and (v.strip() == "" or v.strip().lower() == "null"):
        return None
    try:
        return int(float(v))
    except (ValueError, TypeError):
        return v

# Reusable types to reduce schema code length
FlexTime = Annotated[Union[time, datetime, str], BeforeValidator(validate_start_time)]
FlexDate = Annotated[Union[date, datetime, str], BeforeValidator(validate_logbook_date)]
FlexDatetime = Annotated[Union[datetime, date, str], BeforeValidator(validate_audit_datetime)]
FlexFloat = Annotated[Union[float, str, None], BeforeValidator(validate_float)]
FlexInt = Annotated[Union[int, str, None], BeforeValidator(validate_int)]
