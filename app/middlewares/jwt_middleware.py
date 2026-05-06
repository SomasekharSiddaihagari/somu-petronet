from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request
from fastapi.responses import JSONResponse
from jose import jwt, JWTError, ExpiredSignatureError
import os

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"

if not SECRET_KEY:
    raise RuntimeError("SECRET_KEY is not set in environment")

PUBLIC_PATHS = [
    "/User/login",
    "/User/register",
    "/User/refresh-token",
    "/docs",
    "/User/validate-user",
    "/User/logout",
    "/api/password-reset/request",
    "/api/password-reset/submit",
    "/openapi.json",
    "/healthz",
]

# ✅ SAME STRUCTURE AS custom_exception
def error_response(error_code: int, message: str):
    return JSONResponse(
        status_code=401,
        content={
            "success": False,
            "error": {
                "code": error_code,
                "message": message
            }
        }
    )


class JWTMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request: Request, call_next):

        path = request.url.path

        # ✅ Allow OPTIONS (CORS)
        if request.method == "OPTIONS":
            return await call_next(request)

        # ✅ Allow public routes
        if any(path.startswith(p) for p in PUBLIC_PATHS):
            return await call_next(request)

        auth_header = request.headers.get("Authorization")

        # ✅ Cookie fallback (optional)
        if not auth_header:
            token = request.cookies.get("token")
            if token:
                auth_header = f"Bearer {token}"

        # ❌ Missing token
        if not auth_header:
            return error_response(9007, "Authorization header missing")

        # ❌ Invalid format
        if not auth_header.startswith("Bearer "):
            return error_response(9008, "Invalid token format")

        token = auth_header.replace("Bearer ", "")

        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

            # ❌ Wrong token type
            if payload.get("TokenType") != "AccessToken":
                return error_response(9004, "Invalid token type")

            # ❌ Invalid payload
            if not payload.get("sub"):
                return error_response(9001, "Invalid token payload")

            # ✅ Attach user to request
            request.state.user = payload

        except ExpiredSignatureError:
            return error_response(9078, "Token has expired. Please log in again.")

        except JWTError:
            return error_response(9006, "Invalid token")

        return await call_next(request)