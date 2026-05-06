from fastapi import APIRouter, Depends, HTTPException, Header
from pydantic import BaseModel
from app.database import get_db
from app.schemas.gate_pass.GatePass import APIResponse
from app.utils.access_service import validate_token, verify_token

class ApiResponse(BaseModel):
    status_code: int
    status_message: str
    data: dict
router = APIRouter(tags=["Protected"])
from fastapi import Header, HTTPException, Depends


from fastapi import APIRouter, Depends, Header, Query, HTTPException
from app.database import get_db

# router = APIRouter()

@router.get("/digital-logbook"   , dependencies=[Depends(validate_token)]  
 )

def digital_logbook(
    db=Depends(get_db)
):
    # print("Authorization header:", authorization)
    # print("Query token:", token)

    # 🔹 Step 1: Extract token
    final_token = None

    # if authorization and authorization.startswith("Bearer "):
    #     final_token = authorization.replace("Bearer ", "").strip()
    #     print("Token from header:", final_token)

    # elif token:
    #     final_token = token.strip()
    #     print("Token from query param:", final_token)

    # else:
    #     raise HTTPException(
    #         status_code=401,
    #         detail="Token not provided (header or query param)"
    #     )

    # 🔹 Step 2: Verify token
    token_data = verify_token(db, final_token)

    # 🔹 Step 3: Success response (match your global schema)
    return {
        "status_code": 200,
        "status_message": "Access granted",
        "data": {
            "user_id": token_data["user_id"],
            "access_type": token_data["access_type"],
            "expires_at": token_data["expires_at"]
        }
    }



