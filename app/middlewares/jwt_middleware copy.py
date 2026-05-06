from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request
from fastapi.responses import JSONResponse
from jose import jwt, JWTError
import os

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"

# APIs that do NOT require login
PUBLIC_PATHS = [
    "/User/login",
    "/User/register",
    "/User/refresh-token",
    "/docs",
    "/openapi.json",
    "/healthz",
]

class JWTMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request: Request, call_next):

        path = request.url.path

        # Allow public routes
        if any(path.startswith(p) for p in PUBLIC_PATHS):
            return await call_next(request)

        auth_header = request.headers.get("Authorization")

        if not auth_header:
            return JSONResponse(
                status_code=401,
                content={"detail": "Authorization header missing"}
            )

        if not auth_header.startswith("Bearer "):
            return JSONResponse(
                status_code=401,
                content={"detail": "Invalid token format"}
            )

        token = auth_header.replace("Bearer ", "")

        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            request.state.user = payload

        except JWTError:
            return JSONResponse(
                status_code=401,
                content={"detail": "Invalid or expired token"}
            )

        return await call_next(request)