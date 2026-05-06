import os
from datetime import datetime, timedelta, timezone
from typing import Optional

from jose import ExpiredSignatureError, JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from dotenv import load_dotenv
from app.schemas.UserSchema import TokenData

# ---------------- LOAD ENV ----------------
load_dotenv()

# ---------------- CONFIG ----------------
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"

if not SECRET_KEY:
    raise RuntimeError("SECRET_KEY not set in environment")

ACCESS_TOKEN_EXPIRE_MINUTES = int(os.environ["ACCESS_TOKEN_EXPIRE_MINUTES"])
REFRESH_TOKEN_EXPIRE_DAYS = int(os.environ["REFRESH_TOKEN_EXPIRE_DAYS"])

# 🔥 IMPORTANT: disable default FastAPI error
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="User/login",
    auto_error=False
)

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")


# ---------------- COMMON ERROR HELPER ----------------
def custom_exception(status_code: int, error_code: int, message: str):
    return HTTPException(
        status_code=status_code,
        detail={
            "success": False,
            "error": {
                "code": error_code,
                "message": message
            }
        }
    )


# ---------------- PASSWORD HELPERS ----------------
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password[:72])


# ---------------- TOKEN CREATION ----------------
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    now = datetime.now(timezone.utc)

    expire = now + (
        expires_delta if expires_delta else timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )

    to_encode.update({
        "exp": expire,
        "iat": now,
        "TokenType": "AccessToken"
    })

    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def create_refresh_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    now = datetime.now(timezone.utc)

    expire = now + (
        expires_delta if expires_delta else timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    )

    to_encode.update({
        "exp": expire,
        "iat": now,
        "TokenType": "RefreshToken"
    })

    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


# ---------------- TOKEN DECODING ----------------
def decode_token(token: str) -> TokenData:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        username: str = payload.get("sub")
        role: str = payload.get("role")

        if username is None:
            raise custom_exception(401, 9001, "Invalid token payload")

        return TokenData(username=username, role=role)

    except ExpiredSignatureError:
        raise custom_exception(401, 9002, "Token has expired")

    except JWTError:
        raise custom_exception(401, 9003, "Could not validate credentials")


# ---------------- VERIFY ACCESS TOKEN ----------------
def verify_access_token(token: str = Depends(oauth2_scheme)):

    # 🔥 HANDLE missing token (VERY IMPORTANT)
    if not token:
        raise custom_exception(401, 9007, "Authorization header missing")

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        # 🔥 Token type check (VAPT critical)
        if payload.get("TokenType") != "AccessToken":
            raise custom_exception(401, 9004, "Invalid token type")

        username: str = payload.get("sub")
        role: str = payload.get("role")
        permissions: list = payload.get("permissions", [])
        exp: int = payload.get("exp")

        if username is None:
            raise custom_exception(401, 9005, "Unauthorized user")

        expire_time = datetime.fromtimestamp(exp, tz=timezone.utc)

        return {
            "success": True,
            "data": {
                "username": username,
                "role": role,
                "permissions": permissions,
                "expires_at": expire_time,
            }
        }

    except ExpiredSignatureError:
        raise custom_exception(401, 9078, "Token has expired. Please log in again.")

    except JWTError:
        raise custom_exception(401, 9006, "Unauthorized user")