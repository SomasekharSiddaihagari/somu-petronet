from datetime import datetime
import os
import shutil
from typing import List, Optional, Union
import urllib.parse
import uuid
from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from pydantic import BaseModel
from sqlalchemy import text
from sqlalchemy.orm import Session
from fastapi import Depends
from app.database import get_db
from app.models.MOC.StationModel import Station
from app.models.UserModel import User
from fastapi import APIRouter, Depends, Form, File, UploadFile, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import text
from typing import Optional, Union
from datetime import datetime
import json
import os
import shutil
import uuid
router = APIRouter(prefix="/api/super", tags=["get the dd for super"])

UPLOAD_FOLDER = "files/users_file"
class SupervisorResponse(BaseModel):
    user_id: int
    username: str
    first_name: Optional[str]
    last_name: Optional[str]
    email: Optional[str] = None
    designation: Optional[str]
    employee_code: Optional[str]

 
    class Config:
        from_attributes = True
 
 
 
@router.get("/supervisors")
def get_supervisors(db: Session = Depends(get_db)):
    sql = text("""
        SELECT 
            user_id,
            username,
            first_name,
            last_name,designation,
            email,employee_code
        FROM users
           
    """)

    result = db.execute(sql).fetchall()
    return [dict(row._mapping) for row in result]
 
 
def get_users_with_role_9(db: Session):
    sql = text("SELECT * FROM get_supervisors()")
    result = db.execute(sql).fetchall()
    return [dict(row._mapping) for row in result]