from fastapi import APIRouter, HTTPException, Request
from pathlib import Path
import os

from fastapi.responses import FileResponse


upload_router = APIRouter(prefix="/uploads", tags=["Uploads"])

UPLOADS_BASE_DIR = Path(os.getenv("UPLOAD_BASE_PATH", "./uploads")).resolve()


def normalize_uploads_path(path: str) -> Path:
    path = path.replace("\\", "/")

    if ":" in path:
        path = path.split(":", 1)[-1]

    if "/app/uploads" in path:
        path = path.split("/app/uploads", 1)[-1]

    if "uploads/" in path:
        path = path.split("uploads/", 1)[-1]

    path = path.lstrip("/")

    return UPLOADS_BASE_DIR / path


@upload_router.get("/{path:path}")
def get_upload_file(path: str, request: Request):

    requested_path = normalize_uploads_path(path).resolve()

    if not str(requested_path).startswith(str(UPLOADS_BASE_DIR)):
        raise HTTPException(403, "Invalid path")

    if not requested_path.exists():
        raise HTTPException(404, "File not found")

    return FileResponse(requested_path)