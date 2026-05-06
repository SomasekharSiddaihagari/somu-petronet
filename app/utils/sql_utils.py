# # app/utils/sql_utils.py
# from sqlalchemy import text
# from datetime import datetime

# def fetch_one(db, sql, params=None):
#     return db.execute(text(sql), params or {}).mappings().first()

# def execute(db, sql, params=None):
#     db.execute(text(sql), params or {})

# def now_utc():
#     return datetime.utcnow()

# app/utils/sql_utils.py
from sqlalchemy import text
from datetime import datetime, timezone

def fetch_one(db, sql, params=None):
    return db.execute(text(sql), params or {}).mappings().first()

def execute(db, sql, params=None):
    db.execute(text(sql), params or {})

def now_utc():
    return datetime.now(timezone.utc)