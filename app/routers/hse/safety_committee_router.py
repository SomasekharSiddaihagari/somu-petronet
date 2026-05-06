from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import text
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.hse.safety_committee_schema import SafetyCommitteeMemberCreate, SafetyCommitteeMemberUpdate
from app.crud.hse.safety_committee_crud import (
    create_safety_committee_member,
    get_all_safety_committee_members,
    get_safety_committee_member_by_id,
    get_team_by_station,
    update_safety_committee_member,
    delete_safety_committee_member
)
from app.utils.UserAuthUtils import verify_access_token

router = APIRouter(
    prefix="/api/hse/safety-committee-members",
    tags=["HSE Safety Committee Members"]
)


@router.get("/all")
def get_all_members(db: Session = Depends(get_db)):
    result = get_all_safety_committee_members(db)
    return {"status": "success", "data": result}

@router.post("/create")
def create_member(data: SafetyCommitteeMemberCreate, db: Session = Depends(get_db)):
    result = create_safety_committee_member(db, data)
    return result

@router.get("/team-by-station/{station_id}")
def get_team(station_id: int, db: Session = Depends(get_db)):
    return get_team_by_station(db, station_id)

@router.delete("/delete/{scm_id}")
def delete_member(scm_id: int, db: Session = Depends(get_db)):
    delete_safety_committee_member(db, scm_id)
    return {"message": "Deleted successfully"}



@router.put("/update/{scm_id}")
def update_member(scm_id: int, data: SafetyCommitteeMemberUpdate, db: Session = Depends(get_db)):
    existing = get_safety_committee_member_by_id(db, scm_id)
    if not existing:
        raise HTTPException(status_code=404, detail="Member not found")
    result = update_safety_committee_member(db, scm_id, data)
    return {"status": "success", "message": result["message"]}


@router.get("/engineers/{station_id}")
def get_engineers_by_station(
    station_id: int,
    current_user_id: int,   # 👈 pass logged-in user id
    db: Session = Depends(get_db)
):
    
    sql = text("""
        SELECT DISTINCT ON (u.user_id)
            u.user_id,
            u.first_name,
            u.last_name,
            u.designation,
            u.email,
            st.station_name
        FROM users u
        JOIN role_permissions rp ON rp.user_id = u.user_id
        JOIN station st ON st.station_id = u.station_id
        WHERE rp.role_id = 1
        AND u.station_id = :station_id
        AND u.user_id != :current_user_id   -- ✅ EXCLUDE LOGGED-IN USER
        AND u.is_deleted = FALSE
        AND u.is_employee = TRUE
        ORDER BY u.user_id, u.first_name
    """)

    result = db.execute(sql, {
        "station_id": station_id,
        "current_user_id": current_user_id
    }).mappings().all()

    return {
        "status": "success",
        "role": "Engineer",
        "data": [dict(r) for r in result]
    }

# @router.get("/engineers/{station_id}")
# def get_engineers_by_station(
#     station_id: int,
#     current_user_id: int,        # ← PASS FROM FRONTEND AS QUERY PARAM
#     db: Session = Depends(get_db)
# ):
    
#     sql = text("""
#         SELECT DISTINCT ON (u.user_id)
#             u.user_id,
#             u.first_name,
#             u.last_name,
#             u.designation,
#             u.email,
#             st.station_name
#         FROM users u
#         JOIN role_permissions rp ON rp.user_id = u.user_id
#         JOIN station st ON st.station_id = u.station_id
#         WHERE rp.role_id = 1
#         AND u.station_id = :station_id
#         AND u.is_deleted = FALSE
#         AND u.is_employee = TRUE
#         AND u.user_id != :current_user_id        -- ← EXCLUDE SELF
#         ORDER BY u.user_id, u.first_name
#     """)

#     result = db.execute(sql, {
#         "station_id": station_id,
#         "current_user_id": current_user_id
#     }).mappings().all()

#     return {
#         "status": "success",
#         "role": "Engineer",
#         "data": [dict(r) for r in result]
#     }







@router.get("/safety-officers/{station_id}")
def get_safety_officers_by_station(station_id: int, db: Session = Depends(get_db)):
    
    sql = text("""
        SELECT 
            u.user_id,
            u.first_name,
            u.last_name,
            u.designation,
            u.email,
            st.station_name
        FROM users u
        JOIN role_permissions rp ON rp.user_id = u.user_id
        JOIN station st ON st.station_id = u.station_id
        WHERE rp.role_id = 13
        AND u.station_id = :station_id
        AND u.is_deleted = FALSE
        ORDER BY u.first_name
    """)

    result = db.execute(sql, {"station_id": station_id}).mappings().all()

    return {
        "status": "success",
        "role": "Safety Officer",
        "data": result
    }