import os
from fastapi import Depends
from sqlalchemy.orm import Session
from sqlalchemy import text

from app.database import get_db
def convert_to_urls(value):
    """Handles single or multiple file paths (comma separated)."""
    if not value:
        return []

    # Normalize slashes & split by comma
    files = [p.strip().replace("\\", "/") for p in value.split(",") if p.strip()]

    # Convert each to downloadable URL
    return [make_download_url(f) for f in files]
def serialize_finance(row):
    data = dict(row._mapping)

    # Multiple documents
    docs = data.get("upload_document")
    data["upload_document"] = convert_to_urls(docs)

    # Signature (usually single, but we handle multiple)
    sign = data.get("signature_name")
    sign_list = convert_to_urls(sign)

    data["signature_name"] = sign_list[0] if len(sign_list) == 1 else sign_list

    return data

import urllib.parse

def make_download_url(path: str) -> str:
    if not path or path in ["null", "None", None]:
        return None

    base_url =  os.getenv("BackEndPath")


    # Normalize slashes
    file_path = path.replace("\\", "/")

    # Remove drive letters (C:, D:, etc.)
    if ":" in file_path:
        file_path = file_path.split(":", 1)[1]

    # Remove unwanted base directory if present
    if file_path.startswith("/Petronet"):
        file_path = file_path.replace("/Petronet", "", 1)

    # Ensure leading slash
    file_path = "/" + file_path.lstrip("/")

    # URL encode safely
    encoded_path = urllib.parse.quote(file_path)

    return f"{base_url}{encoded_path}"

def get_all_finance(db: Session):
    query = """
        SELECT 
            uf.*, 
            u.first_name, 
            u.last_name, 
            u.employee_code,
            'user_investment' AS form_type
        FROM user_finance uf
        JOIN users u ON uf.user_id = u.user_id;
    """

    rows = db.execute(text(query)).fetchall()
    return [serialize_finance(r) for r in rows]


def get_finance_by_id(db: Session, finance_id: int):
    query = """
        SELECT 
            uf.*, 
            u.first_name, 
            u.last_name, 
            u.employee_code,
            'user_investment' AS form_type
        FROM user_finance uf
        JOIN users u ON uf.user_id = u.user_id
        WHERE uf.user_finance_id = :fid;
    """

    row = db.execute(text(query), {"fid": finance_id}).fetchone()
    return serialize_finance(row) if row else None


def get_finance_by_user_id(db: Session, user_id: int):
    query = """
        SELECT 
            uf.*, 
            u.first_name, 
            u.last_name, 
            u.employee_code,
            'user_investment' AS form_type
        FROM user_finance uf
        JOIN users u ON uf.user_id = u.user_id
        WHERE uf.user_id = :uid;
    """

    rows = db.execute(text(query), {"uid": user_id}).fetchall()
    return [serialize_finance(r) for r in rows] if rows else []








