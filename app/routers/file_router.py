from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import FileResponse
from pathlib import Path
import os

router = APIRouter(prefix="/files", tags=["Files"])

BASE_DIR = Path(os.getenv("FILE_BASE_PATH", "./files")).resolve()

def normalize_path(path: str) -> Path:
    """
    Converts any incoming path (dev/prod/absolute/weird) into clean relative path
    """

    path = path.replace("\\", "/")

    # 🔥 Remove full system paths (Windows / Linux)
    if ":" in path:  # Windows path
        path = path.split(":", 1)[-1]

    if "/app/files" in path:
        path = path.split("/app/files", 1)[-1]

    if "files/" in path:
        path = path.split("files/", 1)[-1]

    # remove leading slash
    path = path.lstrip("/")

    return BASE_DIR / path


@router.get("/{path:path}")
def get_file(path: str, request: Request):

    requested_path = normalize_path(path).resolve()

    # 🔐 Prevent path traversal
    if not str(requested_path).startswith(str(BASE_DIR)):
        raise HTTPException(403, "Invalid path")

    if not requested_path.exists():
        raise HTTPException(404, "File not found")

    return FileResponse(requested_path)

# BASE_PATHS = {
#     "files": Path(os.getenv("FILE_BASE_PATH", "./files")).resolve(),
#     "uploads": Path(os.getenv("UPLOAD_BASE_PATH", "./uploads")).resolve()
# }

# def normalize_path(path: str) -> Path:
#     path = path.replace("\\", "/").lstrip("/")

#     # 🔥 Detect base folder
#     if path.startswith("uploads/"):
#         base_key = "uploads"
#         relative_path = path[len("uploads/"):]
#     elif path.startswith("files/"):
#         base_key = "files"
#         relative_path = path[len("files/"):]
#     else:
#         # default fallback (optional)
#         base_key = "uploads"
#         relative_path = path

#     return BASE_PATHS[base_key] / relative_path

# @router.get("/{path:path}")
# def get_file(path: str, request: Request):

#     if not hasattr(request.state, "user"):
#         raise HTTPException(401, "Unauthorized")

#     requested_path = normalize_path(path).resolve()

#     print("Incoming:", path)
#     print("Resolved:", requested_path)

#     # 🔐 Validate against both base paths
#     if not any(str(requested_path).startswith(str(base)) for base in BASE_PATHS.values()):
#         raise HTTPException(403, "Invalid path")

#     if not requested_path.exists():
#         raise HTTPException(404, "File not found")

#     return FileResponse(requested_path)


